import sys
from os import execl
from random import randint

from PyQt5.QtCore import Qt, QRect, QPoint, QSize, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QSplashScreen, QLabel


class TribeBubbles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tribe Bubbles')
        self.setGeometry(400, 150, 650, 650)
        self.multiplier = 1
        self.score = 0
        self.in_a_row = 1
        self.gameover = False

        self.timer = QTimer()
        self.time_int = 0
        self.timer.timeout.connect(self.time)
        self.timer.start(1000)

        self.timerlabel = QLabel(self)
        self.timerlabel.setGeometry(40, 5, 200, 50)

        self.newgame = QPushButton("New Game!", self)
        self.newgame.setGeometry(45, 610, 150, 30)
        self.newgame.clicked.connect(lambda restart: execl(sys.executable, sys.executable, *sys.argv))

        self.squares = [[[] for q in range(8)] for r in range(8)]
        self.circlepoints = [[[] for o in range(8)] for p in range(8)]
        self.circles = [['_' for o in range(8)] for p in range(8)]
        self.blockers = [[[] for s in range(8)] for t in range(8)]
        self.blocker_list = []
        self.combined_list = [[[] for q in range(8)] for r in range(8)]

        for i in range(8):
            for j in range(8):
                x = 40 + 70 * i
                y = 40 + 70 * j
                self.squares[i][j] = QRect(QPoint(x, y), QSize(70, 70))

        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        grid_pen = QPen(Qt.black, 7)
        grid_brush = QBrush(QColor(233, 194, 240), Qt.SolidPattern)
        qp.setPen(grid_pen)
        qp.setBrush(grid_brush)

        for row in self.squares:
            for value in row:
                qp.drawRect(value)
                circle = self.circlepoints[row.index(value)][self.squares.index(row)]
                blocker = self.blockers[row.index(value)][self.squares.index(row)]

                if isinstance(circle, QPoint) and not isinstance(blocker,
                                                                 QRect):  # draws the circle and removes if blocked
                    qp.setPen(QPen(QColor(26, 15, 110), 7))
                    qp.drawEllipse(circle, 25, 25)
                    qp.setPen(grid_pen)

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
        gridy = (x - 40) // 70
        gridx = (y - 40) // 70

        for i in range(8):  # check that you cant click on a blocker and score
            for j in range(8):
                if self.circles[i][j] == 'O' and isinstance(self.blockers[i][j], QRect) or isinstance(
                        self.blockers[i][j], QRect) and isinstance(self.circlepoints[i][j], QPoint):
                    self.circles[i][j] = 'X'
                    self.circlepoints[i][j] = []

        while not 20 <= block_point.x() <= 580 and not 20 <= block_point.y() <= 580:  # makes sure the blocker in the grid
            ranx = randint(0, 7)
            rany = randint(0, 7)
            block_point = QPoint(70 * (ranx + 1) - 18, 70 * (rany + 1) - 18)

        if 40 <= x <= 610 and 40 <= y <= 610 and (gridx, gridy) not in self.blocker_list:
            for row in self.squares:
                for square in row:
                    if square.__contains__(QPoint(x, y)):
                        self.circlepoints[row.index(square)][self.squares.index(row)] = QPoint(square.center().x(),
                                                                                               square.center().y())  # adds a point for the circle
                        self.circles[row.index(square)][self.squares.index(row)] = 'O'

            self.blockers[rany][ranx] = QRect(block_point, QSize(45, 45))  # adds the blocker to the list
            self.blocker_list.append((rany, ranx))

            self.scoreCheck()

        self.update()

        for x in range(8):
            for y in range(8):
                pass
                if self.circles[x][y] != '_':
                    self.combined_list[x][y] = self.circles[x][y]
                elif isinstance(self.blockers[x][y], QRect):
                    self.combined_list[x][y] = 'X'
                else:
                    self.combined_list[x][y] = []

        if any([] in value for value in self.combined_list):
            self.gameover = False
        else:
            self.gameover = True

    def scoreCheck(self):
        coordList = []
        line = 0
        scored_hor = 0
        scored_vert = 0
        scored_diag1 = 0
        scored_diag2 = 0
        for r in range(8):  # horizontal scoring
            for c in range(8):
                row = r
                col = c
                start_r = r
                start_c = c
                number = 1
                while col + 1 < 8 and self.circles[row][col] == self.circles[row][col + 1] == 'O':
                    number += 1
                    col += 1

                if number >= 4:
                    line += 1
                    scored_hor = 1
                    for i1 in range(number):
                        coordList.append((start_r, start_c + i1))

        for r in range(8):  # vertical scoring
            for c in range(8):
                row = r
                col = c
                start_r = r
                start_c = c
                number = 1
                while row + 1 < 8 and self.circles[row][col] == self.circles[row + 1][col] == 'O':
                    number += 1
                    row += 1
                if number >= 4:
                    scored_vert = 1
                    line += 1
                    for i2 in range(number):
                        coordList.append((start_r + i2, start_c))

        for r in range(8):  # diagonal right down scoring
            for c in range(8):
                row = r
                col = c
                start_r = r
                start_c = c
                number = 1
                while row + 1 < 8 and col + 1 < 8 and self.circles[row][col] == self.circles[row + 1][col + 1] == 'O':
                    number += 1
                    row += 1
                    col += 1
                if number >= 4:
                    line += 1
                    scored_diag1 = 1
                    for i3 in range(number):
                        coordList.append((start_r + i3, start_c + i3))

        for r in range(8):  # diagonal right up scoring
            for c in range(8):
                row = r
                col = c
                start_r = r
                start_c = c
                number = 1
                while row - 1 < 8 and col + 1 < 8 and self.circles[row][col] == self.circles[row - 1][col + 1] == 'O':
                    number += 1
                    row -= 1
                    col += 1
                if number >= 4:
                    scored_diag2 = 1
                    line += 1
                    for i4 in range(number):
                        coordList.append((start_r - i4, start_c + i4))

        coordList = list(set(coordList))
        bubble_count = len(coordList)
        self.multiplier = scored_vert + scored_hor + scored_diag1 + scored_diag2
        if self.multiplier == 0:
            self.multiplier = 1
        self.score += bubble_count * self.multiplier
        for j, k in coordList:
            self.circles[j][k] = '_'
            self.circlepoints[j][k] = []

    def time(self):
        if self.gameover:
            self.timer.stop()
        else:
            self.time_int += 1

        self.timerlabel.setText("Time: " + str(self.time_int))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pixmap = QPixmap('Tribe_Bubbles.jpg')
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()
    window = QMainWindow()
    splash.finish(window)
    ex = TribeBubbles()
    sys.exit(app.exec_())
