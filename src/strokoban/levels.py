import os

from collections import OrderedDict

class Levels:
    def __init__(self, datadir=None):
        if datadir is None:
            self.datadir = ".." + os.sep + "data" + os.sep + "levels"

    def get_names(self):
        levels_names = os.listdir(self.datadir)
        return levels_names
    
    def get_sorted_list(self, levels_name):
        levels = os.listdir(self.datadir + os.sep + levels_name)
        levels.remove("images")
        return sorted(levels, key = lambda x: int(x.rsplit('.', 1)[0]))

    def get_max_value(self, levels_name):
        return int(self.get_sorted_list(levels_name)[-1].rsplit('.', 1)[0])

    def check(self, levels_name):
        """
        Check if we have continuous levels. 
        """
        levels = self.get_sorted_list(levels_name) 
        
        last_level = 0
        for level in levels:
            level = int(level.rsplit('.', 1)[0])
            if level != last_level + 1:
                return "Error, level %d does not exists" % (last_level + 1)

            last_level = level

        return None

    def get_level(self, levels_name, level_number):
        levelfile = open(self.datadir + os.sep + levels_name + os.sep + str(level_number) + ".txt")
        levelbuf = levelfile.read()
        levelfile.close()
        return levelbuf
