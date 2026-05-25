using System.IO;

namespace sam3
{
    public partial class Form1 : Form
    {
        private const string FileName = "sam3.txt";

        public Form1()
        {
            InitializeComponent();
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            try
            {
                using StreamWriter sw = new StreamWriter(FileName, false);
                sw.WriteLine(txtName.Text);
                sw.WriteLine(txtCity.Text);
                MessageBox.Show("Данные сохранены в " + FileName, "Сохранение",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка записи \n" + ex.Message);
            }
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            if (!File.Exists(FileName))
            {
                MessageBox.Show("Файл " + FileName + " не найден", "Чтение",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }
            try
            {
                using StreamReader sr = new StreamReader(FileName);
                txtName.Text = sr.ReadLine() ?? string.Empty;
                txtCity.Text = sr.ReadLine() ?? string.Empty;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка чтения \n" + ex.Message);
            }
        }
    }
}
