import tkinter as tk
import re


# =========================================================
# WINDOW
# =========================================================

window = tk.Tk()
window.title("Pink Calculator")
window.geometry("380x650")
window.configure(bg="#F7A8C8")
window.resizable(False, False)


# =========================================================
# COLORS
# =========================================================

PINK_BODY = "#F47EAA"
PINK_DARK = "#D94F87"

BUTTON = "#FFE1D2"
BUTTON_ACTIVE = "#FFC3D1"

BROWN = "#65203C"
DISPLAY = "#C9F3F7"
DISPLAY_BORDER = "#65203C"

WHITE = "#FFFFFF"


# =========================================================
# CALCULATOR
# =========================================================

expression = ""


# =========================================================
# CANVAS
# =========================================================

canvas = tk.Canvas(
    window,
    width=380,
    height=650,
    bg=PINK_BODY,
    highlightthickness=0
)

canvas.pack()


# =========================================================
# CALCULATOR BODY
# =========================================================

# Outer body
canvas.create_rectangle(
    15, 15,
    365, 635,
    fill=PINK_DARK,
    outline=BROWN,
    width=5
)

# Inner body
canvas.create_rectangle(
    25, 25,
    355, 625,
    fill=PINK_BODY,
    outline="#FFB6D0",
    width=3
)


# =========================================================
# TOP DECORATION
# =========================================================

canvas.create_rectangle(
    225, 42,
    335, 92,
    fill="#A77A89",
    outline=BROWN,
    width=3
)

# Decorative lines
for x in range(240, 335, 18):

    canvas.create_line(
        x, 44,
        x, 90,
        fill="#80606D",
        width=2
    )


# =========================================================
# DISPLAY FRAME
# =========================================================

canvas.create_rectangle(
    45, 120,
    335, 195,
    fill=BROWN,
    outline="#431326",
    width=3
)


# =========================================================
# DISPLAY
# =========================================================

display_box = canvas.create_rectangle(
    53, 128,
    327, 187,
    fill=DISPLAY,
    outline="#9FE0E7",
    width=3
)


display_text = canvas.create_text(
    315,
    158,
    text="0",
    fill=BROWN,
    font=("Courier New", 30, "bold"),
    anchor="e"
)


# =========================================================
# DISPLAY UPDATE
# =========================================================

def update_display():

    if expression:
        text = expression
    else:
        text = "0"

    # Automatically reduce font size
    length = len(text)

    if length <= 10:
        size = 30
    elif length <= 15:
        size = 25
    elif length <= 20:
        size = 21
    else:
        size = 17

    canvas.itemconfig(
        display_text,
        text=text,
        font=("Courier New", size, "bold")
    )


# =========================================================
# CALCULATION
# =========================================================

def calculate_expression(exp):

    if not exp:
        return None

    try:

        clean = exp.replace("×", "*")
        clean = clean.replace("÷", "/")
        clean = clean.replace("−", "-")

        # Percentage
        clean = re.sub(
            r'(\d+(?:\.\d+)?)%',
            r'(\1/100)',
            clean
        )

        # Allow only calculator characters
        if not re.fullmatch(
            r'[0-9+\-*/().%\s]+',
            clean
        ):
            return None

        result = eval(
            clean,
            {"__builtins__": {}}
        )

        if result == int(result):
            return str(int(result))

        return str(round(result, 10))

    except:
        return None


# =========================================================
# NUMBER
# =========================================================

def number_click(number):

    global expression

    if expression == "0":
        expression = number

    else:
        expression += number

    update_display()


# =========================================================
# DECIMAL
# =========================================================

def decimal_click():

    global expression

    parts = re.split(
        r'[+\-×÷]',
        expression
    )

    current_number = parts[-1]

    if "." in current_number:
        return

    if not expression:
        expression = "0."

    elif expression[-1] in "+-×÷":
        expression += "0."

    else:
        expression += "."

    update_display()


# =========================================================
# OPERATOR
# =========================================================

def operator_click(operator):

    global expression

    if not expression:
        return

    # Replace previous operator
    if expression[-1] in "+-×÷":

        expression = expression[:-1]

    expression += operator

    update_display()


# =========================================================
# PERCENTAGE
# =========================================================

def percentage():

    global expression

    if expression and expression[-1].isdigit():

        expression += "%"

    update_display()


# =========================================================
# CLEAR
# =========================================================

def clear():

    global expression

    expression = ""

    flash_display()

    update_display()


# =========================================================
# BACKSPACE
# =========================================================

def backspace():

    global expression

    if expression:

        expression = expression[:-1]

    update_display()


# =========================================================
# EQUAL
# =========================================================

def equals():

    global expression

    result = calculate_expression(expression)

    if result is not None:

        expression = result

        flash_display()

        update_display()


# =========================================================
# DISPLAY ANIMATION
# =========================================================

def flash_display():

    canvas.itemconfig(
        display_box,
        fill="#FFFFFF"
    )

    window.after(
        120,
        lambda: canvas.itemconfig(
            display_box,
            fill=DISPLAY
        )
    )


