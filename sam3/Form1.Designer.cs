namespace sam3
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;
        private Label lblName;
        private Label lblCity;
        private TextBox txtName;
        private TextBox txtCity;
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
            this.lblCity = new Label();
            this.txtName = new TextBox();
            this.txtCity = new TextBox();
            this.btnSave = new Button();
            this.btnLoad = new Button();

            this.SuspendLayout();

            this.lblName.Text = "Имя:";
            this.lblName.Location = new System.Drawing.Point(20, 25);
            this.lblName.Size = new System.Drawing.Size(70, 20);

            this.txtName.Location = new System.Drawing.Point(100, 22);
            this.txtName.Size = new System.Drawing.Size(200, 23);

            this.lblCity.Text = "Город:";
            this.lblCity.Location = new System.Drawing.Point(20, 60);
            this.lblCity.Size = new System.Drawing.Size(70, 20);

            this.txtCity.Location = new System.Drawing.Point(100, 57);
            this.txtCity.Size = new System.Drawing.Size(200, 23);

            this.btnSave.Text = "Сохранить";
            this.btnSave.Location = new System.Drawing.Point(20, 110);
            this.btnSave.Size = new System.Drawing.Size(130, 30);
            this.btnSave.Click += new EventHandler(this.btnSave_Click);

            this.btnLoad.Text = "Прочитать";
            this.btnLoad.Location = new System.Drawing.Point(170, 110);
            this.btnLoad.Size = new System.Drawing.Size(130, 30);
            this.btnLoad.Click += new EventHandler(this.btnLoad_Click);

            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(330, 170);
            this.Controls.Add(this.lblName);
            this.Controls.Add(this.txtName);
            this.Controls.Add(this.lblCity);
            this.Controls.Add(this.txtCity);
            this.Controls.Add(this.btnSave);
            this.Controls.Add(this.btnLoad);
            this.Name = "Form1";
            this.Text = "Регистрационная форма";

            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
