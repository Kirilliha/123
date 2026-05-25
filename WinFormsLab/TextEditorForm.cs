using System;
using System.IO;
using System.Windows.Forms;

namespace WinFormsLab;

// Пример 1 и Пример 2: текстовый редактор с меню,
// диалогами выбора шрифта/цвета и открытием/сохранением файлов.
public class TextEditorForm : Form
{
    private readonly TextBox _textBox;
    private readonly MenuStrip _menuStrip;
    private readonly ColorDialog _colorDialog;
    private readonly FontDialog _fontDialog;
    private readonly OpenFileDialog _openFileDialog;
    private readonly SaveFileDialog _saveFileDialog;

    public TextEditorForm()
    {
        Text = "Простой текстовый редактор";
        Width = 480;
        Height = 360;
        StartPosition = FormStartPosition.CenterScreen;

        _menuStrip = new MenuStrip();
        _colorDialog = new ColorDialog();
        _fontDialog = new FontDialog();
        _openFileDialog = new OpenFileDialog { Filter = "Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*" };
        _saveFileDialog = new SaveFileDialog { Filter = "Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*" };

        _textBox = new TextBox
        {
            Multiline = true,
            ScrollBars = ScrollBars.Vertical,
            Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right,
            Left = 0,
            Top = _menuStrip.Height + 24,
            Width = ClientSize.Width,
            Height = ClientSize.Height - _menuStrip.Height - 24
        };

        BuildMenu();

        MainMenuStrip = _menuStrip;
        Controls.Add(_textBox);
        Controls.Add(_menuStrip);
    }

    private void BuildMenu()
    {
        // Меню "файл"
        var fileMenu = new ToolStripMenuItem("файл");
        var openItem = new ToolStripMenuItem("открыть");
        openItem.Click += OpenItem_Click;
        var saveItem = new ToolStripMenuItem("сохранить");
        saveItem.Click += SaveItem_Click;
        fileMenu.DropDownItems.Add(openItem);
        fileMenu.DropDownItems.Add(saveItem);

        // Меню "вид"
        var viewMenu = new ToolStripMenuItem("вид");
        var fontItem = new ToolStripMenuItem("шрифт");
        fontItem.Click += FontItem_Click;
        var colorItem = new ToolStripMenuItem("цвет");
        colorItem.Click += ColorItem_Click;
        viewMenu.DropDownItems.Add(fontItem);
        viewMenu.DropDownItems.Add(colorItem);

        // Меню "справка"
        var helpItem = new ToolStripMenuItem("справка");
        helpItem.Click += HelpItem_Click;

        // Меню "выход"
        var exitItem = new ToolStripMenuItem("выход");
        exitItem.Click += ExitItem_Click;

        _menuStrip.Items.Add(fileMenu);
        _menuStrip.Items.Add(viewMenu);
        _menuStrip.Items.Add(helpItem);
        _menuStrip.Items.Add(exitItem);
    }

    private void FontItem_Click(object? sender, EventArgs e)
    {
        if (_fontDialog.ShowDialog() == DialogResult.OK)
            _textBox.Font = _fontDialog.Font;
    }

    private void ColorItem_Click(object? sender, EventArgs e)
    {
        if (_colorDialog.ShowDialog() == DialogResult.OK)
            _textBox.ForeColor = _colorDialog.Color;
    }

    private void HelpItem_Click(object? sender, EventArgs e)
    {
        MessageBox.Show("текстовый редактор\nразработал: студент",
            "Справка", MessageBoxButtons.OK, MessageBoxIcon.Information);
    }

    private void ExitItem_Click(object? sender, EventArgs e)
    {
        var res = MessageBox.Show("завершить работу?", "предупреждение",
            MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
        if (res == DialogResult.Yes)
            Close();
    }

    private void OpenItem_Click(object? sender, EventArgs e)
    {
        _openFileDialog.FileName = string.Empty;
        if (_openFileDialog.ShowDialog() != DialogResult.OK) return;

        var fn = _openFileDialog.FileName;
        Text = "открыт файл " + fn;
        try
        {
            using var sr = new StreamReader(fn);
            _textBox.Text = sr.ReadToEnd();
        }
        catch (Exception ex)
        {
            MessageBox.Show("Ошибка чтения\n" + ex, "Ошибка",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    private void SaveItem_Click(object? sender, EventArgs e)
    {
        if (_saveFileDialog.ShowDialog() != DialogResult.OK) return;

        var fn = _saveFileDialog.FileName;
        if (string.IsNullOrEmpty(fn)) return;

        Text = "сохранен файл " + fn;
        try
        {
            var fi = new FileInfo(fn);
            using var sw = fi.CreateText();
            sw.Write(_textBox.Text);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Ошибка записи\n" + ex, "Ошибка",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
