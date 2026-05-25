# WinFormsLab — меню и диалоговые окна

Лабораторная работа на C# / .NET 8 Windows Forms. Реализованы оба
примера из методички и все четыре задания для самостоятельной работы.

## Состав

- `MainForm.cs` — стартовое окно со списком запускаемых форм.
- `TextEditorForm.cs` — Пример 1 и Пример 2: текстовый редактор с
  меню («файл» → открыть/сохранить, «вид» → шрифт/цвет,
  «справка», «выход»), диалогами `FontDialog`, `ColorDialog`,
  `OpenFileDialog`, `SaveFileDialog` и окнами `MessageBox`.
- `Task1Form.cs` — двойной щелчок по форме вызывает `ColorDialog`
  и меняет цвет формы.
- `Task2Form.cs` — кнопка вызывает `OpenFileDialog`, выбранное
  изображение загружается в `PictureBox`.
- `Task3Form.cs` — регистрационная форма (имя, город); запись и
  чтение из файла `sam3.txt`.
- `Task4Form.cs` — регистрация (имя, класс через `RadioButton`,
  предмет через `ComboBox`: физика / математика / информатика);
  запись и чтение из файла `reg.txt`.

## Сборка и запуск

Требуется .NET 8 SDK на Windows (Windows Forms работает только под
Windows).

```bash
cd WinFormsLab
dotnet build
dotnet run
```
