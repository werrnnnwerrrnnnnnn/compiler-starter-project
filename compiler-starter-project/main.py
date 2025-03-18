import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLCDNumber

from components.lexica import MyLexer
from components.parsers import MyParser
from components.memory import Memory

class MainWindow(QMainWindow):

    # Do this for intellisense
    button_1: QPushButton        # 1
    button_2: QPushButton        # 2
    button_3: QPushButton        # 3
    button_4: QPushButton        # 4
    button_5: QPushButton        # 5
    button_6: QPushButton        # 6
    button_7: QPushButton        # 7
    button_8: QPushButton        # 8
    button_9: QPushButton        # 9
    button_plus: QPushButton     # +
    button_star: QPushButton     # *
    button_equal: QPushButton    # =
    button_clear: QPushButton    # Clear

    input_prefix: QLineEdit      # Prefix input
    output_infix: QLineEdit      # Infix output
    # output_postfix: QLineEdit    # Postfix output
    output_answer: QLCDNumber    # Answer output

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./components/main.ui", self)

        #### Binding buttons to functions ####
        self.button_0.clicked.connect(lambda: self.push("0"))   
        self.button_1.clicked.connect(lambda: self.push("1"))
        self.button_2.clicked.connect(lambda: self.push("2"))
        self.button_3.clicked.connect(lambda: self.push("3"))
        self.button_4.clicked.connect(lambda: self.push("4"))
        self.button_5.clicked.connect(lambda: self.push("5"))
        self.button_6.clicked.connect(lambda: self.push("6"))
        self.button_7.clicked.connect(lambda: self.push("7"))
        self.button_8.clicked.connect(lambda: self.push("8"))
        self.button_9.clicked.connect(lambda: self.push("9"))

        self.button_plus.clicked.connect(lambda: self.push("+"))
        self.button_star.clicked.connect(lambda: self.push("*"))
        self.button_equal.clicked.connect(self.push_equal)
        self.button_clear.clicked.connect(self.clear)

    def push(self, text: str):
        """Append text to the prefix input field."""
        current_text: str = self.input_prefix.text()
        
        # Only add spaces for operators, not numbers
        if text in ["+", "-", "*", "/"]:
            self.input_prefix.setText(f"{current_text} {text} ")  # Space around operators
        else:
            self.input_prefix.setText(f"{current_text}{text}")    # No space for numbers
    
    def clear(self):
        """Clear all input and output fields."""
        self.input_prefix.setText("")       # Clear prefix input
        self.output_answer.display(0)       # Reset answer display
        self.output_infix.setText("")       # Clear infix output
        # self.output_postfix.setText("")     # Clear postfix output

    def push_equal(self):
        print("\n========================================================================")
        print("📍 Calculating from Prefix Input...")

        lexer = MyLexer()
        parser = MyParser()
        memory = Memory()

        input_text = self.input_prefix.text().strip()

        # ✅ Ensure prefix input is properly formatted
        tokens = input_text.split()
        if len(tokens) < 3:
            print(f"❌ ERROR: Prefix expression is too short: {input_text}")
            self.output_infix.setText("Invalid Prefix Input")
            # self.output_postfix.setText("")
            self.output_answer.display("0")
            return

        print(f"🟠 Checking input prefix: {tokens}")

        try:
            # Convert prefix to infix and postfix
            infix_expr = parser.prefix_to_infix(input_text)
            # postfix_expr = parser.prefix_to_postfix(input_text)

            # Debugging
            print(f"✅ Prefix Input: {input_text}")
            print(f"✅ Converted Infix: {infix_expr}")
            # print(f"✅ Converted Postfix: {postfix_expr}")

            # Evaluate the infix expression
            result = parser.parse(lexer.tokenize(infix_expr))

            print(f"✅ Result: {result}\n")

            # Display in UI
            self.output_answer.display(result)       # Show the final answer
            self.output_infix.setText(infix_expr)   # Show infix expression
            # self.output_postfix.setText(postfix_expr)  # Show postfix expression

            print(memory)  # Debugging memory

        except ValueError as e:
            print(f"❌ ERROR: {e}")
            self.output_infix.setText("Invalid Prefix Input")
            # self.output_postfix.setText("")
            self.output_answer.display("0")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()