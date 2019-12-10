import sys
from time import time
from os import execl
from random import randint

from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QSplashScreen


cell_size = 70


class TribeBubbles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tribe Bubbles')
        self.setGeometry(400, 150, 650, 650)
        self.multiplier = 1
        self.score = 0
        self.in_a_row = 1
        print('\n' * 10)
        self.newgame = QPushButton("New Game!", self)
        self.newgame.setGeometry(45, 610, 150, 30)
        self.newgame.clicked.connect(lambda restart: execl(sys.executable, sys.executable, *sys.argv))

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

            # self.blockers[rany][ranx] = QRect(block_point, QSize(45, 45))  # adds the blocker to the list

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
        diagonal_scored = False

        for row in range(len(self.circles)):  # Checks horizontal scoring
            rowstring = ''.join(self.circles[row])
            nO = 8  # number of Os in a row
            while nO >= 4:
                if 'O' * nO in rowstring:
                    first = rowstring.index('O')
                    last = rowstring.rindex('OOO') + 2
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
                    last = col_string.rindex('OOO') + 2
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

        for x in range(8):  # diagonal sloping downward
            for y in range(8):
                try:
                    if self.circles[x][y] == 'O' == self.circles[x + 1][y + 1] == self.circles[x + 2][y + 2] == \
                            self.circles[x + 3][y + 3]:

                        for i in range(4):
                            self.circles[x + i][y + i] = '_'

                        if to_score == 0:
                            to_score += 4
                        elif to_score > 0:
                            to_score += 3
                        diagonal_scored = True

                        if self.circles[x + 4][y + 4] == 'O':
                            self.circles[x + 4][y + 4] = '_'
                            to_score += 1

                            if self.circles[x + 5][y + 5] == 'O':
                                self.circles[x + 5][y + 5] = '_'
                                to_score += 1

                                if self.circles[x + 6][y + 6] == 'O':
                                    self.circles[x + 6][y + 6] = '_'
                                    to_score += 1

                                    break
                                break
                            break
                        break

                except IndexError:
                    continue

        # Adding the  score with the multiplier in mind
        print(vertical_scored, horizontal_scored, diagonal_scored)
        if vertical_scored and horizontal_scored and diagonal_scored:
            print("three scored")
            to_score *= 3 * self.in_a_row
            self.score += to_score
            self.multiplier = 3 * self.in_a_row
            self.in_a_row += 1

        elif vertical_scored and horizontal_scored:
            print("two scored")
            to_score *= 2 * self.in_a_row
            self.score += to_score
            self.multiplier = 2 * self.in_a_row
            self.in_a_row += 1

        elif vertical_scored and diagonal_scored:
            print("two scored")
            to_score *= 2 * self.in_a_row
            self.score += to_score
            self.multiplier = 2 * self.in_a_row
            self.in_a_row += 1

        elif diagonal_scored and horizontal_scored:
            print("two scored")
            to_score *= 2 * self.in_a_row
            self.score += to_score
            self.multiplier = 2 * self.in_a_row
            self.in_a_row += 1

        elif diagonal_scored or horizontal_scored or vertical_scored:
            print('one scored')
            self.score += to_score
            self.multiplier = 1
            self.in_a_row = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pixmap = QPixmap('Tribe_Bubbles.jpg')
    splash = QSplashScreen(pixmap)
    splash.show()
    for i in range(1, 45):
        t = time()
        while time() < t + 0.1:
            app.processEvents()

    window = QMainWindow()
    splash.finish(window)
    ex = TribeBubbles()
    sys.exit(app.exec_())