# =========================================================
# BUTTON ANIMATION
# =========================================================

def button_animation(button):

    canvas.itemconfig(
        button,
        fill=BUTTON_ACTIVE
    )

    window.after(
        100,
        lambda: canvas.itemconfig(
            button,
            fill=BUTTON
        )
    )


# =========================================================
# NORMAL BUTTON
# =========================================================

def create_button(
    x,
    y,
    text,
    command,
    width=62,
    height=52
):

    # Shadow
    shadow = canvas.create_rectangle(
        x + 3,
        y + 4,
        x + width + 3,
        y + height + 4,
        fill=BROWN,
        outline=BROWN
    )

    # Button
    button = canvas.create_rectangle(
        x,
        y,
        x + width,
        y + height,
        fill=BUTTON,
        outline=BROWN,
        width=4
    )

    # Text
    label = canvas.create_text(
        x + width / 2,
        y + height / 2,
        text=text,
        fill=BROWN,
        font=("Arial", 22, "bold")
    )

    def click(event):

        button_animation(button)
        command()

    canvas.tag_bind(
        button,
        "<Button-1>",
        click
    )

    canvas.tag_bind(
        label,
        "<Button-1>",
        click
    )


# =========================================================
# WIDE BUTTON
# =========================================================

def create_wide_button(
    x,
    y,
    text,
    command,
    width,
    height
):

    shadow = canvas.create_rectangle(
        x + 3,
        y + 4,
        x + width + 3,
        y + height + 4,
        fill=BROWN,
        outline=BROWN
    )

    button = canvas.create_rectangle(
        x,
        y,
        x + width,
        y + height,
        fill=BUTTON,
        outline=BROWN,
        width=4
    )

    label = canvas.create_text(
        x + width / 2,
        y + height / 2,
        text=text,
        fill=BROWN,
        font=("Arial", 22, "bold")
    )

    def click(event):

        button_animation(button)
        command()

    canvas.tag_bind(
        button,
        "<Button-1>",
        click
    )

    canvas.tag_bind(
        label,
        "<Button-1>",
        click
    )


# =========================================================
# BUTTON LAYOUT
# =========================================================

X1 = 45
X2 = 120
X3 = 195
X4 = 270

Y1 = 225
Y2 = 285
Y3 = 345
Y4 = 405
Y5 = 465

W = 62
H = 52


# =========================================================
# ROW 1
# C     %     ÷     ⌫
# =========================================================

create_button(
    X1, Y1,
    "C",
    clear
)

create_button(
    X2, Y1,
    "%",
    percentage
)

create_button(
    X3, Y1,
    "÷",
    lambda: operator_click("÷")
)

create_button(
    X4, Y1,
    "⌫",
    backspace
)


# =========================================================
# ROW 2
# 7     8     9     ×
# =========================================================

create_button(
    X1, Y2,
    "7",
    lambda: number_click("7")
)

create_button(
    X2, Y2,
    "8",
    lambda: number_click("8")
)

create_button(
    X3, Y2,
    "9",
    lambda: number_click("9")
)

create_button(
    X4, Y2,
    "×",
    lambda: operator_click("×")
)


# =========================================================
# ROW 3
# 4     5     6     -
# =========================================================

create_button(
    X1, Y3,
    "4",
    lambda: number_click("4")
)

create_button(
    X2, Y3,
    "5",
    lambda: number_click("5")
)

create_button(
    X3, Y3,
    "6",
    lambda: number_click("6")
)

create_button(
    X4, Y3,
    "−",
    lambda: operator_click("−")
)


# =========================================================
# ROW 4
# 1     2     3     +
# =========================================================

create_button(
    X1, Y4,
    "1",
    lambda: number_click("1")
)

create_button(
    X2, Y4,
    "2",
    lambda: number_click("2")
)

create_button(
    X3, Y4,
    "3",
    lambda: number_click("3")
)

create_button(
    X4, Y4,
    "+",
    lambda: operator_click("+")
)


# =========================================================
# ROW 5
# .     0           =
# =========================================================

create_button(
    X1, Y5,
    ".",
    decimal_click
)


# Wide 0
create_wide_button(
    X2,
    Y5,
    "0",
    lambda: number_click("0"),
    137,
    H
)


# Equals
create_button(
    X4, Y5,
    "=",
    equals
)


# =========================================================
# KEYBOARD SUPPORT
# =========================================================

def keyboard(event):

    key = event.keysym

    if event.char.isdigit():

        number_click(event.char)

    elif event.char == ".":

        decimal_click()

    elif event.char == "+":

        operator_click("+")

    elif event.char == "-":

        operator_click("−")

    elif event.char == "*":

        operator_click("×")

    elif event.char == "/":

        operator_click("÷")

    elif event.char == "%":

        percentage()

    elif key == "BackSpace":

        backspace()

    elif key == "Escape":

        clear()

    elif key == "Return":

        equals()


window.bind("<Key>", keyboard)


# =========================================================
# START
# =========================================================

update_display()

window.mainloop()