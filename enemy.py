from microbit import *
import radio
from utilities import Communicator

class Enemy:
    def __init__(self):
        self.max_health = 10
        self.health = self.max_health
        self.attack = 10
        self.level = 2
        # self.defence = 0.5
        # self.sp_defence = 0.5

    def take_damage(self, damage):
        self.health -= int(damage)
        return self.health

    def send_health(self):
        com.send_command("health", self.health)

    def display_health(self):
        lights = (self.health/self.max_health) * 100
        board = [["0" for x in range(5)] for y in range(5)]
        for i in range(5):
            if lights >= i * 20 + 20:
                board[0][i] = "9"
        return Image(':'.join([''.join(vals) for vals in board]))

    def aoe_attack(self):
        com.send_command("attack", self.level)


def show_pixels(mapping):
    grid = [["0"] * 5 for y in range(5)]
    for x, y in mapping:
        grid[x][y] = "9"
    return Image(':'.join([''.join(vals) for vals in grid]))

com = Communicator(42)
enemy = Enemy()
while 1:
    display.show(enemy.display_health())
    resp = com.wait_for_command()
    if resp["command"] == "attack":
        enemy.take_damage(resp["value"])
        enemy.send_health()
