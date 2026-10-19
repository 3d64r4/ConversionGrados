namespace ConversionGrados
{
    public partial class Conversion_temp : Form
    {
        public Conversion_temp()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }


        
        private void button1_Click(object sender, EventArgs e)
        {
            {
                double GradosCent;
                double GradosFahr;

                if (ctGradosC.Text != "" && ctGradosF.Text == "")
                {
                    GradosCent = Convert.ToDouble(ctGradosC.Text);

                    GradosFahr = (GradosCent * 9 / 5) + 32;

                    ctGradosF.Text = GradosFahr.ToString("N2");
                }
                else if (ctGradosF.Text != "" && ctGradosC.Text == "")
                {
                    GradosFahr = Convert.ToDouble(ctGradosF.Text);

                    GradosCent = (GradosFahr - 32) * 5 / 9;

                    ctGradosC.Text = GradosCent.ToString("N2");
                }
                else
                {
                    MessageBox.Show("Solo capture un tipo de grados, para convertilo al otro.");
                }
            }

        }

        private void ctGradosC_Enter(object sender, EventArgs e)
        {
            ctGradosF.Clear();
            ctGradosC.SelectAll();
        }

        private void ctGradosF_Enter(object sender, EventArgs e)
        {
            ctGradosC.Clear();
            ctGradosF.SelectAll();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
