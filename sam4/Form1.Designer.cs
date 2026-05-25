namespace sam4
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;
        private Label lblName;
        private TextBox txtName;
        private GroupBox groupClass;
        private RadioButton rb9;
        private RadioButton rb10;
        private RadioButton rb11;
        private Label lblSubject;
        private ComboBox comboBoxSubject;
        private Button btnSave;
        private Button btnLoad;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.lblName = new Label();
            this.txtName = new TextBox();
            this.groupClass = new GroupBox();
            this.rb9 = new RadioButton();
            this.rb10 = new RadioButton();
            this.rb11 = new RadioButton();
            this.lblSubject = new Label();
            this.comboBoxSubject = new ComboBox();
            this.btnSave = new Button();
            this.btnLoad = new Button();

            this.groupClass.SuspendLayout();
            this.SuspendLayout();

            this.lblName.Text = "Имя:";
            this.lblName.Location = new System.Drawing.Point(20, 25);
            this.lblName.Size = new System.Drawing.Size(80, 20);

            this.txtName.Location = new System.Drawing.Point(110, 22);
            this.txtName.Size = new System.Drawing.Size(220, 23);

            // group class
            this.groupClass.Text = "Класс";
            this.groupClass.Location = new System.Drawing.Point(20, 60);
            this.groupClass.Size = new System.Drawing.Size(310, 60);
            this.groupClass.Controls.Add(this.rb9);
            this.groupClass.Controls.Add(this.rb10);
            this.groupClass.Controls.Add(this.rb11);

            this.rb9.Text = "9";
            this.rb9.Location = new System.Drawing.Point(20, 25);
            this.rb9.Size = new System.Drawing.Size(60, 22);

            this.rb10.Text = "10";
            this.rb10.Location = new System.Drawing.Point(100, 25);
            this.rb10.Size = new System.Drawing.Size(60, 22);

            this.rb11.Text = "11";
            this.rb11.Location = new System.Drawing.Point(180, 25);
            this.rb11.Size = new System.Drawing.Size(60, 22);

            this.lblSubject.Text = "Предмет:";
            this.lblSubject.Location = new System.Drawing.Point(20, 140);
            this.lblSubject.Size = new System.Drawing.Size(80, 20);

            this.comboBoxSubject.Location = new System.Drawing.Point(110, 137);
            this.comboBoxSubject.Size = new System.Drawing.Size(220, 23);
            this.comboBoxSubject.DropDownStyle = ComboBoxStyle.DropDownList;

            this.btnSave.Text = "Сохранить";
            this.btnSave.Location = new System.Drawing.Point(20, 180);
            this.btnSave.Size = new System.Drawing.Size(140, 32);
            this.btnSave.Click += new EventHandler(this.btnSave_Click);

            this.btnLoad.Text = "Прочитать";
            this.btnLoad.Location = new System.Drawing.Point(190, 180);
            this.btnLoad.Size = new System.Drawing.Size(140, 32);
            this.btnLoad.Click += new EventHandler(this.btnLoad_Click);

            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(360, 240);
            this.Controls.Add(this.lblName);
            this.Controls.Add(this.txtName);
            this.Controls.Add(this.groupClass);
            this.Controls.Add(this.lblSubject);
            this.Controls.Add(this.comboBoxSubject);
            this.Controls.Add(this.btnSave);
            this.Controls.Add(this.btnLoad);
            this.Name = "Form1";
            this.Text = "Регистрационная форма";

            this.groupClass.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
