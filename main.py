import tkinter as tk
from tkinter import font as tkfont
import re

GREEN = "#4a7c4e"
DARK_GREEN = "#3a6340"
LIGHT_GREEN = "#6aaa6e"
YELLOW_BG = "#f5f0d0"
GRAY_BG = "#d8d8d8"
WHITE = "#ffffff"
BLACK = "#111111"
RED = "#c0392b"
BLUE_ACTIVE = "#cce5ff"

class BowlingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bowling Calculator")
        self.root.configure(bg=GRAY_BG)
        self.root.resizable(False, False)
        try:
            import sys, os
            base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            self.root.iconbitmap(os.path.join(base, "icon.ico"))
        except Exception:
            pass

        self.series_list = []
        self.build_ui()

    def build_ui(self):
        top = tk.Frame(self.root, bg=GRAY_BG, pady=6)
        top.pack(fill="x", padx=10)

        tk.Label(top, text="Количество сбитых кеглей", bg=GRAY_BG,
                 font=("Arial", 11)).pack(side="left", padx=(0, 10))

        self.pin_buttons = []
        for i in range(11):
            btn = tk.Button(top, text=str(i), width=3, relief="groove",
                            bg=WHITE, font=("Arial", 10),
                            command=lambda v=i: self.on_pin_click(v))
            btn.pack(side="left", padx=1)
            self.pin_buttons.append(btn)

        add_btn = tk.Button(top, text="ДОБАВИТЬ СЕРИЮ »", bg=GRAY_BG,
                            font=("Arial", 10, "bold"), relief="groove",
                            command=self.add_series)
        add_btn.pack(side="left", padx=10)

        self.series_container = tk.Frame(self.root, bg=GRAY_BG)
        self.series_container.pack(fill="both", expand=True, padx=10, pady=5)

        self.add_series()

    def add_series(self):
        series = BowlingSeries(self.series_container, self, len(self.series_list))
        series.frame.pack(fill="x", pady=4)
        self.series_list.append(series)
        self.set_active_series(series)

    def set_active_series(self, series):
        self.active_series = series
        for s in self.series_list:
            s.set_active(s is series)

    def on_pin_click(self, value):
        if self.active_series:
            self.active_series.enter_pins(value)

    def remove_series(self, series):
        series.frame.destroy()
        self.series_list.remove(series)
        if self.series_list:
            self.set_active_series(self.series_list[-1])
        else:
            self.active_series = None
        self.update_overlay()

    def update_overlay(self):
        pass


