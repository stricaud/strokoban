from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *

from strokoban.gamebuffer import GameBuffer

class GameWidget(QWidget):
    def __init__(self, datadir, level_buffer):
        super(GameWidget, self).__init__()

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.game_layout = GameBuffer(datadir, level_buffer)
        game_widget = QWidget()
        game_widget.setLayout(self.game_layout.render())
        self.main_layout.addWidget(game_widget, 0, 0)

    def refresh(self):
        item = self.main_layout.itemAtPosition(0,0)
        item.widget().hide()
        self.main_layout.removeItem(item)
        game_widget = QWidget()
        game_widget.setLayout(self.game_layout.render())
        self.main_layout.addWidget(game_widget, 0, 0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # Undo!
            self.game_layout.history_set_objects_matrix_from_last()
            self.refresh()
            # print("Escape")
            return True

        if event.key() == Qt.Key_Left:
            # print("Left")
            self.game_layout.move_left()
            self.refresh()
        if event.key() == Qt.Key_Right: 
            # print("Right")
            self.game_layout.move_right()
            self.refresh()
        if event.key() == Qt.Key_Up:
            # print("Up")
            self.game_layout.move_up()
            self.refresh()
        if event.key() == Qt.Key_Down:
            # print("Down")
            self.game_layout.move_down()
            self.refresh()

        self.game_layout.history_add()

        if self.game_layout.has_won():
            print("YOU WIN!")

        # print("Key pressed")
