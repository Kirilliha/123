namespace sam2
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            openFileDialog1.Filter = "Изображения|*.bmp;*.jpg;*.jpeg;*.png;*.gif|Все файлы|*.*";
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    pictureBox1.Image = Image.FromFile(openFileDialog1.FileName);
                    this.Text = "загружено: " + openFileDialog1.FileName;
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Ошибка загрузки \n" + ex.Message);
                }
            }
        }
    }
}
