"""
Computational Art Redone
mini project #5
Noah Rivkin

Creates image based on random functions using object oriented code and lambda
functions
"""

import math
import random
from PIL import Image


class RandomImage:
    """
    generates a random image
    """
    def __init__(self, filename, min_depth = 7, max_depth = 9, x_size = 100, y_size = 100):
        """
        Initilizes image
        """
        self.image = Image.new("RGB", (x_size, y_size))
        self.filename = filename
        self.depth = min_depth + random.randint(0, max_depth - min_depth) - 1
        self.x_size = x_size
        self.y_size = y_size
        x_scale = 2/x_size
        y_scale = 2/y_size
        self.x = [(x - x_size) * x_scale + 1 for x in range(x_size)]
        self.y = [(y - y_size) * y_scale + 1 for y in range(y_size)]
        self.f_dict = {0: "x", 1: "y", 2: "prod", 3: "avg", 4: "cos_pi", 5: "sin_pi", 6: "negative", 7:"root_abs_val"}

    def randomize(self):
        red_funcs = self.get_random_function()
        green_funcs = self.get_random_function()
        blue_funcs = self.get_random_function()
        pixels = self.image.load()
        for i in range(self.x_size):
            for j in range(self.y_size):
                pixels[i, j] = (
                        self.col_map(self.eval_function(red_funcs, self.x[i], self.y[j])),
                        self.col_map(self.eval_function(green_funcs, self.x[i], self.y[j])),
                        self.col_map(self.eval_function(blue_funcs, self.x[i], self.y[j]))
                        )
        self.image.save(self.filename)

    def get_random_function(self, depth = 0):
        '''
        chooses random function, and calls itself as necessary
        f_dict = {2: "prod", 3: "avg", 4: "cos_pi", 5: "sin_pi", 6: "negative", 7:"root_abs_val"}
        end_f = {0: "x", 1: "y"}
        '''
        if self.depth < depth:
            return self.f_dict[random.randint(0, 1)]
        else:
            f_num = random.randint(2,7)
            if f_num < 4:
                return [self.f_dict[f_num],self.get_random_function(depth + 1),self.get_random_function(depth + 1)]
            else:
                return [self.f_dict[f_num],self.get_random_function(depth + 1)]

    def eval_function(self,f,x,y):
        if f[0] == "x":
            return x
        elif f[0] == "y":
            return y
        elif f[0] == "prod":
            return self.eval_function(f[1], x, y) * self.eval_function(f[2], x, y)
        elif f[0] == "avg":
            return .5 * (self.eval_function(f[1], x, y) + self.eval_function(f[2], x, y))
        elif f[0] == "cos_pi":
            return math.cos(math.pi * self.eval_function(f[1], x, y))
        elif f[0] == "sin_pi":
            return math.sin(math.pi * self.eval_function(f[1], x, y))
        elif f[0] == "negative":
            return -1 * self.eval_function(f[1], x, y) ** 2
        elif f[0] == "root_abs_val":
            return ((self.eval_function(f[1], x, y) ** 2) ** .5) ** .5

    def col_map(self, val):
        """
        maps function onto color values
        """
        val += 1
        val *= 128
        return int(val)


if __name__ == '__main__':
    myimage = RandomImage('Object_oriented_example.png', 7, 9, 350, 350)
    myimage.randomize()
