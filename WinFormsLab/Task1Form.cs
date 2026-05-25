using System;
using System.Windows.Forms;

namespace WinFormsLab;

// Задание 1: двойной щелчок мыши на форме вызывает colorDialog
// и меняет цвет фона формы.
public class Task1Form : Form
{
    private readonly ColorDialog _colorDialog = new();

    public Task1Form()
    {
        Text = "Задание 1 — цвет формы (двойной щелчок)";
        Width = 400;
        Height = 300;
        StartPosition = FormStartPosition.CenterScreen;

        var hint = new Label
        {
            Text = "Дважды щёлкните по форме, чтобы изменить цвет фона",
            Dock = DockStyle.Top,
            Height = 60,
            TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        };
        Controls.Add(hint);

        DoubleClick += Form_DoubleClick;
        hint.DoubleClick += Form_DoubleClick;
    }

    private void Form_DoubleClick(object? sender, EventArgs e)
    {
        if (_colorDialog.ShowDialog() == DialogResult.OK)
            BackColor = _colorDialog.Color;
    }
}
