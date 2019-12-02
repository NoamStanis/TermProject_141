import sys

from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from random import randint

cell_size = 70


class TribeBubbles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tribe Bubbles')
        self.setGeometry(400, 150, 650, 650)
        self.multiplier = 1

        self.squares = [[[] for q in range(8)] for r in range(8)]
        self.circles = [[[] for o in range(8)] for p in range(8)]
        self.blockers = [[[] for s in range(8)] for t in range(8)]

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

        for row in self.squares:
            for value in row:
                qp.drawRect(value)
                circle = self.circles[row.index(value)][self.squares.index(row)]
                blocker = self.blockers[row.index(value)][self.squares.index(row)]

                if isinstance(circle, QPoint) and not isinstance(blocker, QRect):  # draws the circle and removes if blocked
                    qp.drawEllipse(circle, 25, 25)

                if type(blocker) == QRect: # draws the blocker
                    qp.setPen(QPen(0))
                    qp.setBrush(QBrush(QColor(204, 156, 120), Qt.SolidPattern))
                    qp.drawRect(blocker)
                    qp.setPen(grid_pen)
                    qp.setBrush(grid_brush)

                if type(circle) == QPoint and type(blocker) == QRect:  # removes circle from the circle list if blocker is placed in same location
                    circle = []

        #print(self.circles)
        qp.drawText(250, 620, "Score:\t " + "x" + str(self.multiplier))

        qp.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        block_point = QPoint()

        while not 20 <= block_point.x() <= 580 and not 20 <= block_point.y() <= 580:  # makes sure the blocker in the grid
            ranx = randint(0, 7)
            rany = randint(0, 7)
            block_point = QPoint(70 * (ranx + 1) - 18, 70 * (rany + 1) - 18)

        for row in self.squares:
            for square in row:
                if square.__contains__(QPoint(x, y)):
                    self.circles[row.index(square)][self.squares.index(row)] = QPoint(square.center().x(), square.center().y())  # adds a point for the circle
                    #  print(self.squares.index(col), col.index(square))

        self.blockers[rany][ranx] = QRect(block_point, QSize(45, 45)) # adds the blocker to the list

        # Check for scoring
        score = False
        print("\nCircles")
        for row in self.circles:
            print(row)

        print("\nBlockers")
        for r in self.blockers:
            print(r)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ex = TribeBubbles()
    sys.exit(app.exec_())
