"""
Сапёр со скримером.

Запуск:
    python minesweeper.py

Правила:
    - Левый клик — открыть клетку.
    - Правый клик — поставить/снять флажок.
    - Откройте все клетки без мин, чтобы выиграть.
    - Откроете мину — будет страшно.

Режимы сложности:
    Лёгкий   — 5x5,  4 мины
    Средний  — 8x8,  12 мин
    Сложный  — 12x12, 30 мин
    Свой     — задайте размер (от 5) и количество мин
"""

import random
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

try:
    import winsound  # доступно только на Windows
except ImportError:
    winsound = None


CELL_SIZE = 36
NUMBER_COLORS = {
    1: "#1976d2",
    2: "#388e3c",
    3: "#d32f2f",
    4: "#7b1fa2",
    5: "#ff8f00",
    6: "#00838f",
    7: "#212121",
    8: "#616161",
}

DIFFICULTIES = {
    "Лёгкий":   {"size": 5,  "mines": 4},
    "Средний":  {"size": 8,  "mines": 12},
    "Сложный":  {"size": 12, "mines": 30},
}


def beep_loop(stop_event):
    """Громкие сигналы для эффекта скримера, пока окно открыто."""
    while not stop_event.is_set():
        try:
            if winsound is not None:
                winsound.Beep(880, 250)
                if stop_event.is_set():
                    break
                winsound.Beep(220, 250)
            else:
                # Терминальный bell — лучшее что доступно кроссплатформенно без зависимостей.
                sys.stdout.write("\a")
                sys.stdout.flush()
                time.sleep(0.25)
        except Exception:
            time.sleep(0.25)


class Screamer:
    """Полноэкранное окно со страшной рожей."""

    def __init__(self, parent):
        self.parent = parent
        self.stop_event = threading.Event()
        self.sound_thread = None

    def show(self):
        top = tk.Toplevel(self.parent)
        top.title("!!!")
        top.configure(bg="black")
        try:
            top.attributes("-fullscreen", True)
        except tk.TclError:
            top.geometry("900x700")
        top.attributes("-topmost", True)
        top.grab_set()
        top.focus_force()

        screen_w = top.winfo_screenwidth()
        screen_h = top.winfo_screenheight()

        canvas = tk.Canvas(top, bg="black", highlightthickness=0,
                           width=screen_w, height=screen_h)
        canvas.pack(fill="both", expand=True)

        self._draw_face(canvas, screen_w, screen_h)

        # Мигание фона + случайные «прыжки» лица.
        self._flash_state = {"on": True, "count": 0}
        self._flash(canvas, top, screen_w, screen_h)

        # Звук.
        self.sound_thread = threading.Thread(target=beep_loop,
                                             args=(self.stop_event,),
                                             daemon=True)
        self.sound_thread.start()

        def close(_event=None):
            self.stop_event.set()
            try:
                top.destroy()
            except tk.TclError:
                pass

        top.bind("<Escape>", close)
        top.bind("<Key>", close)
        top.bind("<Button-1>", close)
        top.protocol("WM_DELETE_WINDOW", close)

        # Автозакрытие через 5 секунд, если пользователь сам не закроет.
        top.after(5000, close)

    def _draw_face(self, canvas, w, h):
        canvas.delete("all")
        cx, cy = w // 2, h // 2
        r = min(w, h) // 3

        # Тёмно-серое лицо.
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                           fill="#2a0000", outline="#550000", width=6)

        # Глаза — кроваво-красные.
        eye_dx = r // 2
        eye_dy = r // 4
        eye_r = r // 5
        for sign in (-1, 1):
            ex, ey = cx + sign * eye_dx, cy - eye_dy
            canvas.create_oval(ex - eye_r, ey - eye_r, ex + eye_r, ey + eye_r,
                               fill="white", outline="black", width=3)
            pupil = eye_r // 2
            canvas.create_oval(ex - pupil, ey - pupil, ex + pupil, ey + pupil,
                               fill="red", outline="black")

        # Жуткий рот с зубами.
        mouth_w = r
        mouth_h = r // 2
        mx0, my0 = cx - mouth_w, cy + r // 4
        mx1, my1 = cx + mouth_w, cy + r // 4 + mouth_h
        canvas.create_oval(mx0, my0, mx1, my1, fill="black", outline="#660000",
                           width=4)
        # Зубы.
        tooth_count = 8
        step = (mx1 - mx0) / tooth_count
        for i in range(tooth_count):
            x0 = mx0 + i * step + 4
            x1 = x0 + step - 6
            canvas.create_polygon(
                x0, my0 + 6,
                x1, my0 + 6,
                (x0 + x1) / 2, my0 + 6 + step,
                fill="#e0e0e0", outline="black"
            )
            canvas.create_polygon(
                x0, my1 - 6,
                x1, my1 - 6,
                (x0 + x1) / 2, my1 - 6 - step,
                fill="#e0e0e0", outline="black"
            )

        # Кровь — потёки.
        for _ in range(20):
            sx = random.randint(int(mx0), int(mx1))
            sy = random.randint(int(my1) - 4, int(my1) + 8)
            ey = sy + random.randint(40, 220)
            canvas.create_line(sx, sy, sx, ey, fill="#aa0000",
                               width=random.randint(2, 6))

        # Текст.
        canvas.create_text(cx, cy + r + 80,
                           text="БУ-У-У!!!",
                           fill="red",
                           font=("Impact", 96, "bold"))
        canvas.create_text(cx, h - 40,
                           text="нажмите любую клавишу, чтобы закрыть",
                           fill="#660000", font=("Arial", 14))

    def _flash(self, canvas, top, w, h):
        if not top.winfo_exists():
            return
        # Меняем фон между чёрным и красным.
        self._flash_state["on"] = not self._flash_state["on"]
        bg = "black" if self._flash_state["on"] else "#400000"
        canvas.configure(bg=bg)
        top.configure(bg=bg)

        # Иногда сдвигаем рожу для эффекта дрожания.
        if self._flash_state["count"] % 3 == 0:
            self._draw_face(canvas, w, h)
        self._flash_state["count"] += 1

        top.after(120, lambda: self._flash(canvas, top, w, h))


