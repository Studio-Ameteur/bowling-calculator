import tkinter as tk
import sys
import os

GREEN = "#2a2a2a"
DARK_GREEN = "#111111"
YELLOW_BG = "#1e1e1e"
GRAY_BG = "#1a1a1a"
WHITE = "#ffffff"
BLUE_ACTIVE = "#0d3a5c"
GOLD = "#f0c040"
FG_DIM = "#888888"


def get_base():
    return getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))


def calculate_frame_scores(rolls):
    scores = []
    ri = 0
    for f in range(10):
        if ri >= len(rolls):
            break
        if f < 9:
            if rolls[ri] == 10:
                if ri + 2 < len(rolls):
                    scores.append(10 + rolls[ri+1] + rolls[ri+2])
                    ri += 1
                else:
                    break
            elif ri + 1 < len(rolls):
                s = rolls[ri] + rolls[ri+1]
                if s == 10:
                    if ri + 2 < len(rolls):
                        scores.append(10 + rolls[ri+2])
                        ri += 2
                    else:
                        break
                else:
                    scores.append(s)
                    ri += 2
            else:
                break
        else:
            tenth = rolls[ri:]
            if len(tenth) >= 2:
                if tenth[0] == 10 or (tenth[0] + tenth[1] == 10):
                    if len(tenth) >= 3:
                        scores.append(sum(tenth[:3]))
                    else:
                        break
                else:
                    scores.append(sum(tenth[:2]))
            else:
                break
    return scores


def calc_max_possible(frame_data, frame_scores):
    done = len(frame_scores)
    current = sum(frame_scores)
    remaining = 10 - done
    return min(300, current + remaining * 30)


def frame_display(frame_data, f):
    d = frame_data[f]
    if not d:
        return ("", "", "")
    if f < 9:
        if d[0] == 10:
            return ("", "X", "")
        r1 = "-" if d[0] == 0 else str(d[0])
        if len(d) < 2:
            return (r1, "", "")
        if d[0] + d[1] == 10:
            return (r1, "/", "")
        r2 = "-" if d[1] == 0 else str(d[1])
        return (r1, r2, "")
    else:
        result = []
        for i, v in enumerate(d):
            if i == 0:
                result.append("X" if v == 10 else ("-" if v == 0 else str(v)))
            elif i == 1:
                if d[0] == 10:
                    result.append("X" if v == 10 else ("-" if v == 0 else str(v)))
                elif d[0] + v == 10:
                    result.append("/")
                else:
                    result.append("-" if v == 0 else str(v))
            elif i == 2:
                prev_sum = d[0] + d[1] if len(d) >= 2 else 0
                if d[0] == 10 and d[1] == 10:
                    result.append("X" if v == 10 else ("-" if v == 0 else str(v)))
                elif d[0] == 10 and d[1] != 10:
                    result.append("/" if d[1] + v == 10 else ("-" if v == 0 else str(v)))
                elif prev_sum == 10:
                    result.append("X" if v == 10 else ("-" if v == 0 else str(v)))
                else:
                    result.append("-" if v == 0 else str(v))
        while len(result) < 3:
            result.append("")
        return tuple(result[:3])