class BowlingSeries:
    def __init__(self, parent, app, idx):
        self.app = app
        self.idx = idx
        self.rolls = []
        self.current_frame = 0
        self.roll_in_frame = 0
        self.first_roll_pins = 0
        self.active = False
        self.player_name = f"Игрок {idx + 1}"

        self.frame_data = [[] for _ in range(10)]

        self.frame = tk.Frame(parent, bg=GREEN, bd=1, relief="solid")
        self._build()

    def _build(self):
        header = tk.Frame(self.frame, bg=GREEN)
        header.pack(fill="x")

        self.close_btn = tk.Button(header, text="×", bg=GREEN, fg=WHITE,
                                   font=("Arial", 9, "bold"), bd=0, padx=4,
                                   command=lambda: self.app.remove_series(self))
        self.close_btn.pack(side="left")

        self.name_var = tk.StringVar(value=self.player_name)
        name_entry = tk.Entry(header, textvariable=self.name_var, bg=GREEN,
                              fg=WHITE, font=("Arial", 10, "bold"),
                              bd=0, insertbackground=WHITE, width=20)
        name_entry.pack(side="left", padx=5)
        name_entry.bind("<Return>", lambda e: self.app.root.focus())

        table = tk.Frame(self.frame, bg=DARK_GREEN)
        table.pack(fill="x", padx=2, pady=(0, 2))

        self.cell_frames = []
        self.cell_labels_top = []
        self.cell_labels_bot = []
        self.score_labels = []

        for f in range(10):
            col = tk.Frame(table, bg=DARK_GREEN, bd=1, relief="solid")
            col.grid(row=0, column=f, sticky="nsew", padx=1, pady=1)
            table.columnconfigure(f, weight=1)

            num_lbl = tk.Label(col, text=str(f + 1), bg=GRAY_BG,
                               font=("Arial", 9), width=6)
            num_lbl.pack(fill="x")

            if f < 9:
                sub = tk.Frame(col, bg=YELLOW_BG)
                sub.pack(fill="x")
                r1 = tk.Label(sub, text="", bg=YELLOW_BG, width=3,
                              font=("Arial", 9), relief="solid", bd=1)
                r1.pack(side="left", expand=True, fill="both")
                r2 = tk.Label(sub, text="", bg=YELLOW_BG, width=3,
                              font=("Arial", 9), relief="solid", bd=1)
                r2.pack(side="left", expand=True, fill="both")
                self.cell_labels_top.append((r1, r2, None))
            else:
                sub = tk.Frame(col, bg=YELLOW_BG)
                sub.pack(fill="x")
                r1 = tk.Label(sub, text="", bg=YELLOW_BG, width=2,
                              font=("Arial", 9), relief="solid", bd=1)
                r1.pack(side="left", expand=True, fill="both")
                r2 = tk.Label(sub, text="", bg=YELLOW_BG, width=2,
                              font=("Arial", 9), relief="solid", bd=1)
                r2.pack(side="left", expand=True, fill="both")
                r3 = tk.Label(sub, text="", bg=YELLOW_BG, width=2,
                              font=("Arial", 9), relief="solid", bd=1)
                r3.pack(side="left", expand=True, fill="both")
                self.cell_labels_top.append((r1, r2, r3))

            score_lbl = tk.Label(col, text="", bg=YELLOW_BG,
                                 font=("Arial", 10, "bold"), width=6)
            score_lbl.pack(fill="x")
            self.score_labels.append(score_lbl)
            self.cell_frames.append(col)

        score_col = tk.Frame(table, bg=DARK_GREEN, bd=1, relief="solid")
        score_col.grid(row=0, column=10, sticky="nsew", padx=1, pady=1)
        tk.Label(score_col, text="Счет", bg=GRAY_BG,
                 font=("Arial", 9), width=6).pack(fill="x")
        tk.Label(score_col, text="", bg=YELLOW_BG, width=6).pack(fill="x")
        self.total_label = tk.Label(score_col, text="", bg=YELLOW_BG,
                                    font=("Arial", 10, "bold"), width=6)
        self.total_label.pack(fill="x")

        max_col = tk.Frame(table, bg=DARK_GREEN, bd=1, relief="solid")
        max_col.grid(row=0, column=11, sticky="nsew", padx=1, pady=1)
        tk.Label(max_col, text="MAX", bg=GRAY_BG,
                 font=("Arial", 9), width=6).pack(fill="x")
        tk.Label(max_col, text="", bg=YELLOW_BG, width=6).pack(fill="x")
        self.max_label = tk.Label(max_col, text="300", bg=GRAY_BG,
                                  font=("Arial", 10, "bold"), width=6)
        self.max_label.pack(fill="x")

    def set_active(self, val):
        self.active = val
        bg = BLUE_ACTIVE if val else YELLOW_BG
        for labels in self.cell_labels_top:
            for lbl in labels:
                if lbl:
                    lbl.config(bg=bg)
        for lbl in self.score_labels:
            lbl.config(bg=bg)
        self.total_label.config(bg=bg)

    def enter_pins(self, pins):
        if self.current_frame >= 10:
            return

        f = self.current_frame
        r = self.roll_in_frame

        if f < 9:
            if r == 0:
                if pins > 10:
                    return
                self.first_roll_pins = pins
                self.frame_data[f] = [pins]
                if pins == 10:
                    self.roll_in_frame = 0
                    self.current_frame += 1
                else:
                    self.roll_in_frame = 1
            else:
                if pins + self.first_roll_pins > 10:
                    return
                self.frame_data[f].append(pins)
                self.roll_in_frame = 0
                self.current_frame += 1
        else:
            if r == 0:
                if pins > 10:
                    return
                self.first_roll_pins = pins
                self.frame_data[9] = [pins]
                self.roll_in_frame = 1
            elif r == 1:
                if self.first_roll_pins == 10:
                    if pins > 10:
                        return
                    self.frame_data[9].append(pins)
                    self.roll_in_frame = 2
                    self.first_roll_pins = pins
                else:
                    if pins + self.first_roll_pins > 10:
                        return
                    self.frame_data[9].append(pins)
                    if self.first_roll_pins + pins == 10:
                        self.roll_in_frame = 2
                    else:
                        self.current_frame = 10
            elif r == 2:
                if pins > 10:
                    return
                self.frame_data[9].append(pins)
                self.current_frame = 10

        self.rolls = []
        for fd in self.frame_data:
            self.rolls.extend(fd)

        self.update_display()
        self.app.update_overlay()

    def compute_scores(self):
        scores = []
        ri = 0
        for f in range(10):
            if f < 9:
                if not self.frame_data[f]:
                    break
                if self.frame_data[f][0] == 10:
                    bonus = 0
                    next_rolls = self.rolls[ri + 1:]
                    if len(next_rolls) >= 2:
                        bonus = next_rolls[0] + next_rolls[1]
                    total = 10 + bonus
                    scores.append(total)
                    ri += 1
                elif len(self.frame_data[f]) == 2:
                    s = sum(self.frame_data[f])
                    if s == 10:
                        bonus = 0
                        next_rolls = self.rolls[ri + 2:]
                        if next_rolls:
                            bonus = next_rolls[0]
                        total = 10 + bonus
                    else:
                        total = s
                    scores.append(total)
                    ri += 2
                else:
                    break
            else:
                if self.frame_data[9]:
                    scores.append(sum(self.frame_data[9]))
        return scores

    def frame_display(self, f):
        d = self.frame_data[f]
        if not d:
            return ("", "", "")
        if f < 9:
            if d[0] == 10:
                return ("", "X", "")
            elif len(d) == 2:
                s = "-" if d[0] == 0 else str(d[0])
                if d[0] + d[1] == 10:
                    return (s, "/", "")
                else:
                    return (s, "-" if d[1] == 0 else str(d[1]), "")
            else:
                return ("-" if d[0] == 0 else str(d[0]), "", "")
        else:
            r = []
            for i, v in enumerate(d):
                if i == 0:
                    r.append("X" if v == 10 else ("-" if v == 0 else str(v)))
                elif i == 1:
                    if d[0] == 10:
                        r.append("X" if v == 10 else ("-" if v == 0 else str(v)))
                    else:
                        if d[0] + v == 10:
                            r.append("/")
                        else:
                            r.append("-" if v == 0 else str(v))
                elif i == 2:
                    if len(d) >= 2 and d[0] != 10 and d[0] + d[1] == 10:
                        r.append("X" if v == 10 else ("-" if v == 0 else str(v)))
                    elif d[0] == 10 and d[1] == 10:
                        r.append("X" if v == 10 else ("-" if v == 0 else str(v)))
                    elif d[0] == 10 and d[1] != 10:
                        if d[1] + v == 10:
                            r.append("/")
                        else:
                            r.append("-" if v == 0 else str(v))
                    else:
                        r.append("-" if v == 0 else str(v))
            while len(r) < 3:
                r.append("")
            return tuple(r)

    def update_display(self):
        scores = self.compute_scores()
        cumulative = 0

        for f in range(10):
            labels = self.cell_labels_top[f]
            disp = self.frame_display(f)

            if f < 9:
                labels[0].config(text=disp[0])
                labels[1].config(text=disp[1])
            else:
                labels[0].config(text=disp[0])
                labels[1].config(text=disp[1])
                if labels[2]:
                    labels[2].config(text=disp[2])

            if f < len(scores):
                cumulative += scores[f]
                self.score_labels[f].config(text=str(cumulative))
            else:
                self.score_labels[f].config(text="")

        if scores and len(scores) == 10:
            self.total_label.config(text=str(cumulative))
        elif scores:
            self.total_label.config(text=str(cumulative))
        else:
            self.total_label.config(text="")

        max_score = self.calc_max()
        self.max_label.config(text=str(max_score))

    def calc_max(self):
        scores = self.compute_scores()
        current = sum(scores)
        frames_done = len(scores)
        if self.current_frame >= 10:
            return current
        remaining_frames = 10 - frames_done
        max_possible = current + remaining_frames * 30
        if frames_done == 9 and self.frame_data[9]:
            pass
        return min(max_possible, 300)

    def get_total(self):
        scores = self.compute_scores()
        return sum(scores)

    def get_max(self):
        return self.calc_max()

    def get_name(self):
        return self.name_var.get()


if __name__ == "__main__":
    root = tk.Tk()
    app = BowlingApp(root)
    root.mainloop()
