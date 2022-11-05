import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QPen

from model import State

WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400

class MainWindow(QMainWindow):

    def __init__(self, state: State) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setContentsMargins(0,0,0,0)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        layout.addWidget(self.label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.draw_board(state)

    def draw_board(self, state: State) -> None:
        _canvas = QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        _canvas.fill(QColor("#197b30")) # dark green
        self.label.setPixmap(_canvas)
        painter = QPainter(self.label.pixmap())
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))

        dimension = len(state.board)

        # draw grid
        for row_index in range(dimension + 1):
            painter.drawLine(0, row_index * 50, WINDOW_WIDTH, row_index * 50)
        for col_index in range(dimension + 1):
            painter.drawLine(col_index * 50, 0, col_index * 50, WINDOW_HEIGHT)

        # draw disks
        for row_index in range(dimension):
            for col_index in range(dimension):
                cell = state.board[row_index][col_index]
                if cell == 0:
                    continue

                disk_color = Qt.black if cell == 1 else Qt.white
                painter.setPen(QPen(disk_color, 8, Qt.SolidLine))
                painter.setBrush(QBrush(disk_color, Qt.SolidPattern))
                painter.drawEllipse(row_index * 50 + 10, col_index * 50 + 10, 30, 30)

        painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(State())
    window.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setWindowTitle("Reversi")
    window.show()
    app.exec_()
