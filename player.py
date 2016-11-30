from microbit import *
import random
import radio

class Comm:
    def __init__(self, group):
        self.group = group
        radio.on()
        radio.config(group=group)

    def send_command(self, command, value):
        vals = {}
        vals["command"] = command
        vals["value"] = value
        data = ":".join([str(x) + "," + str(vals[x]) for x in vals])
        radio.send(data)

    def wait_for_command(self):
        while True:
            msg = radio.receive()
            if msg:
                break
        vals = msg.split(":")
        data = {}
        for x in vals:
            key, value = x.split(",")
            data[x] = value
        return data

class Player:
    def __init__(self):
        self.lvl = 1
        self.hp = 10

    def attack(self):
        com.send_command("attack", self.lvl)
        resp = com.wait_for_command()
        while 1:
            if resp["command"] == "health":
                health = resp["value"]
                break

    def takeDamage(self, damage):
        self.hp -= damage

    def displayHealth(self,board):
        lights = self.hp*10
        board = [[0 for x in range(w)] for y in range(h)]
        for i in range(5):
            if lights>=i*20+20:
                for y in range(5):
                    board[i][y] = 9
        return board
        
com = Comm(42)
w, h = 5,5
grid = [[0 for x in range(w)] for y in range(h)]
tim = Player()
while 1:
    if button_a.get_presses() > 0:
        tim.attack()
    

