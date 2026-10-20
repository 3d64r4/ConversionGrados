import csv
import os
from datetime import datetime, timedelta, timezone
 
from ctrader_open_api import Client, Protobuf, TcpProtocol, EndPoints
from ctrader_open_api.messages.OpenApiMessages_pb2 import (
    ProtoOAApplicationAuthReq,
    ProtoOAGetAccountListByAccessTokenReq,
    ProtoOAAccountAuthReq,
    ProtoOASymbolsListReq,
    ProtoOASymbolByIdReq,
    ProtoOAGetTrendbarsReq,
    ProtoOAErrorRes,
)
from ctrader_open_api.messages.OpenApiModelMessages_pb2 import ProtoOATrendbarPeriod
from twisted.internet import reactor
 
# ---------------- CONFIGURACIÓN ----------------
CLIENT_ID = os.getenv("CTRADER_CLIENT_ID", "44634_M0BNkQhjyhLWsZvvxntggRzHZOdF92xp7DW8mBAiJHacSP7LrB")
CLIENT_SECRET = os.getenv("CTRADER_CLIENT_SECRET", "6Ros9B5DlqNpDIeWeJvFKIfzBMN5ZFLBMLcvgIYhLoncGUHN9j")
ACCESS_TOKEN = os.getenv("CTRADER_ACCESS_TOKEN", "kQ0bkgD2ntifmbGAJ9QDcEQS4BV67sWeGetBhFRGu7g")
ENTORNO = os.getenv("CTRADER_ENV", "demo")        # "demo" o "live" (debe coincidir con la cuenta)
ACCOUNT_ID = os.getenv("CTRADER_ACCOUNT_ID")      # opcional: si no se pone, usa la primera cuenta del entorno
SIMBOLOS_ORO = ["XAUUSD", "GOLD", "XAU/USD"]      # el nombre varía según el bróker
DIAS = 15
ARCHIVO_CSV = "oro_m30_15dias.csv"
# -----------------------------------------------
 
host = EndPoints.PROTOBUF_LIVE_HOST if ENTORNO == "live" else EndPoints.PROTOBUF_DEMO_HOST
client = Client(host, EndPoints.PROTOBUF_PORT, TcpProtocol)
estado = {"account_id": int(ACCOUNT_ID) if ACCOUNT_ID else None}
 
 
def terminar(mensaje=None):
    if mensaje:
        print(mensaje)
    if reactor.running:
        reactor.stop()
 
 
def respuesta(msg):
    """Extrae el mensaje y lanza error si la API devolvió ProtoOAErrorRes."""
    res = Protobuf.extract(msg)
    if isinstance(res, ProtoOAErrorRes):
        raise RuntimeError(f"Error API: {res.errorCode} - {res.description}")
    return res
 
 
def on_error(failure):
    terminar(f"❌ {failure.getErrorMessage()}")
 
 
# 1) Autenticar la aplicación
def on_connected(_client):
    print(f"Conectado a {host}")
    req = ProtoOAApplicationAuthReq(clientId=CLIENT_ID, clientSecret=CLIENT_SECRET)
    client.send(req).addCallback(app_autenticada).addErrback(on_error)
 
 
# 2) Obtener cuentas (si no se indicó una)
def app_autenticada(msg):
    respuesta(msg)
    print("App autenticada")
    if estado["account_id"]:
        autenticar_cuenta()
    else:
        req = ProtoOAGetAccountListByAccessTokenReq(accessToken=ACCESS_TOKEN)
        client.send(req).addCallback(cuentas_recibidas).addErrback(on_error)
 
 
def cuentas_recibidas(msg):
    res = respuesta(msg)
    quiero_live = ENTORNO == "live"
    for cuenta in res.ctidTraderAccount:
        print(f"  Cuenta {cuenta.ctidTraderAccountId} ({'Live' if cuenta.isLive else 'Demo'})")
    candidatas = [c for c in res.ctidTraderAccount if c.isLive == quiero_live]
    if not candidatas:
        return terminar(f"❌ No hay cuentas {ENTORNO} autorizadas para este token.")
    estado["account_id"] = candidatas[0].ctidTraderAccountId
    autenticar_cuenta()
 
 
