import ast
import operator as op

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


# =========================================================
# WINDOW
# =========================================================

Window.size = (380, 650)
Window.clearcolor = (0.969, 0.659, 0.784, 1)


# =========================================================
# COLORS
# =========================================================

BUTTON_PINK = (1.0, 0.882, 0.824, 1)
BUTTON_PRESS = (1.0, 0.765, 0.820, 1)
DARK_PINK = (0.851, 0.310, 0.529, 1)
TEXT_BROWN = (0.396, 0.125, 0.235, 1)
DISPLAY_BLUE = (0.788, 0.953, 0.969, 1)
WHITE = (1, 1, 1, 1)


# =========================================================
# SAFE CALCULATION
# =========================================================

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
}


def safe_calculate(expression):

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("−", "-")

    def calculate(node):

        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError

        if isinstance(node, ast.BinOp):

            if type(node.op) not in OPERATORS:
                raise ValueError

            left = calculate(node.left)
            right = calculate(node.right)

            return OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp):

            if isinstance(node.op, ast.USub):
                return -calculate(node.operand)

            if isinstance(node.op, ast.UAdd):
                return calculate(node.operand)

        raise ValueError

    tree = ast.parse(expression, mode="eval")

    return calculate(tree)


# =========================================================
# BUTTON
# =========================================================

class CalculatorButton(Button):

    def __init__(
        self,
        button_color=BUTTON_PINK,
        text_color=TEXT_BROWN,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.normal_color = button_color
        self.press_color = BUTTON_PRESS

        self.background_normal = ""
        self.background_down = ""

        self.background_color = button_color

        self.color = text_color

        self.font_size = dp(22)
        self.bold = True

        self.bind(
            pos=self.draw_button,
            size=self.draw_button
        )

    def draw_button(self, *args):

        self.canvas.before.clear()

        with self.canvas.before:

            Color(*self.background_color)

            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(13)]
            )

    def on_press(self):

        self.background_color = self.press_color
        self.draw_button()

    def on_release(self):

        self.background_color = self.normal_color
        self.draw_button()


# =========================================================
# CALCULATOR
# =========================================================

