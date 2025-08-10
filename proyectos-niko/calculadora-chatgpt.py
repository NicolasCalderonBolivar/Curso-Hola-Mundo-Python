import customtkinter as ctk
import ast, operator as op
import time, threading
import tkinter as tk

# --- Operadores seguros ---
operators = {
    ast.Add: ("+", op.add),
    ast.Sub: ("-", op.sub),
    ast.Mult: ("×", op.mul),
    ast.Div: ("÷", op.truediv),
    ast.Pow: ("^", op.pow),
    ast.Mod: ("mod", op.mod),
    ast.UAdd: ("+", op.pos),
    ast.USub: ("-", op.neg),
}


# --- Evaluador seguro y explicador ---
def safe_eval_with_steps(expr):
    node = ast.parse(expr, mode="eval")
    steps = []
    result = _eval_with_steps(node.body, steps)
    return result, steps


def _eval_with_steps(node, steps):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval_with_steps(node.left, steps)
        right = _eval_with_steps(node.right, steps)
        op_symbol, func = operators[type(node.op)]
        step_str = f"{left} {op_symbol} {right} = {func(left, right)}"
        steps.append(step_str)
        return func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_with_steps(node.operand, steps)
        op_symbol, func = operators[type(node.op)]
        step_str = f"{op_symbol}{operand} = {func(operand)}"
        steps.append(step_str)
        return func(operand)
    raise TypeError("Operación no permitida")


# --- Animación ---
def flash_button(btn):
    original_color = btn.cget("fg_color")
    btn.configure(fg_color="#00bfff")
    time.sleep(0.15)
    btn.configure(fg_color=original_color)


# --- Interfaz principal ---
def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Calculadora Educativa")
    root.geometry("340x480")
    root.resizable(False, False)

    display = ctk.CTkEntry(
        root, font=("Helvetica", 28), justify="right", corner_radius=8
    )
    display.grid(row=0, column=0, columnspan=4, padx=10, pady=15, sticky="we")

    def append_char(c):
        display.insert("end", c)

    def clear_all():
        display.delete(0, "end")

    def backspace():
        s = display.get()
        if s:
            display.delete(0, "end")
            display.insert(0, s[:-1])

    def calculate():
        try:
            expr = display.get()
            result, _ = safe_eval_with_steps(expr)
            clear_all()
            display.insert(0, result)
        except Exception:
            clear_all()
            display.insert(0, "Error")

    def explain():
        try:
            expr = display.get()
            result, steps = safe_eval_with_steps(expr)
            show_explanation(expr, steps, result)
        except Exception:
            show_explanation(expr, ["Error al interpretar la operación"], None)

    def show_explanation(expr, steps, result):
        top = ctk.CTkToplevel(root)
        top.title("Explicación paso a paso")
        top.geometry("350x400")
        top.resizable(False, False)

        title = ctk.CTkLabel(
            top, text="🧮 Cómo resolvemos tu operación", font=("Helvetica", 16, "bold")
        )
        title.pack(pady=10)

        op_label = ctk.CTkLabel(top, text=f"Operación: {expr}", font=("Helvetica", 14))
        op_label.pack(pady=5)

        steps_frame = ctk.CTkFrame(top)
        steps_frame.pack(pady=5, padx=10, fill="both", expand=True)

        if steps:
            for step in steps:
                lbl = ctk.CTkLabel(
                    steps_frame, text=step, font=("Helvetica", 13), anchor="w"
                )
                lbl.pack(anchor="w", pady=2)
        else:
            ctk.CTkLabel(
                steps_frame, text="No hay pasos que mostrar", font=("Helvetica", 13)
            ).pack()

        if result is not None:
            ctk.CTkLabel(
                top,
                text=f"✅ Resultado final: {result}",
                font=("Helvetica", 14, "bold"),
                text_color="#00ff88",
            ).pack(pady=10)

        # Ejemplo visual simple
        if (
            result is not None
            and isinstance(result, (int, float))
            and result <= 10
            and result >= 0
        ):
            visual = "🍎" * int(result)
            ctk.CTkLabel(top, text=f"Visual: {visual}", font=("Helvetica", 20)).pack(
                pady=5
            )

    def toggle_theme():
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    # Botones numéricos y operaciones
    buttons = [
        ("7", 1, 0),
        ("8", 1, 1),
        ("9", 1, 2),
        ("/", 1, 3),
        ("4", 2, 0),
        ("5", 2, 1),
        ("6", 2, 2),
        ("*", 2, 3),
        ("1", 3, 0),
        ("2", 3, 1),
        ("3", 3, 2),
        ("-", 3, 3),
        ("0", 4, 0),
        (".", 4, 1),
        ("=", 4, 2),
        ("+", 4, 3),
    ]

    def create_btn(text, r, c, cmd=None, color="#333333"):
        btn = ctk.CTkButton(
            root,
            text=text,
            width=60,
            height=60,
            corner_radius=10,
            fg_color=color,
            hover_color="#666666",
            font=("Helvetica", 18),
            command=lambda: [
                threading.Thread(target=flash_button, args=(btn,)).start(),
                cmd() if cmd else append_char(text),
            ],
        )
        btn.grid(row=r, column=c, padx=5, pady=5)
        return btn

    for text, r, c in buttons:
        if text == "=":
            create_btn(text, r, c, calculate, "#00bfff")
        elif text in ["+", "-", "*", "/"]:
            create_btn(text, r, c, None, "#444444")
        else:
            create_btn(text, r, c)

    # Botones extra
    clear_btn = create_btn("C", 5, 0, clear_all, "#555555")
    back_btn = create_btn("⌫", 5, 1, backspace, "#555555")
    lpar = create_btn("(", 5, 2, lambda: append_char("("), "#555555")
    rpar = create_btn(")", 5, 3, lambda: append_char(")"), "#555555")

    explain_btn = ctk.CTkButton(
        root,
        text="📖 Explicar",
        width=120,
        height=40,
        fg_color="#ffaa00",
        font=("Helvetica", 14),
        command=explain,
    )
    explain_btn.grid(row=6, column=0, columnspan=2, pady=10)

    theme_btn = ctk.CTkButton(
        root,
        text="🌗 Cambiar tema",
        width=120,
        height=40,
        fg_color="#888888",
        font=("Helvetica", 14),
        command=toggle_theme,
    )
    theme_btn.grid(row=6, column=2, columnspan=2, pady=10)

    # Atajos teclado
    def on_key(event):
        if event.char.isdigit() or event.char in "+-*/().%":
            append_char(event.char)
        elif event.keysym == "Return":
            calculate()
        elif event.keysym == "BackSpace":
            backspace()
        elif event.keysym.lower() == "c":
            clear_all()

    root.bind("<Key>", on_key)
    root.mainloop()


if __name__ == "__main__":
    main()