class BowlingSeries:
    def __init__(self, parent, app, idx):
        self.app = app
        self.idx = idx
        self.frame_data = [[] for _ in range(10)]
        self.current_frame = 0
        self.roll_in_frame = 0
        self.active = False

        self.widget = tk.Frame(parent, bg="#111", bd=1, relief="flat")
        self._build()

    def _build(self):
        header = tk.Frame(self.widget, bg="#4a7c4e")
        header.pack(fill="x")

        tk.Button(header, text="×", bg="#4a7c4e", fg=WHITE,
                  font=("Arial", 9, "bold"), bd=0, padx=4,
                  command=self._remove).pack(side="left")

        self.name_var = tk.StringVar(value=f"Игрок {self.idx + 1}")
        name_entry = tk.Entry(header, textvariable=self.name_var, bg="#4a7c4e",
                              fg=WHITE, font=("Arial", 10, "bold"),
                              bd=0, insertbackground=WHITE, width=20)
        name_entry.pack(side="left", padx=5)

        self.widget.bind("<Button-1>", self._on_click)
        header.bind("<Button-1>", self._on_click)
        name_entry.bind("<Button-1>", lambda e: self.app.set_active(self))

        table = tk.Frame(self.widget, bg=DARK_GREEN)
        table.pack(fill="x", padx=2, pady=(0, 2))

        self.roll_labels = []
        self.score_labels = []

        for f in range(10):
            col = tk.Frame(table, bg=DARK_GREEN, bd=1, relief="solid")
            col.grid(row=0, column=f, sticky="nsew", padx=1, pady=1)
            table.columnconfigure(f, weight=1)

            tk.Label(col, text=str(f+1), bg="#2a2a2a", fg="#888",
                     font=("Arial", 8), width=6).pack(fill="x")

            sub = tk.Frame(col, bg=YELLOW_BG)
            sub.pack(fill="x")

            if f < 9:
                r1 = tk.Label(sub, text="", bg=YELLOW_BG, width=3,
                              font=("Arial", 9), relief="solid", bd=1)
                r1.pack(side="left", expand=True, fill="both")
                r2 = tk.Label(sub, text="", bg=YELLOW_BG, width=3,
                              font=("Arial", 9), relief="solid", bd=1)
                r2.pack(side="left", expand=True, fill="both")
                self.roll_labels.append((r1, r2, None))
            else:
                r1 = tk.Label(sub, text="", bg=YELLOW_BG, width=2,
                              font=("Arial", 9), relief="solid", bd=1)
                r1.pack(side="left", expand=True, fill="both")
                r2 = tk.Label(sub, text="", bg=YELLOW_BG, width=2,
                              font=("Arial", 9), relief="solid", bd=1)
                r2.pack(side="left", expand=True, fill="both")
                r3 = tk.Label(sub, text="", bg=YELLOW_BG, width=2,
                              font=("Arial", 9), relief="solid", bd=1)
                r3.pack(side="left", expand=True, fill="both")
                self.roll_labels.append((r1, r2, r3))

            sc = tk.Label(col, text="", bg=YELLOW_BG,
                          font=("Arial", 10, "bold"), width=6)
            sc.pack(fill="x")
            self.score_labels.append(sc)

        score_col = tk.Frame(table, bg=DARK_GREEN, bd=1, relief="solid")
        score_col.grid(row=0, column=10, sticky="nsew", padx=1, pady=1)
        tk.Label(score_col, text="Счет", bg="#2a2a2a", fg="#888",
                 font=("Arial", 8), width=6).pack(fill="x")
        tk.Label(score_col, text="", bg="#1e1e1e", width=6).pack(fill="x")
        self.total_lbl = tk.Label(score_col, text="", bg="#1e1e1e", fg="#f0c040",
                                  font=("Arial", 10, "bold"), width=6)
        self.total_lbl.pack(fill="x")

        max_col = tk.Frame(table, bg=DARK_GREEN, bd=1, relief="solid")
        max_col.grid(row=0, column=11, sticky="nsew", padx=1, pady=1)
        tk.Label(max_col, text="MAX", bg="#2a2a2a", fg="#888",
                 font=("Arial", 8), width=6).pack(fill="x")
        tk.Label(max_col, text="", bg=YELLOW_BG, width=6).pack(fill="x")
        self.max_lbl = tk.Label(max_col, text="300", bg="#1a1a1a", fg="#f0c040",
                                font=("Arial", 10, "bold"), width=6)
        self.max_lbl.pack(fill="x")

    def _on_click(self, e=None):
        self.app.set_active(self)

    def _remove(self):
        self.app.remove_series(self)

    def set_active(self, val):
        self.active = val
        bg = BLUE_ACTIVE if val else YELLOW_BG
        for labels in self.roll_labels:
            for lbl in labels:
                if lbl:
                    lbl.config(bg=bg)
        for lbl in self.score_labels:
            lbl.config(bg=bg)
        self.total_lbl.config(bg=bg)

    def get_rolls_flat(self):
        rolls = []
        for fd in self.frame_data:
            rolls.extend(fd)
        return rolls

    def undo_last_roll(self):
        for f in range(9, -1, -1):
            if self.frame_data[f]:
                self.frame_data[f].pop()
                self.current_frame = f
                self.roll_in_frame = len(self.frame_data[f])
                self.refresh()
                self.app.update_pin_buttons()
                self.app.update_overlay()
                return

    def enter_pins(self, pins):
        if self.current_frame >= 10:
            return

        f = self.current_frame
        r = self.roll_in_frame

        if f < 9:
            if r == 0:
                self.frame_data[f] = [pins]
                if pins == 10:
                    self.current_frame += 1
                    self.roll_in_frame = 0
                else:
                    self.roll_in_frame = 1
            else:
                self.frame_data[f].append(pins)
                self.current_frame += 1
                self.roll_in_frame = 0
        else:
            self.frame_data[9].append(pins)
            d = self.frame_data[9]
            if len(d) == 2:
                if d[0] != 10 and d[0] + d[1] < 10:
                    self.current_frame = 10
                elif d[0] != 10 and d[0] + d[1] == 10:
                    self.roll_in_frame = 2
                else:
                    self.roll_in_frame = 2
            elif len(d) == 3:
                self.current_frame = 10
            self.roll_in_frame = len(d)

        self.refresh()
        self.app.update_overlay()

    def get_frame_scores(self):
        return calculate_frame_scores(self.get_rolls_flat())

    def get_total(self):
        return sum(self.get_frame_scores())

    def get_max(self):
        fs = self.get_frame_scores()
        return calc_max_possible(self.frame_data, fs)

    def get_name(self):
        return self.name_var.get()

    def get_display(self):
        result = []
        for f in range(10):
            d = self.frame_data[f]
            if not d:
                result.append([])
                continue
            disp = list(frame_display(self.frame_data, f))
            result.append([x for x in disp if x != ""])
        return result

    def refresh(self):
        fs = self.get_frame_scores()
        cumulative = 0
        for f in range(10):
            d = frame_display(self.frame_data, f)
            labels = self.roll_labels[f]
            for idx, val in enumerate(d[:3]):
                if idx < len(labels) and labels[idx] is not None:
                    if val == "X":
                        fg = "#5dde5d"
                    elif val == "/":
                        fg = "#f0c040"
                    else:
                        fg = WHITE
                    labels[idx].config(text=val, fg=fg)

            if f < len(fs):
                cumulative += fs[f]
                self.score_labels[f].config(text=str(cumulative), fg="#f0c040")
            else:
                self.score_labels[f].config(text="")

        total = sum(fs)
        self.total_lbl.config(text=str(total) if fs else "")
        self.max_lbl.config(text=str(self.get_max()))

    def get_allowed_pins(self):
        if self.current_frame >= 10:
            return set()
        f = self.current_frame
        r = self.roll_in_frame
        if f < 9:
            if r == 0:
                return set(range(11))
            else:
                first = self.frame_data[f][0] if self.frame_data[f] else 0
                return set(range(10 - first + 1))
        else:
            d = self.frame_data[9]
            if len(d) == 0:
                return set(range(11))
            elif len(d) == 1:
                if d[0] == 10:
                    return set(range(11))
                else:
                    return set(range(10 - d[0] + 1))
            elif len(d) == 2:
                if d[0] == 10:
                    if d[1] == 10:
                        return set(range(11))
                    else:
                        return set(range(10 - d[1] + 1))
                elif d[0] + d[1] == 10:
                    return set(range(11))
                else:
                    return set()
            return set()


class BowlingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bowling Calculator")
        self.root.configure(bg=GRAY_BG)
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap(os.path.join(get_base(), "icon.ico"))
        except Exception:
            pass

        self.series_list = []
        self.active_series = None
        self.overlay_win = None

        self._build_ui()
        self.add_series()

    def _build_ui(self):
        top = tk.Frame(self.root, bg="#111", pady=6)
        top.pack(fill="x", padx=10)

        tk.Label(top, text="Количество сбитых кеглей", bg="#111", fg=WHITE,
                 font=("Arial", 11)).pack(side="left", padx=(0, 10))

        self.pin_buttons = []
        for i in range(11):
            btn = tk.Button(top, text=str(i), width=3, relief="groove",
                            bg="#333", fg="#ffffff", font=("Arial", 10, "bold"), activebackground="#555", activeforeground="#ffffff",
                            command=lambda v=i: self.on_pin(v))
            btn.pack(side="left", padx=1)
            self.pin_buttons.append(btn)

        tk.Button(top, text="ДОБАВИТЬ СЕРИЮ »", bg="#2a2a2a", fg=WHITE,
                  font=("Arial", 10, "bold"), relief="groove",
                  command=self.add_series).pack(side="left", padx=8)

        tk.Button(top, text="Оверлей", bg="#2a2a2a", fg=WHITE,
                  font=("Arial", 10, "bold"), relief="groove",
                  command=self.show_overlay).pack(side="left", padx=4)

        self.undo_btn = tk.Button(top, text="← Отмена", bg="#7a1a1a", fg=WHITE,
                  font=("Arial", 10, "bold"), relief="groove",
                  command=self.undo_last)
        self.undo_btn.pack(side="left", padx=8)

        self.container = tk.Frame(self.root, bg="#111")
        self.container.pack(fill="both", expand=True, padx=10, pady=5)

    def add_series(self):
        s = BowlingSeries(self.container, self, len(self.series_list))
        s.widget.pack(fill="x", pady=4)
        self.series_list.append(s)
        self.set_active(s)

    def set_active(self, series):
        self.active_series = series
        for s in self.series_list:
            s.set_active(s is series)
        self.update_pin_buttons()

    def remove_series(self, series):
        series.widget.destroy()
        self.series_list.remove(series)
        if self.series_list:
            self.set_active(self.series_list[-1])
        else:
            self.active_series = None
            self.update_pin_buttons()
        self.update_overlay()

    def on_pin(self, value):
        if not self.active_series:
            return
        if self.active_series.current_frame >= 10:
            return
        allowed = self.active_series.get_allowed_pins()
        if value not in allowed:
            return
        self.active_series.enter_pins(value)
        self.update_pin_buttons()

    def update_pin_buttons(self):
        if not self.active_series or self.active_series.current_frame >= 10:
            for btn in self.pin_buttons:
                btn.config(state="disabled", bg="#222", fg="#555",
                           disabledforeground="#555")
            return
        allowed = self.active_series.get_allowed_pins()
        for i, btn in enumerate(self.pin_buttons):
            if i in allowed:
                btn.config(state="normal", bg="#3a7a3a", fg="#ffffff",
                           activebackground="#5aaa5a", activeforeground="#ffffff")
            else:
                btn.config(state="disabled", bg="#222", fg="#555",
                           disabledforeground="#555")

    def show_overlay(self):
        if self.overlay_win and self.overlay_win.winfo_exists():
            self.overlay_win.lift()
            return
        self.overlay_win = OverlayWindow(self.root, self)

    def undo_last(self):
        if self.active_series:
            self.active_series.undo_last_roll()

    def update_overlay(self):
        if self.overlay_win and self.overlay_win.winfo_exists():
            self.overlay_win.refresh()


