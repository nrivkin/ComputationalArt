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
        self.depth = min_depth + random.randint(0, max_depth - min_depth) - 1
        self.x_size = x_size
        self.y_size = y_size
        x_scale = 2/x_size
        y_scale = 2/y_size
        self.x = [(x + x_size) * x_scale - 1 for x in range(x_size)]
        self.y = [(y + y_size) * y_scale - 1 for y in range(y_size)]

    def randomize(self):
        red_funcs = self.gen_rand_func()
        green_funcs = self.gen_rand_func()
        blue_funcs = self.gen_rand_func()
        pixels = self.image.load()
        for i in range(self.x_size):
            temp_x = self.x[i]
            for j in range(self.y_size):
                pixels[i, j] = (
                        self.col_map(red_funcs, temp_x, self.y[j]),
                        self.col_map(green_funcs, temp_x, self.y[j]),
                        self.col_map(blue_funcs, temp_x, self.y[j])
                        )
        self.image.save(filemane)

    def gen_rand_func(self):
        func_list = []
        for i in range(self.depth):
            func_list.append(random.randint(0,5))
        func_list.append(random.randint(0,1))
        return func_list

    def eval_func(self, func_list, x, y, level):
        """
        Evaluate the random function f with inputs x,y
        """
        f = func_list[self.depth - level]
        if f == 0:
            return map(lambda x: x, x)
        elif f == 1:
            return map(lambda x: x, y)
        elif f == 2:
            return map(lambda x: self.eval_func(func_list, x, y, level + 1) * self.eval_func(func_list, x, y, level + 1), x)
        elif f == 3:
            return map(lambda x: .5 * (self.eval_func(func_list, x, y, level + 1) + self.eval_func(func_list, x, y, level + 1)), x)
        elif f == 4:
            return map(lambda x: math.cos(math.pi * self.eval_func(func_list, x, y, level + 1)), x)
        elif f == 5:
            return map(lambda x: math.sin(math.pi * self.eval_func(func_list, x, y, level + 1)), x)
        elif f == 6:
            return map(lambda x: -1 * self.eval_func(func_list, x, y, level + 1) ** 2, x)
        elif f == 7:
            return map(lambda x: ((self.eval_func(func_list, x, y, level + 1) ** 2) ** .5) ** .5, x)

    def col_map(self, func, x, y):
        """
        maps function onto color values
        """
        print(map(self.eval_func(func, x, y, 0)), 1)
        val += 1
        val *= 128
        return int(val)







def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    depth = random.randint(0, 1)
    if depth > max_depth:
        end_f = {0: "x", 1: "y"}
        return end_f[depth]
    else:
        f_num = random.randint(0,5)
        f_dict = {0: "prod", 1: "avg", 2: "cos_pi", 3: "sin_pi", 4: "negative", 5:"root_abs_val"}
        return [f_dict[f_num],build_random_function(min_depth - 1, max_depth - 1),build_random_function(min_depth - 1, max_depth -1)]


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    elif f[0] == "prod":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == "avg":
        return .5 * (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))
    elif f[0] == "cos_pi":
        return math.cos(math.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == "sin_pi":
        return math.sin(math.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == "negative":
        return -1 * evaluate_random_function(f[1], x, y) ** 2
    elif f[0] == "root_abs_val":
        return ((evaluate_random_function(f[1], x, y) ** 2) ** .5) ** .5


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    scale_factor = (output_interval_end - output_interval_start) / (input_interval_end - input_interval_start)
    val -= input_interval_start  # displacement to ensure scaling is correct
    val *= scale_factor  # scaling
    val += output_interval_start # reverse displacement
    return val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    # generate_art("example3.png")
    myimage = RandomImage('Object_oriented_example')
    myimage.randomize()
