using System.IO;

namespace sam4
{
    public partial class Form1 : Form
    {
        private const string FileName = "reg.txt";

        public Form1()
        {
            InitializeComponent();
            comboBoxSubject.Items.AddRange(new object[] { "физика", "математика", "информатика" });
            comboBoxSubject.SelectedIndex = 0;
            rb9.Checked = true;
        }

        private string GetSelectedClass()
        {
            if (rb9.Checked) return "9";
            if (rb10.Checked) return "10";
            if (rb11.Checked) return "11";
            return string.Empty;
        }

        private void SetSelectedClass(string cls)
        {
            rb9.Checked = cls == "9";
            rb10.Checked = cls == "10";
            rb11.Checked = cls == "11";
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            try
            {
                using StreamWriter sw = new StreamWriter(FileName, false);
                sw.WriteLine(txtName.Text);
                sw.WriteLine(GetSelectedClass());
                sw.WriteLine(comboBoxSubject.SelectedItem?.ToString() ?? string.Empty);
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
                SetSelectedClass(sr.ReadLine() ?? string.Empty);
                string subj = sr.ReadLine() ?? string.Empty;
                int idx = comboBoxSubject.Items.IndexOf(subj);
                if (idx >= 0) comboBoxSubject.SelectedIndex = idx;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка чтения \n" + ex.Message);
            }
        }
    }
}
