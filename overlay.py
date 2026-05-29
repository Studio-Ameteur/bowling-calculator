import tkinter as tk

BG = "#1a1a1a"
BG_ROW = "#222222"
BG_ROW_ALT = "#1e1e1e"
GOLD = "#f0c040"
GREEN = "#5dde5d"
WHITE = "#ffffff"
GRAY = "#888888"
ACCENT = "#4a7c4e"


class OverlayWindow(tk.Toplevel):
    def __init__(self, parent, get_series_func):
        super().__init__(parent)
        self.get_series = get_series_func

        self.title("Итоги — Боулинг")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.attributes("-topmost", True)

        try:
            import sys, os
            base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            self.iconbitmap(os.path.join(base, "icon.ico"))
        except Exception:
            pass

        self._build()
        self.refresh()

    def _build(self):
        header = tk.Frame(self, bg=ACCENT, pady=6)
        header.pack(fill="x")
        tk.Label(header, text="БОУЛИНГ — РЕЗУЛЬТАТЫ", bg=ACCENT, fg=WHITE,
                 font=("Arial", 11, "bold"), padx=12).pack(side="left")

        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=10, pady=8)

        footer = tk.Frame(self, bg=BG, pady=6)
        footer.pack(fill="x", padx=10)

        tk.Label(footer, text="Лучший результат:", bg=BG, fg=GRAY,
                 font=("Arial", 10)).pack(side="left")
        self.best_label = tk.Label(footer, text="—", bg=BG, fg=GOLD,
                                   font=("Arial", 13, "bold"))
        self.best_label.pack(side="left", padx=6)

    def refresh(self):
        for w in self.body.winfo_children():
            w.destroy()

        series_list = self.get_series()

        tk.Label(self.body, text="ПОСЛЕДНИЕ 3 СЕРИИ", bg=BG, fg=GRAY,
                 font=("Arial", 8, "bold")).pack(anchor="w", pady=(0, 6))

        recent = series_list[-3:] if series_list else []

        for i, s in enumerate(recent):
            bg = BG_ROW if i % 2 == 0 else BG_ROW_ALT
            row = tk.Frame(self.body, bg=bg, pady=8, padx=10)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=s.get_name(), bg=bg, fg=WHITE,
                     font=("Arial", 11, "bold"), width=16, anchor="w").pack(side="left")

            total = s.get_total()
            mx = s.get_max()

            tk.Label(row, text=str(total), bg=bg, fg=GOLD,
                     font=("Arial", 14, "bold"), width=5).pack(side="left")

            tk.Label(row, text=f"MAX: {mx}", bg=bg, fg=GREEN,
                     font=("Arial", 10), width=9).pack(side="left")

        if not recent:
            tk.Label(self.body, text="Нет данных", bg=BG, fg=GRAY,
                     font=("Arial", 10)).pack(pady=10)

        tk.Frame(self.body, bg="#333", height=1).pack(fill="x", pady=8)

        all_totals = [s.get_total() for s in series_list if s.rolls]
        best = max(all_totals) if all_totals else None
        self.best_label.config(text=str(best) if best is not None else "—")
