from pickle import TRUE
import sys
from PySide6.QtWidgets import QMainWindow, QPushButton
from PySide6.QtGui import QIcon

class ButtonHolder(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Holder APP")
        button = QPushButton("Press Me!")
        icon = QIcon.fromTheme("dialog-question")
        button.setIcon(icon)
        self.setCentralWidget(button)
        button.setCheckable(True)

        def button_clicked(data):
            print("f", data)
            
        button.clicked.connect(button_clicked)