# 3) Autenticar la cuenta
def autenticar_cuenta():
    req = ProtoOAAccountAuthReq(ctidTraderAccountId=estado["account_id"], accessToken=ACCESS_TOKEN)
    client.send(req).addCallback(cuenta_autenticada).addErrback(on_error)
 
 
# 4) Buscar el símbolo del oro
def cuenta_autenticada(msg):
    respuesta(msg)
    print(f"Cuenta {estado['account_id']} autenticada")
    req = ProtoOASymbolsListReq(ctidTraderAccountId=estado["account_id"])
    client.send(req).addCallback(simbolos_recibidos).addErrback(on_error)
 
 
def simbolos_recibidos(msg):
    res = respuesta(msg)
    nombres = {s.symbolName.upper(): s for s in res.symbol}
    simbolo = next((nombres[n] for n in SIMBOLOS_ORO if n in nombres), None)
    if simbolo is None:  # búsqueda flexible, p.ej. "XAUUSD.r"
        simbolo = next((s for s in res.symbol if "XAUUSD" in s.symbolName.upper()), None)
    if simbolo is None:
        return terminar("❌ No encontré el oro. Revisa el nombre del símbolo en tu bróker.")
    estado["symbol_id"] = simbolo.symbolId
    estado["symbol_name"] = simbolo.symbolName
    print(f"Símbolo: {simbolo.symbolName} (id {simbolo.symbolId})")
    req = ProtoOASymbolByIdReq(ctidTraderAccountId=estado["account_id"], symbolId=[simbolo.symbolId])
    client.send(req).addCallback(detalle_simbolo).addErrback(on_error)
 
 
# 5) Obtener decimales y pedir las velas M30
def detalle_simbolo(msg):
    res = respuesta(msg)
    estado["digits"] = res.symbol[0].digits
    ahora = datetime.now(timezone.utc)
    desde = ahora - timedelta(days=DIAS)
    req = ProtoOAGetTrendbarsReq(
        ctidTraderAccountId=estado["account_id"],
        symbolId=estado["symbol_id"],
        period=ProtoOATrendbarPeriod.Value("M30"),
        fromTimestamp=int(desde.timestamp() * 1000),
        toTimestamp=int(ahora.timestamp() * 1000),
    )
    client.send(req).addCallback(velas_recibidas).addErrback(on_error)
 
 
# 6) Convertir y guardar
def velas_recibidas(msg):
    res = respuesta(msg)
    d = estado["digits"]
    filas = []
    for b in res.trendbar:
        # Los precios vienen en enteros (1/100000) y relativos al mínimo
        low = b.low
        fecha = datetime.fromtimestamp(b.utcTimestampInMinutes * 60, tz=timezone.utc)
        filas.append({
            "fecha_utc": fecha.strftime("%Y-%m-%d %H:%M"),
            "open": round((low + b.deltaOpen) / 100000, d),
            "high": round((low + b.deltaHigh) / 100000, d),
            "low": round(low / 100000, d),
            "close": round((low + b.deltaClose) / 100000, d),
            "volumen": b.volume,
        })
    filas.sort(key=lambda f: f["fecha_utc"])
 
    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["fecha_utc", "open", "high", "low", "close", "volumen"])
        writer.writeheader()
        writer.writerows(filas)
 
    print(f"✅ {len(filas)} velas de {estado['symbol_name']} guardadas en {ARCHIVO_CSV}")
    if filas:
        print("Última vela:", filas[-1])
    terminar()
 
 
client.setConnectedCallback(on_connected)
client.setDisconnectedCallback(lambda c, razon: terminar(f"Desconectado: {razon.getErrorMessage()}"))
client.startService()
reactor.callLater(60, terminar, "⏱️ Tiempo de espera agotado")  # por si algo se queda colgado
reactor.run()