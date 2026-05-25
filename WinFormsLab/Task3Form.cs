using System;
using System.IO;
using System.Windows.Forms;

namespace WinFormsLab;

// Задание 3: регистрационная форма с именем и городом.
// Данные записываются в файл sam3.txt и читаются по нажатию кнопок.
public class Task3Form : Form
{
    private const string DataFile = "sam3.txt";

    private readonly TextBox _nameBox;
    private readonly TextBox _cityBox;
    private readonly TextBox _output;

    public Task3Form()
    {
        Text = "Задание 3 — регистрация (имя, город)";
        Width = 460;
        Height = 380;
        StartPosition = FormStartPosition.CenterScreen;

        Controls.Add(new Label { Text = "Имя:", Left = 20, Top = 20, Width = 60 });
        _nameBox = new TextBox { Left = 100, Top = 18, Width = 320 };
        Controls.Add(_nameBox);

        Controls.Add(new Label { Text = "Город:", Left = 20, Top = 56, Width = 60 });
        _cityBox = new TextBox { Left = 100, Top = 54, Width = 320 };
        Controls.Add(_cityBox);

        var saveBtn = new Button { Text = "Записать", Left = 20, Top = 96, Width = 120 };
        saveBtn.Click += SaveBtn_Click;
        Controls.Add(saveBtn);

        var loadBtn = new Button { Text = "Прочитать", Left = 160, Top = 96, Width = 120 };
        loadBtn.Click += LoadBtn_Click;
        Controls.Add(loadBtn);

        _output = new TextBox
        {
            Left = 20,
            Top = 140,
            Width = 400,
            Height = 160,
            Multiline = true,
            ScrollBars = ScrollBars.Vertical,
            ReadOnly = true
        };
        Controls.Add(_output);
    }

    private void SaveBtn_Click(object? sender, EventArgs e)
    {
        try
        {
            File.AppendAllText(DataFile,
                $"{_nameBox.Text};{_cityBox.Text}{Environment.NewLine}");
            MessageBox.Show("Данные записаны в " + Path.GetFullPath(DataFile),
                "Запись", MessageBoxButtons.OK, MessageBoxIcon.Information);
            _nameBox.Clear();
            _cityBox.Clear();
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