class OverlayWindow(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Оверлей")
        self.configure(bg="#111")
        self.resizable(False, False)
        self.checkboxes = {}

        try:
            self.iconbitmap(os.path.join(get_base(), "icon.ico"))
        except Exception:
            pass

        self._build()
        self.refresh()

    def _build(self):
        self.checks_frame = tk.Frame(self, bg="#111", pady=4)
        self.checks_frame.pack(fill="x", padx=8)

        self.canvas_frame = tk.Frame(self, bg="#111")
        self.canvas_frame.pack(fill="both", expand=True, padx=8, pady=6)

    def _rebuild_checkboxes(self):
        for w in self.checks_frame.winfo_children():
            w.destroy()
        tk.Label(self.checks_frame, text="Показывать:", bg="#111", fg="#aaa",
                 font=("Arial", 8)).pack(side="left", padx=(0, 6))
        current_ids = {id(s) for s in self.app.series_list}
        for sid in list(self.checkboxes.keys()):
            if sid not in current_ids:
                del self.checkboxes[sid]
        for s in self.app.series_list:
            sid = id(s)
            if sid not in self.checkboxes:
                self.checkboxes[sid] = tk.BooleanVar(value=True)
            var = self.checkboxes[sid]
            cb = tk.Checkbutton(self.checks_frame, text=s.get_name(),
                                variable=var, bg="#111", fg="white",
                                selectcolor="#333", activebackground="#111",
                                activeforeground="white", font=("Arial", 8),
                                command=self.refresh)
            cb.pack(side="left", padx=4)

    def refresh(self):
        self._rebuild_checkboxes()
        self._draw_table()

    def _draw_table(self):
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        shown = [s for s in self.app.series_list
                 if self.checkboxes.get(id(s), tk.BooleanVar(value=True)).get()]

        if not shown:
            tk.Label(self.canvas_frame, text="Нет выбранных серий",
                     bg="#111", fg="#555", font=("Arial", 10)).pack(pady=20)
            return

        max_frame = 0
        for s in shown:
            for f in range(9, -1, -1):
                if s.frame_data[f]:
                    max_frame = max(max_frame, f)
                    break

        visible_frames = list(range(max_frame + 1)) if max_frame >= 0 else []
        last_frames = visible_frames[-4:] if len(visible_frames) > 4 else visible_frames

        BG_DARK = "#1a1a1a"
        BG_RED = "#b02020"
        BG_HEAD = "#2a2a2a"
        FG_WHITE = "#ffffff"
        FG_GRAY = "#aaaaaa"
        FG_YELLOW = "#f0c040"
        CW = 6
        NW = 14

        grid = tk.Frame(self.canvas_frame, bg="#111")
        grid.pack(fill="x")

        tk.Label(grid, text="", bg=BG_HEAD, width=NW, anchor="w",
                 font=("Arial", 9)).grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
        for ci, f in enumerate(last_frames):
            tk.Label(grid, text=str(f+1), bg=BG_HEAD, fg=FG_GRAY,
                     font=("Arial", 9, "bold"), width=CW,
                     anchor="center").grid(row=0, column=ci+1, padx=1, pady=1, sticky="nsew")
        tk.Label(grid, text="MAX", bg=BG_HEAD, fg=FG_GRAY,
                 font=("Arial", 9, "bold"), width=CW,
                 anchor="center").grid(row=0, column=len(last_frames)+1, padx=1, pady=1, sticky="nsew")

        totals = [s.get_total() for s in shown]
        best_total = max(totals) if totals else 0

        for idx, s in enumerate(shown):
            row_bg = BG_DARK if idx % 2 == 0 else "#1e1e1e"
            ri = idx + 1

            tk.Label(grid, text=s.get_name(), bg=row_bg, fg=FG_WHITE,
                     font=("Arial", 10, "bold"), width=NW,
                     anchor="w").grid(row=ri, column=0, padx=1, pady=1, sticky="nsew")

            disp = s.get_display()
            fs = s.get_frame_scores()
            cumulative_all = []
            c = 0
            for sc in fs:
                c += sc
                cumulative_all.append(c)

            my_total = s.get_total()
            diff = my_total - best_total

            for ci, f in enumerate(last_frames):
                d = disp[f] if f < len(disp) else []
                has_strike = "X" in d
                has_spare = "/" in d
                cell_bg = BG_RED if (has_strike or has_spare) else row_bg

                cell = tk.Frame(grid, bg=cell_bg)
                cell.grid(row=ri, column=ci+1, padx=1, pady=1, sticky="nsew")
                grid.columnconfigure(ci+1, minsize=50)

                roll_text = " ".join(d) if d else ""
                tk.Label(cell, text=roll_text, bg=cell_bg, fg=FG_WHITE,
                         font=("Arial", 9, "bold"), width=CW,
                         anchor="center").pack(fill="x")
                sc_text = str(cumulative_all[f]) if f < len(cumulative_all) else ""
                tk.Label(cell, text=sc_text, bg=cell_bg, fg=FG_YELLOW,
                         font=("Arial", 8, "bold"), width=CW,
                         anchor="center").pack(fill="x")

            max_val = s.get_max()
            max_cell = tk.Frame(grid, bg=row_bg)
            max_cell.grid(row=ri, column=len(last_frames)+1, padx=1, pady=1, sticky="nsew")
            grid.columnconfigure(len(last_frames)+1, minsize=50)
            tk.Label(max_cell, text=str(max_val), bg=row_bg, fg=FG_YELLOW,
                     font=("Arial", 10, "bold"), width=CW,
                     anchor="center").pack(fill="x")

class MiniBowlingGame(tk.Toplevel):
    W = 600
    H = 400
    BALL_R = 14
    PIN_R = 8
    LANE_Y = 340
    GUTTER_TOP = 60
    GUTTER_BOT = 380

    PIN_LAYOUT = [
        (300, 100),
        (282, 130), (318, 130),
        (264, 160), (300, 160), (336, 160),
        (246, 190), (282, 190), (318, 190), (354, 190),
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Mini Bowling")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        try:
            self.iconbitmap(os.path.join(get_base(), "icon.ico"))
        except Exception:
            pass

        self.canvas = tk.Canvas(self, width=self.W, height=self.H,
                                bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack()

        self.info = tk.Label(self, text="Зажми и отпусти ПРОБЕЛ чтобы бросить",
                             bg="#111", fg="#aaa", font=("Arial", 10))
        self.info.pack(fill="x")

        self.reset_state()
        self.bind_keys()
        self.draw()

    def reset_state(self):
        self.ball_x = 300.0
        self.ball_y = float(self.LANE_Y)
        self.ball_vx = 0.0
        self.ball_vy = 0.0
        self.launched = False
        self.power = 0
        self.charging = False
        self.aim_dir = 1
        self.aim_x = 300.0
        self.aim_speed = 2.5
        self.pins = [[x, y, True] for x, y in self.PIN_LAYOUT]
        self.rolling = False
        self.result_text = ""
        self.frame_count = 0
        self.after_id = None
        self._start_aim()

    def bind_keys(self):
        self.bind("<space>", self._on_space_press)
        self.bind("<KeyRelease-space>", self._on_space_release)
        self.bind("<r>", lambda e: self._restart())
        self.bind("<R>", lambda e: self._restart())

    def _restart(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.reset_state()
        self.draw()

    def _start_aim(self):
        self.launched = False
        self.rolling = False
        self.ball_x = 300.0
        self.ball_y = float(self.LANE_Y)
        self.ball_vx = 0.0
        self.ball_vy = 0.0
        self.power = 0
        self.charging = False
        self.aim_x = 300.0
        self.aim_dir = 1
        self._animate_aim()

    def _animate_aim(self):
        if self.launched:
            return
        self.aim_x += self.aim_speed * self.aim_dir
        if self.aim_x > 480 or self.aim_x < 120:
            self.aim_dir *= -1
        self.draw()
        self.after_id = self.after(16, self._animate_aim)

    def _on_space_press(self, e):
        if self.launched:
            return
        if not self.charging:
            self.charging = True
            self._charge()

    def _charge(self):
        if not self.charging or self.launched:
            return
        self.power = min(self.power + 2, 100)
        self.draw()
        self.after_id = self.after(30, self._charge)

    def _on_space_release(self, e):
        if self.launched:
            return
        self.charging = False
        self._launch()

    def _launch(self):
        self.launched = True
        speed = 4 + self.power * 0.12
        dx = self.aim_x - self.ball_x
        dist = abs(dx) if abs(dx) > 1 else 1
        total = ((self.ball_x - 300) ** 2 + (self.ball_y - 100) ** 2) ** 0.5
        self.ball_vx = dx / max(abs(self.ball_y - 100), 1) * speed * 0.6
        self.ball_vy = -speed
        self.rolling = True
        self._animate_ball()

    def _animate_ball(self):
        if not self.rolling:
            return
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        for pin in self.pins:
            if not pin[2]:
                continue
            dx = self.ball_x - pin[0]
            dy = self.ball_y - pin[1]
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < self.BALL_R + self.PIN_R + 2:
                pin[2] = False
                self.ball_vx += dx / dist * 1.5
                self.ball_vy += dy / dist * 0.5

        if self.ball_x < 80 or self.ball_x > 520:
            self.ball_vy = 0
            self.rolling = False
            self._show_result()
            self.draw()
            return

        if self.ball_y < 80:
            self.rolling = False
            self._show_result()
            self.draw()
            return

        self.draw()
        self.after_id = self.after(16, self._animate_ball)

    def _show_result(self):
        knocked = sum(1 for p in self.pins if not p[2])
        if knocked == 10:
            self.result_text = "STRIKE! 🎳"
        elif knocked == 0:
            self.result_text = "Мимо... 😅"
        else:
            self.result_text = f"Сбито: {knocked} из 10"
        self.info.config(text=f"{self.result_text}   |   R — играть снова")

    def draw(self):
        c = self.canvas
        c.delete("all")

        c.create_rectangle(80, 60, 520, 380, fill="#2d2d1a", outline="#555")
        c.create_rectangle(0, 0, 80, self.H, fill="#1a0a0a", outline="")
        c.create_rectangle(520, 0, self.W, self.H, fill="#1a0a0a", outline="")
        for i in range(80, 520, 40):
            c.create_line(i, 60, i, 380, fill="#3a3a20", width=1)

        for pin in self.pins:
            px, py, standing = pin
            color = "#f0f0e0" if standing else "#555"
            outline = "#aaa" if standing else "#333"
            c.create_oval(px-self.PIN_R, py-self.PIN_R,
                          px+self.PIN_R, py+self.PIN_R,
                          fill=color, outline=outline, width=2)

        if not self.launched:
            aim_ix = int(self.aim_x)
            c.create_line(aim_ix, self.LANE_Y - 10, aim_ix, 80,
                          fill="#ff6666", dash=(6, 4), width=1)
            bar_x = 10
            bar_y = self.H - 20
            c.create_rectangle(bar_x, bar_y - 80, bar_x+16, bar_y,
                                fill="#333", outline="#666")
            fill_h = int(self.power * 0.8)
            color = "#ff4444" if self.power > 70 else ("#ffaa00" if self.power > 40 else "#44cc44")
            c.create_rectangle(bar_x, bar_y - fill_h, bar_x+16, bar_y,
                                fill=color, outline="")
            c.create_text(bar_x+8, bar_y - 88, text="PWR", fill="#aaa",
                          font=("Arial", 7, "bold"))

        bx, by = int(self.ball_x), int(self.ball_y)
        c.create_oval(bx-self.BALL_R, by-self.BALL_R,
                      bx+self.BALL_R, by+self.BALL_R,
                      fill="#222299", outline="#4444ff", width=2)
        c.create_oval(bx-4, by-6, bx, by-2, fill="#5555cc", outline="")

        if self.result_text:
            c.create_text(self.W//2, self.H//2,
                          text=self.result_text, fill="#f0c040",
                          font=("Arial", 22, "bold"))

        knocked = sum(1 for p in self.pins if not p[2])
        c.create_text(self.W - 10, 10, anchor="ne",
                      text=f"Сбито: {knocked}/10",
                      fill="#aaa", font=("Arial", 9))


if __name__ == "__main__":
    root = tk.Tk()
    app = BowlingApp(root)

    keys = {"ctrl": False, "shift": False, "caps": False}

    def on_key(e):
        if e.keysym in ("Control_L", "Control_R"):
            keys["ctrl"] = True
        if e.keysym == "Shift_L":
            keys["shift"] = True
        if e.keysym == "Caps_Lock":
            keys["caps"] = True
        if keys["ctrl"] and keys["shift"] and keys["caps"]:
            keys["ctrl"] = keys["shift"] = keys["caps"] = False
            MiniBowlingGame(root)

    def on_key_release(e):
        if e.keysym in ("Control_L", "Control_R"):
            keys["ctrl"] = False
        if e.keysym == "Shift_L":
            keys["shift"] = False
        if e.keysym == "Caps_Lock":
            keys["caps"] = False

    root.bind("<KeyPress>", on_key)
    root.bind("<KeyRelease>", on_key_release)

    root.mainloop()
