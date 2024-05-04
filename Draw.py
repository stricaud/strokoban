import pygame


class Buddy():
    def __init__(self):
        self.state = "buddy-down"
        self.x = 0
        self.y = 0

    def update_xy(self, x, y):
        self.x = x
        self.y = y

    def update_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state

class LevelMatrix():
    def __init__(self, level_matrix):
        self.level_matrix = level_matrix

    def set(self, value, x, y):
        self.level_matrix[y][x] = value

    def get(self, x, y):
        return self.level_matrix[y][x]

    def foreach_row(self):
        for row in self.level_matrix:
            yield row

    def foreach_col(self, row):
        for col in row:
            yield col
    
class StrokobanDraw():
    def __init__(self, level_matrix):
        self.tile_file = "tilesheet.png"
        self.tile_width = 64
        self.tile_height = self.tile_width
        self.tileset = pygame.image.load(self.tile_file)
        
        self.tiles = {"box": [1, 0],
                      "buddy-down": [0, 5],
                      "buddy-left": [3, 6],
                      "buddy-right": [0, 6],
                      "buddy-up": [5, 4],
                      "empty": [0, 1],
                      "target": [11, 4],
                      "wall": [7, 6]}

        self.buddy = Buddy()
        self.is_first = True
        self.matrix = LevelMatrix(level_matrix)

    def get_tile(self, tile_name):
        tile_x = self.tiles[tile_name][0] * self.tile_width
        tile_y = self.tiles[tile_name][1] * self.tile_height

        tile_rect = pygame.Rect(tile_x, tile_y, self.tile_width, self.tile_height)
        tile = self.tileset.subsurface(tile_rect)

        return tile

    def draw_tile(self, screen, tile_name, x, y):
        tile = self.get_tile(tile_name)
        tile_x = x * self.tile_width
        tile_y = y * self.tile_height
        screen.blit(tile, (tile_x, tile_y))

    def move_buddy(self, direction):
        current_x = self.buddy.x
        current_y = self.buddy.y
        can_move = False
        if direction == "up":
            if self.matrix.get(current_x, current_y-1) in [" ", "."]:
                can_move = True
            if self.matrix.get(current_x, current_y-1) == "#":
                if self.matrix.get(current_x, current_y-2) in [" ", "."]:
                    can_move = True
                    self.matrix.set("#", current_x, current_y-2)

            if can_move:
                self.buddy.update_xy(current_x, current_y-1)
                self.buddy.update_state("buddy-up")
                self.matrix.set(" ", current_x, current_y)
                self.matrix.set("*", current_x, current_y - 1)

        if direction == "down":
            if self.matrix.get(current_x, current_y+1) in [" ", "."]:
                can_move = True
            if self.matrix.get(current_x, current_y+1) == "#":
                if self.matrix.get(current_x, current_y+2) == " ":
                    can_move = True
                    self.matrix.set("#", current_x, current_y + 2)

            if can_move:
                self.buddy.update_xy(current_x, current_y+1)
                self.buddy.update_state("buddy-down")
                self.matrix.set(" ", current_x, current_y)
                self.matrix.set("*", current_x, current_y + 1)

                
        if direction == "left":
            if self.matrix.get(current_x-1, current_y) in [" ", "."]:
                can_move = True
            if self.matrix.get(current_x-1, current_y) == "#":
                if self.matrix.get(current_x-2, current_y) in [" ", "."]:
                    can_move = True
                    self.matrix.set("#", current_x-2, current_y)

            if can_move:
                self.buddy.update_xy(current_x-1, current_y)
                self.buddy.update_state("buddy-left")
                self.matrix.set(" ", current_x, current_y)
                self.matrix.set("*", current_x-1, current_y)

        if direction == "right":
            if self.matrix.get(current_x+1, current_y) in [" ", "."]:
                can_move = True
            if self.matrix.get(current_x+1, current_y) == "#":
                if self.matrix.get(current_x+2, current_y) in [" ", "."]:
                    can_move = True
                    self.matrix.set("#", current_x+2, current_y)

            if can_move:
                self.buddy.update_xy(current_x+1, current_y)
                self.buddy.update_state("buddy-right")
                self.matrix.set(" ", current_x, current_y)
                self.matrix.set("*", current_x+1, current_y)

                
    def draw_level(self, screen):
        current_row = 0
        for row in self.matrix.foreach_row():
            current_col = 0
            for col in self.matrix.foreach_col(row):
                if col == "X": # Wall
                    self.draw_tile(screen, "wall", current_col, current_row)
                if col == "*" or col == "$":
                    if self.is_first:
                        self.buddy.update_xy(current_col, current_row)
                        self.is_first = False
                    self.draw_tile(screen, self.buddy.get_state(), current_col, current_row)
                if col == ".": 
                    self.draw_tile(screen, "target", current_col, current_row)
                if col == "#" or col == "%": 
                    self.draw_tile(screen, "box", current_col, current_row)
                current_col += 1
            current_row += 1
