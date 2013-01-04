#!/usr/bin/python3

import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *

from strokoban.levels import Levels
from strokoban.gamewidget import GameWidget

strokoban_levels = Levels()
print("Levels list:")
print(strokoban_levels.get_names())

use_level = "default"

error = strokoban_levels.check(use_level)
if error is not None:
    print(error)


# print("Number of levels: %d" % (strokoban_levels.get_max_value(use_level)))
# print("Buffer for level 1: [%s]" % (strokoban_levels.get_level(use_level, 1)))


app = QApplication(sys.argv)

images_datadir = ".." + os.sep + "data" + os.sep + "levels" + os.sep + "default" + os.sep + "images"
level_buffer = strokoban_levels.get_level(use_level, sys.argv[1])
game_widget = GameWidget(images_datadir, level_buffer)
# game_widget.render(strokoban_levels.get_level(use_level, 31))
game_widget.show()

# Run the main Qt loop
app.exec_()    
