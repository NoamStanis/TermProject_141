import sys

from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

cell_size = 70


class TribeBubbles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tribe Bubbles')
        self.setGeometry(400, 150, 600, 600)
        self.squares = [[[] for q in range(8)] for r in range(8)]
        for i in range(8):
            for j in range(8):
                x = 20 + cell_size * i
                y = 20 + cell_size * j
                self.squares[i][j] = QRect(QPoint(x, y), QSize(cell_size, cell_size))

        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        grid_pen = QPen(Qt.black, 7)
        grid_brush = QBrush(QColor(120, 204, 141), Qt.SolidPattern)
        qp.setPen(grid_pen)
        qp.setBrush(grid_brush)

        for row in self.squares:
            for value in row:
                qp.drawRect(value)

        qp.end()

    def MousePressEvent(self, event):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ex = TribeBubbles()
    sys.exit(app.exec_())
