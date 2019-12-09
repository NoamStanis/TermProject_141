import sys
from random import randint

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
        self.score = 0
        self.in_a_row = 1

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
        gridx = (x - 40) // 70
        gridy = (y - 40) // 70

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

            self.blockers[rany][ranx] = QRect(block_point, QSize(45, 45))  # adds the blocker to the list

            self.scoreCheck()

            for i in range(8):  # stops clicks on blockers
                for j in range(8):
                    if self.circles[i][j] != 'O':
                        self.circlepoints[i][j] = []
                    if isinstance(self.blockers[i][j], QRect):
                        self.circles[i][j] = '_'
                        self.circlepoints[i][j] = []

        self.update()

    def scoreCheck(self):
        """
        Checks if a scoring move has been completed with the currently placed bubbles and blockers.
        """""
        to_score = 0
        vertcircles = list(map(list, zip(*self.circles)))
        horizontal_scored = False
        vertical_scored = False

        for row in range(len(self.circles)):  # Checks horizontal scoring
            rowstring = ''.join(self.circles[row])
            nO = 8  # number of Os in a row
            while nO >= 4:
                if 'O' * nO in rowstring:
                    first = rowstring.index('O')
                    last = rowstring.rindex('O')
                    for j in range(first, last + 1):
                        self.circles[row][j] = '_'
                    if to_score == 0:
                        to_score += nO
                    elif to_score > 0:
                        to_score += nO - 1
                    horizontal_scored = True
                    break
                if nO == 4:
                    break
                else:
                    nO -= 1

        for col in range(len(vertcircles)):  # vertical score check
            col_string = ''.join(vertcircles[col])
            numberOs = 8  # similar to nO above
            while numberOs >= 4:
                if 'O' * numberOs in col_string:
                    first = col_string.index('O')
                    last = col_string.rindex('O')
                    for i in range(first, last + 1):
                        self.circles[i][col] = '_'
                    if to_score == 0:
                        to_score += numberOs
                    elif to_score > 0:
                        to_score += numberOs - 1
                    vertical_scored = True

                    break
                if numberOs == 4:
                    break
                else:
                    numberOs -= 1

        if vertical_scored and horizontal_scored:
            to_score *= 2 * self.in_a_row
            self.score += to_score
            self.multiplier = 2 * self.in_a_row
            self.in_a_row += 1

        else:
            self.score += to_score
            self.multiplier = 1
            self.in_a_row = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ex = TribeBubbles()
    sys.exit(app.exec_())
