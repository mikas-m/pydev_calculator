import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import math, re



class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_file = QFile("calculator.ui")
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.setFixedSize(400,300)
        self.setWindowTitle("Calculator")
        
        self.setCentralWidget(self.ui)
        self.ui.clear.clicked.connect(self.clear_text)
        self.ui.button_result.clicked.connect(self.result)


        numbers = list(range(10))
        for number in numbers:
            number_button_name = f"number_{number}"
            number_button = getattr(self.ui, number_button_name, None)
            if number_button:
                number_button.clicked.connect(lambda checked, num=number: self.number_clicked(num))

        operations_one = ["add", "subtract", "multiply", "divide"]
        for operation in operations_one:
            operation_button_name = f"operation_{operation}"
            operation_button = getattr(self.ui, operation_button_name, None)
            if operation_button:
                operation_button.clicked.connect(lambda checked, op_one=operation: self.operation_clicked_one(op_one))

        operations_two = ["sin", "cos", "tan", "cotangent"]
        for operation in operations_two:
            operation_button_name = f"operation_{operation}"
            operation_button = getattr(self.ui, operation_button_name, None)
            if operation_button:
                operation_button.clicked.connect(lambda checked, op_two=operation: self.operation_clicked_two(op_two))

    def clear_text(self):
       self.ui.button_clicked.clear()

    def number_clicked(self, num):
        current_text = self.ui.button_clicked.text()
        self.ui.button_clicked.setText(current_text + str(num))
    
    def operation_clicked_one(self, op_one):
        current_text = self.ui.button_clicked.text()
        if op_one == "add":
            self.ui.button_clicked.setText(current_text + "+")
        if op_one == "subtract":    
            self.ui.button_clicked.setText(current_text + "-")
        if op_one == "multiply":
            self.ui.button_clicked.setText(current_text + "*")
        if op_one == "divide":
            self.ui.button_clicked.setText(current_text + "/")

    def operation_clicked_two(self, op_two):
        user_angle = self.ui.button_clicked.text()
        try:
            if op_two != "cotangent":
                operation = getattr(math, op_two)
                result = operation(math.radians(float(user_angle)))      
            else:
                tg = math.tan(math.radians(float(user_angle)))
                if tg == 0:
                    result = "Tg = 0"
                else:
                    result = 1/tg   
            self.ui.button_clicked.setText(str(result))
        except Exception as e:
            print(f"Error: {e}")
            self.ui.button_clicked.setText("Error")


    def result(self):
        current_text = self.ui.button_clicked.text()
        text_to_calculate = re.split(r"([*/+-])", current_text)

        i=0
        while i < len(text_to_calculate):
            if text_to_calculate[i] in "*/":
                num1 = float(text_to_calculate[i-1])
                num2 = float(text_to_calculate[i+1])
                
                if text_to_calculate[i] == "*":
                    result = float(num1*num2)
                elif text_to_calculate[i] == "/":
                    result = float(num1/num2) if num2 != 0 else "Err Div 0"

                text_to_calculate[i-1:i+2] = [str(result)]
                i -= 1
            else:
                i += 1

        i=0
        while i < len(text_to_calculate):
            if text_to_calculate[i] in "+-":
                num1 = float(text_to_calculate[i-1])
                num2 = float(text_to_calculate[i+1])
                
                if text_to_calculate[i] == "+":
                    result = float(num1+num2)
                elif text_to_calculate[i] == "-":
                    result = float(num1-num2)

                text_to_calculate[i-1:i+2] = [str(result)]
            else:
                i += 1
        
        self.ui.button_clicked.setText("".join(text_to_calculate))

def main():
    app = QApplication(sys.argv)
    window = Calculator()
    window.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
