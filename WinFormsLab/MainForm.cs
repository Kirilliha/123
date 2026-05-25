using System;
using System.Drawing;
using System.Windows.Forms;

namespace WinFormsLab;

public class MainForm : Form
{
    public MainForm()
    {
        Text = "Лабораторная работа: меню и диалоговые окна";
        Width = 460;
        Height = 360;
        StartPosition = FormStartPosition.CenterScreen;

        var label = new Label
        {
            Text = "Выберите пример для запуска:",
            Dock = DockStyle.Top,
            Height = 36,
            TextAlign = ContentAlignment.MiddleCenter,
            Font = new Font("Segoe UI", 11F, FontStyle.Bold)
        };
        Controls.Add(label);

        AddLauncher("Текстовый редактор (пример 1 и 2)", 50, () => new TextEditorForm().Show());
        AddLauncher("Задание 1 — цвет формы по двойному щелчку", 95, () => new Task1Form().Show());
        AddLauncher("Задание 2 — загрузка изображения", 140, () => new Task2Form().Show());
        AddLauncher("Задание 3 — регистрация (имя, город)", 185, () => new Task3Form().Show());
        AddLauncher("Задание 4 — регистрация (имя, класс, предмет)", 230, () => new Task4Form().Show());

        var exitBtn = new Button
        {
            Text = "Выход",
            Left = 150,
            Top = 280,
            Width = 140,
            Height = 30
        };
        exitBtn.Click += (_, _) => Application.Exit();
        Controls.Add(exitBtn);
    }

    private void AddLauncher(string text, int top, Action handler)
    {
        var btn = new Button
        {
            Text = text,
            Left = 40,
            Top = top,
            Width = 360,
            Height = 32
        };
        btn.Click += (_, _) => handler();
        Controls.Add(btn);
    }
}
