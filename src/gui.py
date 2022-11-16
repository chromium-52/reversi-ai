import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QPen

from model import State
from time import sleep

WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400

class MainWindow(QMainWindow):

    CELL_SIZE = 50
    DISK_SIZE = 30

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.board = QLabel()
        self.board.setContentsMargins(0, 0, 0, 0)
        self.board.setAlignment(Qt.AlignCenter)
        self.board.setScaledContents(True)
        self.board.mousePressEvent = self.handle_board_click
        layout.addWidget(self.board)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        _canvas = QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        _canvas.fill(QColor("#197b30")) # dark green
        self.board.setPixmap(_canvas)
        self.painter = QPainter(self.board.pixmap())

    def draw_board(self, state: State) -> None:
        self.painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))

        dimension = len(state.board)

        # draw grid
        for row_index in range(dimension + 1):
            self.painter.drawLine(0, row_index * self.CELL_SIZE, WINDOW_WIDTH, row_index * self.CELL_SIZE)
        for col_index in range(dimension + 1):
            self.painter.drawLine(col_index * self.CELL_SIZE, 0, col_index * self.CELL_SIZE, WINDOW_HEIGHT)

        # draw disks
        for row_index in range(dimension):
            for col_index in range(dimension):
                cell = state.board[row_index][col_index]
                if cell == State.EMPTY:
                    continue

                self.draw_disk(row_index, col_index, cell)

        print('Repainting')
        self.repaint()
        self.update()

    def draw_disk(self, row_index: int, col_index: int, cell: int) -> None:
        disk_color = Qt.black if cell == State.BLACK else Qt.white
        self.painter.setPen(QPen(disk_color, 8, Qt.SolidLine))
        self.painter.setBrush(QBrush(disk_color, Qt.SolidPattern))
        self.painter.drawEllipse(row_index * self.CELL_SIZE + 10, col_index * self.CELL_SIZE + 10, self.DISK_SIZE, self.DISK_SIZE)

    def handle_board_click(self, event) -> None:
        position = event.localPos()
        row_index = int(position.x() // self.CELL_SIZE)
        col_index = int(position.y() // self.CELL_SIZE)
        print(row_index, col_index)

    def shutdown(self) -> None:
        self.painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setWindowTitle("Reversi")

    sleep(1)
    window.draw_board(State())

    window.show()

    sleep(1)
    window.draw_board(State())

    app.exec_()

    window.draw_board(State())

    window.shutdown()
