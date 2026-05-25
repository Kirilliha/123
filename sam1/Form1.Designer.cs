namespace sam1
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;
        private ColorDialog colorDialog1;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.colorDialog1 = new ColorDialog();

            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(400, 300);
            this.Name = "Form1";
            this.Text = "Двойной клик — выбор цвета формы";
            this.DoubleClick += new EventHandler(this.Form1_DoubleClick);
        }
    }
}
