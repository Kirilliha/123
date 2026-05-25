using System;
using System.Windows.Forms;

namespace WinFormsLab;

// Задание 2: по нажатию кнопки вызывается openFileDialog,
// выбранное изображение загружается в pictureBox.
public class Task2Form : Form
{
    private readonly PictureBox _pictureBox;
    private readonly OpenFileDialog _openFileDialog;

    public Task2Form()
    {
        Text = "Задание 2 — загрузка изображения";
        Width = 520;
        Height = 420;
        StartPosition = FormStartPosition.CenterScreen;

        _openFileDialog = new OpenFileDialog
        {
            Filter = "Изображения|*.bmp;*.jpg;*.jpeg;*.png;*.gif;*.tif;*.tiff|Все файлы (*.*)|*.*"
        };

        var loadButton = new Button
        {
            Text = "Загрузить изображение...",
            Dock = DockStyle.Top,
            Height = 36
        };
        loadButton.Click += LoadButton_Click;

        _pictureBox = new PictureBox
        {
            Dock = DockStyle.Fill,
            SizeMode = PictureBoxSizeMode.Zoom,
            BorderStyle = BorderStyle.FixedSingle
        };

        Controls.Add(_pictureBox);
        Controls.Add(loadButton);
    }

    private void LoadButton_Click(object? sender, EventArgs e)
    {
        if (_openFileDialog.ShowDialog() != DialogResult.OK) return;
        try
        {
            _pictureBox.Image?.Dispose();
            _pictureBox.Image = Image.FromFile(_openFileDialog.FileName);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Не удалось загрузить изображение\n" + ex.Message,
                "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
