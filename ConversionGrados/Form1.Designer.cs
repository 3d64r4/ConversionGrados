namespace ConversionGrados
{
    partial class Conversion_temp
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            btAceptar = new Button();
            etGradosC = new Label();
            etGradosF = new Label();
            ctGradosC = new TextBox();
            ctGradosF = new TextBox();
            SuspendLayout();
            // 
            // btAceptar
            // 
            btAceptar.Location = new Point(246, 280);
            btAceptar.Name = "btAceptar";
            btAceptar.RightToLeft = RightToLeft.No;
            btAceptar.Size = new Size(130, 36);
            btAceptar.TabIndex = 0;
            btAceptar.Text = "&Aceptar";
            btAceptar.UseVisualStyleBackColor = true;
            btAceptar.UseWaitCursor = true;
            btAceptar.Click += button1_Click;
            // 
            // etGradosC
            // 
            etGradosC.AutoSize = true;
            etGradosC.Font = new Font("Segoe UI", 14.25F, FontStyle.Regular, GraphicsUnit.Point, 0);
            etGradosC.Location = new Point(109, 115);
            etGradosC.Name = "etGradosC";
            etGradosC.Size = new Size(179, 25);
            etGradosC.TabIndex = 1;
            etGradosC.Text = "Grados Centigrados";
            etGradosC.UseWaitCursor = true;
            etGradosC.Click += label1_Click;
            // 
            // etGradosF
            // 
            etGradosF.AutoSize = true;
            etGradosF.Font = new Font("Segoe UI", 14.25F, FontStyle.Regular, GraphicsUnit.Point, 0);
            etGradosF.Location = new Point(109, 181);
            etGradosF.Name = "etGradosF";
            etGradosF.Size = new Size(155, 25);
            etGradosF.TabIndex = 2;
            etGradosF.Text = "Grados Farenheit";
            etGradosF.UseWaitCursor = true;
            etGradosF.Click += label2_Click;
            // 
            // ctGradosC
            // 
            ctGradosC.Location = new Point(344, 117);
            ctGradosC.Name = "ctGradosC";
            ctGradosC.Size = new Size(100, 23);
            ctGradosC.TabIndex = 3;
            ctGradosC.Text = "0.00";
            ctGradosC.TextAlign = HorizontalAlignment.Right;
            ctGradosC.UseWaitCursor = true;
            ctGradosC.TextChanged += textBox1_TextChanged;
            ctGradosC.Enter += ctGradosC_Enter;
            // 
            // ctGradosF
            // 
            ctGradosF.Location = new Point(344, 181);
            ctGradosF.Name = "ctGradosF";
            ctGradosF.Size = new Size(100, 23);
            ctGradosF.TabIndex = 5;
            ctGradosF.Text = "0.00";
            ctGradosF.TextAlign = HorizontalAlignment.Right;
            ctGradosF.UseWaitCursor = true;
            ctGradosF.Enter += ctGradosF_Enter;
            // 
            // Conversion_temp
            // 
            AcceptButton = btAceptar;
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = SystemColors.ActiveCaption;
            ClientSize = new Size(662, 382);
            Controls.Add(ctGradosF);
            Controls.Add(ctGradosC);
            Controls.Add(etGradosF);
            Controls.Add(etGradosC);
            Controls.Add(btAceptar);
            HelpButton = true;
            Name = "Conversion_temp";
            Text = "Conversion de temperatura";
            UseWaitCursor = true;
            Load += Form1_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button btAceptar;
        private Label etGradosC;
        private Label etGradosF;
        private TextBox ctGradosC;
        private TextBox ctGradosF;

    }
}
