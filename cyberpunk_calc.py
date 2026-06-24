import math
import os
import sys
import random
import tkinter as tk

APP_NAME = "Cyberpunk Calc"
VERSION = "v1.1.0"
W, H = 420, 690
BG = "#050611"
CYAN = "#00fff0"
MAGENTA = "#ff22d2"
PURPLE = "#6622ff"
PINK_DARK = "#78124f"
TEAL_DARK = "#00898c"
TEXT = "#e9f7ff"


def resource_path(name: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base, name)


class CyberpunkCalc:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.overrideredirect(True)
        self.root.configure(bg=BG)
        self.root.geometry(f"{W}x{H}+160+80")
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap(resource_path("cyberpunk_calc.ico"))
        except Exception:
            pass

        self.expr = ""
        self.dragging = False
        self.drag_x = 0
        self.drag_y = 0
        self.build()
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<Key>", self.keypress)

    def glow_rect(self, x1, y1, x2, y2, color, width=2, glow=True):
        if glow:
            for spread in (5, 3):
                self.canvas.create_rectangle(x1-spread, y1-spread, x2+spread, y2+spread,
                                             outline=color, width=1)
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=width)

    def build(self):
        self.canvas = tk.Canvas(self.root, width=W, height=H, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Symmetrical safe outer frame.
        self.glow_rect(12, 12, W-12, H-12, CYAN, 2)
        self.glow_rect(16, 16, W-16, H-16, MAGENTA, 1)

        # X11-style title bar.
        title_top, title_bottom = 18, 66
        self.canvas.create_rectangle(18, title_top, W-18, title_bottom, fill="#070812", outline=CYAN, width=2)
        self.canvas.create_rectangle(31, 29, 59, 57, fill="#101020", outline="#b464ff", width=2)
        self.canvas.create_text(45, 43, text=">_", font=("Consolas", 11, "bold"), fill=CYAN)

        # Title is shifted left enough to never run under the controls.
        self.canvas.create_text(176, 43, text=APP_NAME, font=("Consolas", 13, "bold"), fill=CYAN)
        self.title_button(W-55, 26, W-25, 60, "×", MAGENTA, self.root.destroy)
        self.title_button(W-91, 26, W-61, 60, "□", CYAN, None)
        self.title_button(W-127, 26, W-97, 60, "–", CYAN, self.minimize)

        self.canvas.bind("<ButtonPress-1>", self.mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)

        self.canvas.create_text(49, 95, text="/* neon arithmetic desk */", anchor="w",
                                font=("Consolas", 12, "bold"), fill=MAGENTA)

        # Compact CRT display with all digit coordinates inside the box.
        self.display_box = (30, 116, W-30, 206)
        self.glow_rect(*self.display_box, MAGENTA, 2)
        self.canvas.create_rectangle(36, 122, W-36, 200, fill="#020712", outline="")
        for y in range(124, 200, 3):
            self.canvas.create_line(38, y, W-38, y, fill="#042323", width=1)
        self.canvas.create_text(W-58, 144, text="INPUT", font=("Consolas", 12), fill=CYAN)
        self.display_y = 178
        self.display_x = W - 62
        self.display_shadow2 = self.canvas.create_text(self.display_x, self.display_y, text="0", anchor="e",
                                                       font=("Consolas", 27, "bold"), fill="#005f66")
        self.display_shadow1 = self.canvas.create_text(self.display_x, self.display_y, text="0", anchor="e",
                                                       font=("Consolas", 27, "bold"), fill="#20ffff")
        self.display = self.canvas.create_text(self.display_x, self.display_y, text="0", anchor="e",
                                               font=("Consolas", 27, "bold"), fill="#b9ffff")
        self.root.after(90, self.animate_display)

        buttons = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],
            ["√", "x²", "1/x", "EXIT"],
        ]
        # Centered keypad: 4*74 + 3*16 = 344 wide; x0=38 gives 38 px margins.
        x0, y0 = 38, 238
        bw, bh = 74, 47
        gapx, gapy = 16, 13
        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                x = x0 + c * (bw + gapx)
                y = y0 + r * (bh + gapy)
                color = PURPLE
                fill = "#101135"
                if (r == 0 and c < 2) or label == "EXIT":
                    color, fill = MAGENTA, PINK_DARK
                if label == "=":
                    color, fill = CYAN, TEAL_DARK
                self.button(x, y, bw, bh, label, color, fill)

        # Footer placed below the keypad with enough clearance.
        self.canvas.create_text(W//2, H-38, text=VERSION, font=("Consolas", 11, "bold"), fill=CYAN)

    def animate_display(self):
        try:
            brightness = random.choice(["#8dffff", "#aaffff", "#c8ffff", "#e0ffff", "#75f6ff"])
            halo = random.choice(["#00d8e8", "#00ffff", "#009aa5", "#35ffff"])
            dx = random.choice([-1, 0, 0, 0, 1])
            dy = random.choice([-1, 0, 0, 1])
            self.canvas.itemconfigure(self.display, fill=brightness)
            self.canvas.itemconfigure(self.display_shadow1, fill=halo)
            self.canvas.coords(self.display_shadow2, self.display_x + dx*2, self.display_y + dy)
            self.canvas.coords(self.display_shadow1, self.display_x + dx, self.display_y + dy)
            self.canvas.coords(self.display, self.display_x, self.display_y)
            if random.random() < 0.03:
                self.canvas.itemconfigure(self.display, fill="#06383d")
                self.root.after(35, lambda: self.canvas.itemconfigure(self.display, fill=brightness))
        except tk.TclError:
            return
        self.root.after(random.randint(70, 150), self.animate_display)



    def title_button(self, x1, y1, x2, y2, label, color, cmd):
        tag = f"ctl_{label}_{x1}"
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#080913", outline="#44475a", width=2, tags=(tag, "control"))
        self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=label, font=("Consolas", 13, "bold"), fill=color, tags=(tag, "control"))
        if cmd:
            self.canvas.tag_bind(tag, "<Button-1>", lambda e: cmd())

    def button(self, x, y, w, h, label, color, fill):
        tag = f"btn_{label}_{x}_{y}"
        self.canvas.create_rectangle(x+3, y+3, x+w+3, y+h+3, fill="#02020a", outline="#0a0a18", tags=tag)
        self.canvas.create_rectangle(x, y, x+w, y+h, fill=fill, outline=color, width=2, tags=tag)
        self.canvas.create_rectangle(x+3, y+3, x+w-3, y+h-3, outline=color, width=1, tags=tag)
        self.canvas.create_text(x+w/2, y+h/2, text=label, font=("Consolas", 13, "bold"), fill=TEXT, tags=tag)
        self.canvas.tag_bind(tag, "<Button-1>", lambda e, l=label: self.press(l))

    def mouse_down(self, event):
        current = self.canvas.gettags("current")
        if event.y <= 66 and "control" not in current:
            self.dragging = True
            self.drag_x = event.x
            self.drag_y = event.y

    def mouse_drag(self, event):
        if self.dragging:
            x = self.root.winfo_pointerx() - self.drag_x
            y = self.root.winfo_pointery() - self.drag_y
            self.root.geometry(f"+{x}+{y}")

    def mouse_up(self, event):
        self.dragging = False

    def minimize(self):
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(250, lambda: self.root.overrideredirect(True))

    def show(self, text):
        text = str(text)
        if len(text) > 14:
            text = text[:14]
        shown = text or "0"
        for item in (self.display, self.display_shadow1, self.display_shadow2):
            self.canvas.itemconfigure(item, text=shown)

    def press(self, label):
        try:
            if label == "EXIT":
                self.root.destroy(); return
            if label == "C":
                self.expr = ""; self.show("0"); return
            if label == "⌫":
                self.expr = self.expr[:-1]; self.show(self.expr); return
            if label in "0123456789.":
                self.expr += label; self.show(self.expr); return
            if label in ["+", "−", "×", "÷"]:
                op = {"−": "-", "×": "*", "÷": "/", "+": "+"}[label]
                if self.expr and self.expr[-1] not in "+-*/":
                    self.expr += op
                self.show(self.expr); return
            if label == "%":
                self.expr = self.clean(float(self.eval_expr()) / 100.0); self.show(self.expr); return
            if label == "±":
                self.expr = self.clean(-float(self.eval_expr() or 0)); self.show(self.expr); return
            if label == "√":
                self.expr = self.clean(math.sqrt(float(self.eval_expr() or 0))); self.show(self.expr); return
            if label == "x²":
                self.expr = self.clean(float(self.eval_expr() or 0) ** 2); self.show(self.expr); return
            if label == "1/x":
                self.expr = self.clean(1 / float(self.eval_expr() or 0)); self.show(self.expr); return
            if label == "=":
                self.expr = self.clean(self.eval_expr()); self.show(self.expr); return
        except Exception:
            self.expr = ""
            self.show("ERROR")

    def eval_expr(self):
        if not self.expr:
            return 0
        return eval(self.expr, {"__builtins__": {}}, {})

    def clean(self, value):
        try:
            f = float(value)
            if f.is_integer():
                return str(int(f))
            return ("%.10f" % f).rstrip("0").rstrip(".")
        except Exception:
            return str(value)

    def keypress(self, event):
        k = event.char
        if k in "0123456789.+-*/":
            maps = {"*": "×", "/": "÷", "-": "−"}
            self.press(maps.get(k, k))
        elif event.keysym in ("Return", "KP_Enter"):
            self.press("=")
        elif event.keysym == "BackSpace":
            self.press("⌫")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CyberpunkCalc().run()
