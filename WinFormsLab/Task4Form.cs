using System;
using System.IO;
using System.Windows.Forms;

namespace WinFormsLab;

// Задание 4: регистрация — имя, класс (radioButton),
// предмет (comboBox: физика, математика, информатика).
// Запись/чтение из файла reg.txt по нажатию кнопок.
public class Task4Form : Form
{
    private const string DataFile = "reg.txt";

    private readonly TextBox _nameBox;
    private readonly RadioButton _r9;
    private readonly RadioButton _r10;
    private readonly RadioButton _r11;
    private readonly ComboBox _subject;
    private readonly TextBox _output;

    public Task4Form()
    {
        Text = "Задание 4 — регистрация (имя, класс, предмет)";
        Width = 480;
        Height = 460;
        StartPosition = FormStartPosition.CenterScreen;

        Controls.Add(new Label { Text = "Имя:", Left = 20, Top = 20, Width = 60 });
        _nameBox = new TextBox { Left = 100, Top = 18, Width = 340 };
        Controls.Add(_nameBox);

        var classGroup = new GroupBox
        {
            Text = "Класс",
            Left = 20,
            Top = 60,
            Width = 200,
            Height = 130
        };
        _r9 = new RadioButton { Text = "9 класс", Left = 15, Top = 25, Checked = true };
        _r10 = new RadioButton { Text = "10 класс", Left = 15, Top = 55 };
        _r11 = new RadioButton { Text = "11 класс", Left = 15, Top = 85 };
        classGroup.Controls.Add(_r9);
        classGroup.Controls.Add(_r10);
        classGroup.Controls.Add(_r11);
        Controls.Add(classGroup);

        Controls.Add(new Label { Text = "Предмет:", Left = 240, Top = 80, Width = 80 });
        _subject = new ComboBox
        {
            Left = 240,
            Top = 105,
            Width = 200,
            DropDownStyle = ComboBoxStyle.DropDownList
        };
        _subject.Items.AddRange(new object[] { "физика", "математика", "информатика" });
        _subject.SelectedIndex = 0;
        Controls.Add(_subject);

        var saveBtn = new Button { Text = "Записать", Left = 20, Top = 210, Width = 120 };
        saveBtn.Click += SaveBtn_Click;
        Controls.Add(saveBtn);

        var loadBtn = new Button { Text = "Прочитать", Left = 160, Top = 210, Width = 120 };
        loadBtn.Click += LoadBtn_Click;
        Controls.Add(loadBtn);

        _output = new TextBox
        {
            Left = 20,
            Top = 250,
            Width = 420,
            Height = 160,
            Multiline = true,
            ScrollBars = ScrollBars.Vertical,
            ReadOnly = true,
            Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        };
        Controls.Add(_output);
    }

    private string SelectedClass()
    {
        if (_r9.Checked) return "9";
        if (_r10.Checked) return "10";
        return "11";
    }

    private void SaveBtn_Click(object? sender, EventArgs e)
    {
        try
        {
            var line = $"{_nameBox.Text};{SelectedClass()};{_subject.SelectedItem}{Environment.NewLine}";
            File.AppendAllText(DataFile, line);
            MessageBox.Show("Данные записаны в " + Path.GetFullPath(DataFile),
                "Запись", MessageBoxButtons.OK, MessageBoxIcon.Information);
            _nameBox.Clear();
        }
        catch (Exception ex)
        {
            MessageBox.Show("Ошибка записи\n" + ex.Message,
                "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    private void LoadBtn_Click(object? sender, EventArgs e)
    {
        try
        {
            if (!File.Exists(DataFile))
            {
                _output.Text = "Файл " + DataFile + " ещё не создан.";
                return;
            }
            _output.Text = File.ReadAllText(DataFile);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Ошибка чтения\n" + ex.Message,
                "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
