from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

import sys

app = QApplication(sys.argv)

window = QPushButton("push me")
window.show()

app.exec_()