class PinkCalculator(App):

    def build(self):

        self.expression = ""

        # -------------------------------------------------
        # MAIN LAYOUT
        # -------------------------------------------------

        root = BoxLayout(
            orientation="vertical",
            padding=[
                dp(20),
                dp(20),
                dp(20),
                dp(18)
            ],
            spacing=dp(10)
        )

        # -------------------------------------------------
        # DISPLAY
        # -------------------------------------------------

        self.display = Label(
            text="0",
            font_size=dp(34),
            bold=True,
            color=TEXT_BROWN,
            halign="right",
            valign="middle",
            padding=[
                dp(15),
                dp(5)
            ],
            size_hint_y=None,
            height=dp(105)
        )

        with self.display.canvas.before:

            Color(*DISPLAY_BLUE)

            self.display_background = RoundedRectangle(
                pos=self.display.pos,
                size=self.display.size,
                radius=[dp(16)]
            )

        self.display.bind(
            pos=self.update_display_background,
            size=self.update_display_background
        )

        root.add_widget(self.display)

        # -------------------------------------------------
        # BUTTON AREA
        # -------------------------------------------------

        button_area = BoxLayout(
            orientation="vertical",
            spacing=dp(9)
        )

        # =================================================
        # ROW 1
        # C     %     ÷     ⌫
        # =================================================

        self.create_row(
            button_area,
            [
                ("C", self.clear),
                ("%", self.percentage),
                ("÷", self.operator),
                ("⌫", self.backspace)
            ]
        )

        # =================================================
        # ROW 2
        # 7     8     9     ×
        # =================================================

        self.create_row(
            button_area,
            [
                ("7", self.number),
                ("8", self.number),
                ("9", self.number),
                ("×", self.operator)
            ]
        )

        # =================================================
        # ROW 3
        # 4     5     6     −
        # =================================================

        self.create_row(
            button_area,
            [
                ("4", self.number),
                ("5", self.number),
                ("6", self.number),
                ("−", self.operator)
            ]
        )

        # =================================================
        # ROW 4
        # 1     2     3     +
        # =================================================

        self.create_row(
            button_area,
            [
                ("1", self.number),
                ("2", self.number),
                ("3", self.number),
                ("+", self.operator)
            ]
        )

        # =================================================
        # ROW 5
        # .     0     (     )
        # =================================================

        self.create_row(
            button_area,
            [
                (".", self.decimal),
                ("0", self.number),
                ("(", self.bracket),
                (")", self.bracket)
            ]
        )

        # =================================================
        # ROW 6
        #          =
        # =================================================

        equals_row = BoxLayout(
            orientation="horizontal",
            spacing=dp(9)
        )

        # Empty space on the left

        left_space = Label()
        left_space.size_hint_x = 1

        equals_row.add_widget(left_space)

        # Equals button

        equals = CalculatorButton(
            text="=",
            button_color=DARK_PINK,
            text_color=WHITE
        )

        equals.bind(
            on_release=lambda instance: self.equals()
        )

        # Make equals wider

        equals.size_hint_x = 2

        equals_row.add_widget(equals)

        # Empty space on the right

        right_space = Label()
        right_space.size_hint_x = 1

        equals_row.add_widget(right_space)

        button_area.add_widget(equals_row)

        # -------------------------------------------------
        # ADD BUTTON AREA
        # -------------------------------------------------

        root.add_widget(button_area)

        return root

    # =====================================================
    # DISPLAY BACKGROUND
    # =====================================================

    def update_display_background(self, *args):

        self.display_background.pos = self.display.pos
        self.display_background.size = self.display.size

    # =====================================================
    # CREATE ROW
    # =====================================================

    def create_row(self, parent, buttons):

        row = BoxLayout(
            orientation="horizontal",
            spacing=dp(9)
        )

        for text, function in buttons:

            button = CalculatorButton(
                text=text
            )

            button.bind(
                on_release=lambda instance,
                value=text,
                func=function: func(value)
            )

            row.add_widget(button)

        parent.add_widget(row)

    # =====================================================
    # NUMBER
    # =====================================================

    def number(self, value):

        if self.expression == "0":
            self.expression = ""

        self.expression += value

        self.update_display()

    # =====================================================
    # DECIMAL
    # =====================================================

    def decimal(self, value=None):

        if not self.expression:

            self.expression = "0."

        elif self.expression[-1] in "+−×÷(":

            self.expression += "0."

        else:

            current_number = ""

            for char in reversed(self.expression):

                if char in "+−×÷()":
                    break

                current_number = char + current_number

            if "." not in current_number:
                self.expression += "."

        self.update_display()

    # =====================================================
    # BRACKETS
    # =====================================================

    def bracket(self, value):

        if value == "(":

            # Add multiplication automatically when needed
            if self.expression and (
                self.expression[-1].isdigit()
                or self.expression[-1] == ")"
            ):
                self.expression += "×"

            self.expression += "("

        else:

            # Don't allow ) as the first character
            if not self.expression:
                return

            # Don't allow ) immediately after an operator or (
            if self.expression[-1] in "+−×÷(":
                return

            # Only add ) if there is an unmatched (
            if self.expression.count("(") > self.expression.count(")"):
                self.expression += ")"

        self.update_display()

    # =====================================================
    # OPERATOR
    # =====================================================

    def operator(self, value):

        if not self.expression:
            return

        if self.expression[-1] in "+−×÷":

            self.expression = self.expression[:-1]

        # Don't put operator immediately after (
        if self.expression[-1] == "(":
            return

        self.expression += value

        self.update_display()

    # =====================================================
    # PERCENTAGE
    # =====================================================

    def percentage(self, value=None):

        if not self.expression:
            return

        try:

            result = safe_calculate(
                self.expression
            )

            result = result / 100

            self.expression = self.format_number(
                result
            )

            self.update_display()

        except:

            self.expression = ""
            self.display.text = "Error"

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self, value=None):

        self.expression = ""

        self.display.text = "0"

    # =====================================================
    # BACKSPACE
    # =====================================================

    def backspace(self, value=None):

        if self.expression:

            self.expression = self.expression[:-1]

        self.update_display()

    # =====================================================
    # EQUALS
    # =====================================================

    def equals(self):

        if not self.expression:
            return

        # Incomplete expression
        if self.expression[-1] in "+−×÷(":

            self.display.text = "Error"
            return

        # Check brackets
        if self.expression.count("(") != self.expression.count(")"):

            self.display.text = "Error"
            return

        try:

            result = safe_calculate(
                self.expression
            )

            self.expression = self.format_number(
                result
            )

            self.update_display()

        except ZeroDivisionError:

            self.expression = ""
            self.display.text = "Cannot divide by zero"

        except:

            self.expression = ""
            self.display.text = "Error"

    # =====================================================
    # FORMAT NUMBER
    # =====================================================

    def format_number(self, number):

        if isinstance(number, float):

            if number.is_integer():

                return str(int(number))

            return str(round(number, 10))

        return str(number)

    # =====================================================
    # UPDATE DISPLAY
    # =====================================================

    def update_display(self):

        if self.expression:

            self.display.text = self.expression

        else:

            self.display.text = "0"


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    PinkCalculator().run()