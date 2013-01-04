import os

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *

class GameBuffer:
    def __init__(self, datadir, level_buffer):
        self.images = {
            'box': datadir + os.sep + "box.svg",
            'buddy-down': datadir + os.sep + "buddy-down.svg",
            'buddy-front': datadir + os.sep + "buddy-front.svg",
            'buddy-left': datadir + os.sep + "buddy-left.svg",
            'buddy-right': datadir + os.sep + "buddy-right.svg",
            'buddy-up': datadir + os.sep + "buddy-up.svg",
            'empty': datadir + os.sep + "empty.svg",
            'target': datadir + os.sep + "target.svg",
            'wall': datadir + os.sep + "wall.svg",
            }

        self.targets_number = self.get_targets_number(level_buffer)
        self.objects_matrix = level_buffer.split('\n')
        self.objects_matrix_history_tracking = []
        self.buddy_x = 0
        self.buddy_y = 0
        self.max_x = 0
        self.max_y = 0

    def history_add(self):
        matrix = list(self.objects_matrix)
        self.objects_matrix_history_tracking.append(matrix)
        # print(">>>")
        # for obj in self.objects_matrix_history_tracking:
        #     print(str(obj))
        # print("<<<")

    def history_set_objects_matrix_from_last(self):
        try:
            self.objects_matrix_history_tracking.pop() # We remove the last
            self.objects_matrix = self.objects_matrix_history_tracking[-1]
            return True
        except:
            # We don't care, but we just notify that is no more history if one want to graphicaly do something
            return False

    def get_targets_number(self, level_buffer):
        return level_buffer.count('#') + level_buffer.count('%')

    def has_won(self):
        total_targets = 0
        for line in self.objects_matrix:
            total_targets += line.count('%')

        if total_targets == self.targets_number:
            return True

        return False

    def render(self):
        game_layout = QGridLayout()

        # print("[%s]" % (self.objects_matrix))
        y_pos = 0
        for line in self.objects_matrix:
            x_pos = 0
            while x_pos < len(line):
                if line[x_pos] == 'X': # Wall
                    game_layout.addWidget(QSvgWidget(self.images['wall']), y_pos, x_pos)
                if line[x_pos] == ' ': # Empty
                    game_layout.addWidget(QSvgWidget(self.images['empty']), y_pos, x_pos)
                if line[x_pos] == '*' or line[x_pos] == '$': # Buddy Front
                    self.buddy_x = x_pos
                    self.buddy_y = y_pos
                    # print("BUDDY POS X = %d" % (x_pos))
                    game_layout.addWidget(QSvgWidget(self.images['buddy-front']), y_pos, x_pos)
                if line[x_pos] == '.': # Target
                    game_layout.addWidget(QSvgWidget(self.images['target']), y_pos, x_pos)
                if line[x_pos] == '#': # Target
                    game_layout.addWidget(QSvgWidget(self.images['box']), y_pos, x_pos)
                if line[x_pos] == '%': # Target
                    game_layout.addWidget(QSvgWidget(self.images['box']), y_pos, x_pos)
                x_pos += 1

            y_pos += 1

        self.max_y = y_pos - 1
        self.max_x = len(self.objects_matrix[0])

        return game_layout

    def set_object_matrix_item(self, x_pos, y_pos, item):
        line = self.objects_matrix[y_pos]
        line = line[:x_pos] + item + line[x_pos+1:]
        self.objects_matrix[y_pos] = line

    def get_object_matrix_item(self, x_pos, y_pos):
        return self.objects_matrix[y_pos][x_pos]

    def is_pos_invalid(self, x_pos, y_pos):
        # print("xpos=%d" % (x_pos))
        if x_pos < 1 or y_pos < 1:
            return True

        return False

    def get_object_right(self):
        if self.is_pos_invalid(self.buddy_x, self.buddy_y):
            return "E"
        return self.objects_matrix[self.buddy_y][self.buddy_x + 1]

    def get_object_left(self):
        if self.is_pos_invalid(self.buddy_x, self.buddy_y):
            return "E"
        return self.objects_matrix[self.buddy_y][self.buddy_x - 1]

    def get_object_up(self):
        if self.is_pos_invalid(self.buddy_x, self.buddy_y):
            return "E"
        return self.objects_matrix[self.buddy_y - 1][self.buddy_x]

    def get_object_down(self):
        if self.is_pos_invalid(self.buddy_x, self.buddy_y):
            return "E"
        return self.objects_matrix[self.buddy_y + 1][self.buddy_x]

    def get_object_right_right(self):
        if self.is_pos_invalid(self.buddy_x + 1, self.buddy_y):
            return "E"
        return self.objects_matrix[self.buddy_y][self.buddy_x + 2]

    def get_object_left_left(self):
        if self.is_pos_invalid(self.buddy_x - 1, self.buddy_y):
            return "E"
        return self.objects_matrix[self.buddy_y][self.buddy_x - 2]

    def get_object_up_up(self):
        if self.is_pos_invalid(self.buddy_x, self.buddy_y - 1):
            return "E"
        return self.objects_matrix[self.buddy_y - 2][self.buddy_x]

    def get_object_down_down(self):
        if self.is_pos_invalid(self.buddy_x, self.buddy_y + 1):
            return "E"
        return self.objects_matrix[self.buddy_y + 2][self.buddy_x]

    def can_move(self, on, onn): # on = object_next ; onn = object_next_next
        if on == '%' or on == '#':
            if onn == '#' or onn == 'X' or onn == 'E' or onn == '%':
                return False

        if on == 'X':
            return False

        if on == 'E':
            return False

        return True

    def _get_xpos_level1(self, direction):
        return { 'right' : self.buddy_x + 1,
                 'left': self.buddy_x - 1,
                 'up': self.buddy_x,
                 'down': self.buddy_x,
                 }.get(direction)

    def _get_xpos_level2(self, direction):
        return { 'right' : self.buddy_x + 2,
                 'left': self.buddy_x - 2,
                 'up': self.buddy_x,
                 'down': self.buddy_x,
                 }.get(direction)

    def _get_ypos_level1(self, direction):
        return { 'right' : self.buddy_y,
                 'left': self.buddy_y,
                 'up': self.buddy_y - 1,
                 'down': self.buddy_y + 1,
                 }.get(direction)

    def _get_ypos_level2(self, direction):
        return { 'right' : self.buddy_y,
                 'left': self.buddy_y,
                 'up': self.buddy_y - 2,
                 'down': self.buddy_y + 2,
                 }.get(direction)

    def change_item_after_move(self, direction, on, onn):
        # direction = 'up', 'right', 'down' or 'left'
        # print("[%d:%d] = '%s'" % (self.buddy_x + 1, self.buddy_y, self.get_object_matrix_item(self.buddy_x + 1, self.buddy_y)))
        # print("Direction:%s current_item:%s on:%s onn:%s" % (direction, self.get_object_matrix_item(self.buddy_x, self.buddy_y), on, onn))

        # Our buddy was on a target
        if self.get_object_matrix_item(self.buddy_x, self.buddy_y) == '$':
            # Since the buddy has moved, we now see the target again
            self.set_object_matrix_item(self.buddy_x, self.buddy_y, '.')        
        else:
            self.set_object_matrix_item(self.buddy_x, self.buddy_y, ' ')        


        if on == '#':
            if onn == '.':
                self.set_object_matrix_item(self._get_xpos_level1(direction), self._get_ypos_level1(direction), '*')
                self.set_object_matrix_item(self._get_xpos_level2(direction), self._get_ypos_level2(direction), '%')
            else:
                self.set_object_matrix_item(self._get_xpos_level1(direction), self._get_ypos_level1(direction), '*')
                self.set_object_matrix_item(self._get_xpos_level2(direction), self._get_ypos_level2(direction), '#')
            return

        if on == '.':
            self.set_object_matrix_item(self._get_xpos_level1(direction), self._get_ypos_level1(direction), '$') 
            return
           
        if on == '%':
            self.set_object_matrix_item(self._get_xpos_level1(direction), self._get_ypos_level1(direction), '$')
            if onn == '.':
                self.set_object_matrix_item(self._get_xpos_level2(direction), self._get_ypos_level2(direction), '%')
            else:
                self.set_object_matrix_item(self._get_xpos_level2(direction), self._get_ypos_level2(direction), '#')
            return
        else:
            self.set_object_matrix_item(self._get_xpos_level1(direction), self._get_ypos_level1(direction), '*')


    def move_buddy_right(self):
        right = self.get_object_right()
        right_right = self.get_object_right_right()

        if self.can_move(right, right_right):
            self.change_item_after_move('right', right, right_right)

    def move_right(self):
        self.move_buddy_right()

    def move_buddy_left(self):
        left = self.get_object_left()
        left_left = self.get_object_left_left()

        if self.can_move(left, left_left):
            self.change_item_after_move('left', left, left_left)

    def move_left(self):
        self.move_buddy_left()

    def move_buddy_up(self):
        up = self.get_object_up()
        up_up = self.get_object_up_up()

        if self.can_move(up, up_up):
            self.change_item_after_move('up', up, up_up)

    def move_up(self):
        self.move_buddy_up()

    def move_buddy_down(self):
        down = self.get_object_down()
        down_down = self.get_object_down_down()

        if self.can_move(down, down_down):
            self.change_item_after_move('down', down, down_down)

    def move_down(self):
        self.move_buddy_down()
