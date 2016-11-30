from microbit import *


def showPixel(brightness, x, y):
    grid = [["0"] * 5 for y in range(5)]
    grid[x][y] = str(brightness)
    return Image(':'.join([''.join(vals) for vals in grid]))


def showPixels(mapping):
    grid = [["0"] * 5 for y in range(5)]
    for x, y in mapping:
        grid[x][y] = "9"
    return Image(':'.join([''.join(vals) for vals in grid]))


class Snake(object):
    def __init__(self):
        self.length = 1
        self.turn_squares = []
        self.turn_directions = []
        self.head_square = [0, 0]
        self.brightness = 9

    def generate_map(self):
        mapping = []
        mapping.append(self.head_square)
        return mapping

    def move_snake(self, gesture):
        if gesture == "down":
            self.head_square[1] = min(9, self.head_square[1] + 1)
        elif gesture == "up":
            self.head_square[1] = max(0, self.head_square[1] - 1)
        elif gesture == "left":
            self.head_square[0] = max(0, self.head_square[0] - 1)
        elif gesture == "right":
            self.head_square[0] = min(9, self.head_square[0] + 1)


snake = Snake()
while 1:
    snake.move_snake(accelerometer.current_gesture())
    display.show(showPixels(snake.generate_map()))
    sleep(2000)