class MinesweeperGame:
    def __init__(self, root, size, mines):
        self.root = root
        self.size = size
        self.mines = mines
        self.board = [[0] * size for _ in range(size)]
        self.revealed = [[False] * size for _ in range(size)]
        self.flagged = [[False] * size for _ in range(size)]
        self.first_click = True
        self.game_over = False
        self.cells_to_open = size * size - mines
        self.opened_count = 0
        self.buttons = []

        self.frame = tk.Frame(root, bg="#bdbdbd", padx=6, pady=6)
        self.frame.pack()

        self.status = tk.Label(self.frame,
                               text=self._status_text(),
                               font=("Arial", 12, "bold"),
                               bg="#bdbdbd")
        self.status.grid(row=0, column=0, columnspan=size, pady=(0, 6),
                         sticky="we")

        for r in range(size):
            row = []
            for c in range(size):
                b = tk.Label(self.frame, text="", width=2,
                             height=1,
                             relief="raised",
                             bd=2,
                             font=("Arial", 14, "bold"),
                             bg="#c0c0c0")
                b.grid(row=r + 1, column=c, padx=0, pady=0,
                       ipadx=4, ipady=2)
                b.bind("<Button-1>", lambda e, rr=r, cc=c: self.on_left(rr, cc))
                b.bind("<Button-3>", lambda e, rr=r, cc=c: self.on_right(rr, cc))
                # macOS / некоторые тачпады присылают Button-2 как правую кнопку.
                b.bind("<Button-2>", lambda e, rr=r, cc=c: self.on_right(rr, cc))
                row.append(b)
            self.buttons.append(row)

    def _status_text(self):
        flags = sum(self.flagged[r][c]
                    for r in range(self.size) for c in range(self.size))
        return f"Мин: {self.mines}   Флажков: {flags}   Открыто: {self.opened_count}/{self.cells_to_open}"

    def _update_status(self):
        self.status.config(text=self._status_text())

    def place_mines(self, safe_r, safe_c):
        forbidden = {(safe_r + dr, safe_c + dc)
                     for dr in (-1, 0, 1) for dc in (-1, 0, 1)}
        candidates = [(r, c) for r in range(self.size) for c in range(self.size)
                      if (r, c) not in forbidden]
        # Если мин больше, чем разрешённых клеток (маленькое поле), позволим
        # мины ближе к первой клетке, но не в ней самой.
        if len(candidates) < self.mines:
            candidates = [(r, c) for r in range(self.size)
                          for c in range(self.size)
                          if (r, c) != (safe_r, safe_c)]
        mine_cells = random.sample(candidates, self.mines)
        for r, c in mine_cells:
            self.board[r][c] = -1
        for r, c in mine_cells:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size \
                            and self.board[nr][nc] != -1:
                        self.board[nr][nc] += 1

    def on_left(self, r, c):
        if self.game_over or self.flagged[r][c] or self.revealed[r][c]:
            return
        if self.first_click:
            self.first_click = False
            self.place_mines(r, c)
        self.reveal(r, c)
        self._update_status()
        if not self.game_over and self.opened_count >= self.cells_to_open:
            self.win()

    def on_right(self, r, c):
        if self.game_over or self.revealed[r][c]:
            return
        self.flagged[r][c] = not self.flagged[r][c]
        b = self.buttons[r][c]
        if self.flagged[r][c]:
            b.config(text="⚑", fg="red")
        else:
            b.config(text="", fg="black")
        self._update_status()

    def reveal(self, r, c):
        if not (0 <= r < self.size and 0 <= c < self.size):
            return
        if self.revealed[r][c] or self.flagged[r][c]:
            return
        self.revealed[r][c] = True
        self.opened_count += 1
        v = self.board[r][c]
        b = self.buttons[r][c]
        b.config(relief="sunken", bd=1, bg="#e0e0e0")
        if v == -1:
            b.config(text="✸", bg="red", fg="black")
            self.lose(r, c)
            return
        if v > 0:
            b.config(text=str(v), fg=NUMBER_COLORS.get(v, "black"))
        else:
            b.config(text="")
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    self.reveal(r + dr, c + dc)

    def lose(self, mine_r, mine_c):
        self.game_over = True
        # Показать все мины.
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == -1 and not self.revealed[r][c]:
                    self.buttons[r][c].config(text="✸", bg="#ffaaaa",
                                              relief="sunken", bd=1)
        self.root.update_idletasks()
        # СКРИМЕР!
        screamer = Screamer(self.root)
        screamer.show()
        self.status.config(text="ПРОИГРЫШ! Нажмите «Новая игра».", fg="red")

    def win(self):
        self.game_over = True
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == -1:
                    self.buttons[r][c].config(text="⚑", fg="green",
                                              bg="#aaffaa")
        self.status.config(text="🎉 ПОБЕДА! Все мины обезврежены.", fg="green")
        messagebox.showinfo("Победа!", "Вы выиграли! Все мины найдены.")

    def destroy(self):
        self.frame.destroy()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Сапёр со скримером")
        self.root.configure(bg="#bdbdbd")
        self.game = None

        self._build_menu()
        self._build_controls()
        self._start_game("Лёгкий")

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        gamemenu = tk.Menu(menubar, tearoff=0)
        gamemenu.add_command(label="Новая игра",
                             command=self._restart_current)
        gamemenu.add_separator()
        for name in DIFFICULTIES:
            gamemenu.add_command(label=name,
                                 command=lambda n=name: self._start_game(n))
        gamemenu.add_command(label="Свой размер...",
                             command=self._custom_dialog)
        gamemenu.add_separator()
        gamemenu.add_command(label="Выход", command=self.root.destroy)
        menubar.add_cascade(label="Игра", menu=gamemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Как играть", command=self._show_help)
        helpmenu.add_command(label="О программе", command=self._show_about)
        menubar.add_cascade(label="Справка", menu=helpmenu)

        self.root.config(menu=menubar)

    def _build_controls(self):
        bar = tk.Frame(self.root, bg="#bdbdbd")
        bar.pack(fill="x", padx=6, pady=6)
        tk.Label(bar, text="Сложность:", bg="#bdbdbd",
                 font=("Arial", 11)).pack(side="left")
        self.diff_var = tk.StringVar(value="Лёгкий")
        combo = ttk.Combobox(bar, textvariable=self.diff_var,
                             values=list(DIFFICULTIES.keys()) + ["Свой..."],
                             state="readonly", width=12)
        combo.pack(side="left", padx=6)
        combo.bind("<<ComboboxSelected>>", self._on_combo)
        tk.Button(bar, text="🙂 Новая игра",
                  command=self._restart_current).pack(side="right")

    def _on_combo(self, _evt):
        choice = self.diff_var.get()
        if choice == "Свой...":
            self._custom_dialog()
        else:
            self._start_game(choice)

    def _restart_current(self):
        choice = self.diff_var.get()
        if choice in DIFFICULTIES:
            self._start_game(choice)
        elif self.game is not None:
            self._start_game_custom(self.game.size, self.game.mines)

    def _start_game(self, difficulty_name):
        cfg = DIFFICULTIES[difficulty_name]
        self.diff_var.set(difficulty_name)
        self._start_game_custom(cfg["size"], cfg["mines"])

    def _start_game_custom(self, size, mines):
        if self.game is not None:
            self.game.destroy()
        self.game = MinesweeperGame(self.root, size, mines)

    def _custom_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Свой размер")
        dlg.configure(bg="#bdbdbd")
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text="Размер поля (от 5 до 25):",
                 bg="#bdbdbd").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        size_var = tk.IntVar(value=10)
        tk.Spinbox(dlg, from_=5, to=25, textvariable=size_var,
                   width=6).grid(row=0, column=1, padx=8, pady=6)

        tk.Label(dlg, text="Количество мин:",
                 bg="#bdbdbd").grid(row=1, column=0, padx=8, pady=6, sticky="w")
        mines_var = tk.IntVar(value=15)
        tk.Spinbox(dlg, from_=1, to=600, textvariable=mines_var,
                   width=6).grid(row=1, column=1, padx=8, pady=6)

        def ok():
            try:
                s = int(size_var.get())
                m = int(mines_var.get())
            except (tk.TclError, ValueError):
                messagebox.showerror("Ошибка", "Введите целые числа.")
                return
            if s < 5:
                messagebox.showerror("Ошибка", "Минимальный размер поля — 5x5.")
                return
            if s > 25:
                messagebox.showerror("Ошибка", "Максимальный размер поля — 25x25.")
                return
            max_mines = s * s - 9
            if m < 1 or m > max_mines:
                messagebox.showerror("Ошибка",
                                     f"Количество мин должно быть от 1 до {max_mines}.")
                return
            self.diff_var.set("Свой...")
            dlg.destroy()
            self._start_game_custom(s, m)

        btns = tk.Frame(dlg, bg="#bdbdbd")
        btns.grid(row=2, column=0, columnspan=2, pady=8)
        tk.Button(btns, text="Начать", width=10, command=ok).pack(side="left",
                                                                    padx=4)
        tk.Button(btns, text="Отмена", width=10,
                  command=dlg.destroy).pack(side="left", padx=4)

    def _show_help(self):
        messagebox.showinfo(
            "Как играть",
            "• Левый клик — открыть клетку.\n"
            "• Правый клик — поставить или снять флажок ⚑.\n"
            "• Цифра в клетке — сколько мин рядом (по 8 соседям).\n"
            "• Откройте все клетки без мин — победа.\n"
            "• Если открыть мину — будет страшно!\n\n"
            "Совет: первая клетка всегда безопасна."
        )

    def _show_about(self):
        messagebox.showinfo(
            "О программе",
            "Сапёр со скримером.\n"
            "Режимы: Лёгкий (5x5), Средний (8x8), Сложный (12x12), Свой.\n"
            "Написано на Python + tkinter."
        )


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
