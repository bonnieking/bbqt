import sys
from PyQt4.QtGui import QApplication, QTextEdit, QPainter, QWidget

class MyTextEdit(QWidget):
    """A TextEdit widget derived from QTextEdit and implementing its
       own paintEvent"""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawLine(0, 10, 10, 10)
        QWidget.paintEvent(self, event)

app = QApplication(sys.argv)
textEdit = MyTextEdit()
textEdit.show()

sys.exit(app.exec_())
