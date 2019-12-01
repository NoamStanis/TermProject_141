import sys

from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

cell_size = 70


class TribeBubbles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tribe Bubbles')
        self.setGeometry(400, 150, 650, 650)
        self.multiplier = 1

        self.squares = [[[] for q in range(8)] for r in range(8)]
        self.shapes = [[[] for o in range(8)] for p in range(8)]
        for i in range(8):
            for j in range(8):
                x = 40 + cell_size * i
                y = 40 + cell_size * j
                self.squares[i][j] = QRect(QPoint(x, y), QSize(cell_size, cell_size))

        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        grid_pen = QPen(Qt.black, 7)
        grid_brush = QBrush(QColor(120, 204, 141), Qt.SolidPattern)
        qp.setPen(grid_pen)
        qp.setBrush(grid_brush)

        for col in self.squares:
            for value in col:
                qp.drawRect(value)
                if type(self.shapes[self.squares.index(col)][col.index(value)]) == QPoint:
                    qp.drawEllipse(self.shapes[self.squares.index(col)][col.index(value)], 25, 25)

        qp.drawText(250, 620, "Score:\t " + "x" + str(self.multiplier))

        qp.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        for col in self.squares:
            for square in col:
                if square.__contains__(QPoint(x, y)):
                    self.shapes[self.squares.index(col)][col.index(square)] = QPoint(square.center().x(), square.center().y())
                    print(self.squares.index(col), col.index(square))
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ex = TribeBubbles()
    sys.exit(app.exec_())
