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
        self.score = 0

        self.squares = [[[] for q in range(8)] for r in range(8)]
        self.circlepoints = [[[] for o in range(8)] for p in range(8)]
        self.circles = [['_' for o in range(8)] for p in range(8)]
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
                circle = self.circlepoints[row.index(value)][self.squares.index(row)]
                blocker = self.blockers[row.index(value)][self.squares.index(row)]

                if isinstance(circle, QPoint) and not isinstance(blocker,
                                                                 QRect):  # draws the circle and removes if blocked
                    qp.drawEllipse(circle, 25, 25)

                if type(blocker) == QRect:  # draws the blocker
                    qp.setPen(QPen(0))
                    qp.setBrush(QBrush(QColor(204, 156, 120), Qt.SolidPattern))
                    qp.drawRect(blocker)
                    qp.setPen(grid_pen)
                    qp.setBrush(grid_brush)

                if type(circle) == QPoint and type(
                        blocker) == QRect:  # removes circle from the circle list if blocker is placed in same location
                    circle = []

        qp.drawText(250, 620, "Score:" + str(self.score) + "\t" + "x" + str(self.multiplier))

        qp.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        block_point = QPoint()

        while not 20 <= block_point.x() <= 580 and not 20 <= block_point.y() <= 580:  # makes sure the blocker in the grid
            ranx = randint(0, 7)
            rany = randint(0, 7)
            block_point = QPoint(70 * (ranx + 1) - 18, 70 * (rany + 1) - 18)

        if 40 <= x <= 610 and 40 <= y <= 610:
            for r in self.blockers:
                for b in r:
                    if b.__contains__(QPoint(x, y)):
                        return

            for row in self.squares:
                for square in row:
                    if square.__contains__(QPoint(x, y)):
                        self.circlepoints[row.index(square)][self.squares.index(row)] = QPoint(square.center().x(),
                                                                                               square.center().y())  # adds a point for the circle
                        self.circles[row.index(square)][self.squares.index(row)] = 'O'
                        #  print(self.squares.index(col), col.index(square))

            self.blockers[rany][ranx] = QRect(block_point, QSize(45, 45))  # adds the blocker to the list

            # Check for scoring

            for row in self.circles:  # Checks horizontal scoring
                rowstring = ''.join(row)
                nO = 8
                while 4 <= nO <= 8:
                    if 'O' * nO in rowstring:
                        for i in range(len(row)):
                            try:
                                if row[i:i + nO] == ['O' for j in range(nO)] and not isinstance(
                                        self.blockers[self.circles.index(row)][i], QRect):
                                    row[i:i + nO] = ['_' for k in range(nO)]
                                    self.score += nO
                            except IndexError:
                                continue
                    if nO == 4:
                        break
                    else:
                        nO -= 1

            vertcircles = list(map(list, zip(*self.circles)))

            print("\ncircles")
            for row in self.circles:
                print(row)
            print("\ninverted circles")
            for c in vertcircles:
                print(c)

            for col in range(len(vertcircles)):  # vertical score check
                col_string = ''.join(vertcircles[col])
                numberOs = 8
                while numberOs >= 4:
                    if 'O' * numberOs in col_string:
                        first = col_string.index('O')
                        last = col_string.rindex('O')
                        for i in range(first, last+1):
                            self.circles[i][col] = '_'
                        self.score += numberOs
                        break
                    if numberOs == 4:
                        break
                    else:
                        numberOs -= 1

            for i in range(8):  # stops clicks on blockers
                for j in range(8):
                    if self.circles[i][j] != 'O':
                        self.circlepoints[i][j] = []
                    if isinstance(self.blockers[i][j], QRect):
                        self.circles[i][j] = '_'
                        self.circlepoints[i][j] = []

            # print("\nBlockers")
            # for r in self.blockers:
            #     print(r)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ex = TribeBubbles()
    sys.exit(app.exec_())
