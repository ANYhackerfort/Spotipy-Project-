import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from button_holder import ButtonHolder

app = QApplication(sys.argv)

window = ButtonHolder()
window.show() 

app.exec() 
