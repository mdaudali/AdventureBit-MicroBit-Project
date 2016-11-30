from microbit import *
import random
import radio

class Comm:
    def __init__(self, group):
        self.group = group
        radio.on()
        radio.config(group=group, queue=10)

    def send_command(self, command, value):
        vals = {}
        vals["command"] = command
        vals["value"] = value
        data = ":".join([str(x) + "," + str(vals[x]) for x in vals])
        radio.send(data)

    def wait_for_command(self, blocking=1):
        if blocking:
            while True:
                msg = radio.receive()
                if msg:
                    break
        else:
            msg = radio.receive()
        if not msg:
            return {"command":"", "value":""}
        vals = msg.split(":")
        data = {}
        for x in vals:
            key, value = x.split(",")
            data[key] = value
        return data

class Player:
    def __init__(self):
        self.lvl = 3
        self.maxHealth = 10
        self.health = 10

    def attack(self):
        com.send_command("attack", self.lvl)
            
    def take_damage(self, damage):
        self.health -= int(damage)

    def display_health(self):
        #lights = int((self.health/self.maxHealth)*100)
        lights = self.health*10
        board = [["0" for x in range(5)] for y in range(5)]
        for i in range(5):
            if lights >= i * 20 + 20:
                board[0][i] = "9"
        return Image(':'.join([''.join(vals) for vals in board]))
        
com = Comm(42)
w, h = 5,5
grid = [[0 for x in range(w)] for y in range(h)]
tim = Player()
while tim.health>0:
    display.show(tim.display_health())
    resp = com.wait_for_command(0)
    #display.scroll(resp["command"])
    if resp["command"] == "health":
        health = int(resp["value"])
        if health <= 0:
            display.scroll("dead")
    elif resp["command"] == "enemy_attack":
        tim.take_damage(resp["value"])
        
    if button_a.get_presses() > 0:
        tim.attack()
    sleep(100)
    #display.clear()
    #sleep(500)

display.show(Image("90009:09090:00900:09090:90009"))