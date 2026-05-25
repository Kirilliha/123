namespace wf341
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        private TextBox textBox1;
        private MenuStrip menuStrip1;
        private ToolStripMenuItem файлToolStripMenuItem;
        private ToolStripMenuItem открытьToolStripMenuItem;
        private ToolStripMenuItem сохранитьToolStripMenuItem;
        private ToolStripMenuItem видToolStripMenuItem;
        private ToolStripMenuItem шрифтToolStripMenuItem;
        private ToolStripMenuItem цветToolStripMenuItem;
        private ToolStripMenuItem справкаToolStripMenuItem;
        private ToolStripMenuItem выходToolStripMenuItem;
        private ColorDialog colorDialog1;
        private FontDialog fontDialog1;
        private OpenFileDialog openFileDialog1;
        private SaveFileDialog saveFileDialog1;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();

            this.textBox1 = new TextBox();
            this.menuStrip1 = new MenuStrip();
            this.файлToolStripMenuItem = new ToolStripMenuItem();
            this.открытьToolStripMenuItem = new ToolStripMenuItem();
            this.сохранитьToolStripMenuItem = new ToolStripMenuItem();
            this.видToolStripMenuItem = new ToolStripMenuItem();
            this.шрифтToolStripMenuItem = new ToolStripMenuItem();
            this.цветToolStripMenuItem = new ToolStripMenuItem();
            this.справкаToolStripMenuItem = new ToolStripMenuItem();
            this.выходToolStripMenuItem = new ToolStripMenuItem();
            this.colorDialog1 = new ColorDialog();
            this.fontDialog1 = new FontDialog();
            this.openFileDialog1 = new OpenFileDialog();
            this.saveFileDialog1 = new SaveFileDialog();

            this.menuStrip1.SuspendLayout();
            this.SuspendLayout();

            // menuStrip1
            this.menuStrip1.Items.AddRange(new ToolStripItem[] {
                this.файлToolStripMenuItem,
                this.видToolStripMenuItem,
                this.справкаToolStripMenuItem,
                this.выходToolStripMenuItem });
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(480, 24);

            // файл
            this.файлToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] {
                this.открытьToolStripMenuItem,
                this.сохранитьToolStripMenuItem });
            this.файлToolStripMenuItem.Text = "файл";

            this.открытьToolStripMenuItem.Text = "открыть";
            this.открытьToolStripMenuItem.Click += new EventHandler(this.открытьToolStripMenuItem_Click);

            this.сохранитьToolStripMenuItem.Text = "сохранить";
            this.сохранитьToolStripMenuItem.Click += new EventHandler(this.сохранитьToolStripMenuItem_Click);

            // вид
            this.видToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] {
                this.шрифтToolStripMenuItem,
                this.цветToolStripMenuItem });
            this.видToolStripMenuItem.Text = "вид";

            this.шрифтToolStripMenuItem.Text = "шрифт";
            this.шрифтToolStripMenuItem.Click += new EventHandler(this.шрифтToolStripMenuItem_Click);

            this.цветToolStripMenuItem.Text = "цвет";
            this.цветToolStripMenuItem.Click += new EventHandler(this.цветToolStripMenuItem_Click);

            // справка
            this.справкаToolStripMenuItem.Text = "справка";
            this.справкаToolStripMenuItem.Click += new EventHandler(this.справкаToolStripMenuItem_Click);

            // выход
            this.выходToolStripMenuItem.Text = "выход";
            this.выходToolStripMenuItem.Click += new EventHandler(this.выходToolStripMenuItem_Click);

            // textBox1
            this.textBox1.Multiline = true;
            this.textBox1.ScrollBars = ScrollBars.Vertical;
            this.textBox1.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            this.textBox1.Location = new System.Drawing.Point(12, 30);
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(456, 318);

            // Form1
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(480, 360);
            this.Controls.Add(this.textBox1);
            this.Controls.Add(this.menuStrip1);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "Form1";
            this.Text = "Текстовый редактор";

            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
