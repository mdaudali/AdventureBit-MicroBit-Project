from microbit import *
import radio


class Enemy:
    def __init__(self):
        self.health = 100
        self.attack = 10
        # self.defence = 0.5
        # self.sp_defence = 0.5

    def take_damage(self, damage):
        self.health -= damage
        return self.health


class Communication:
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
            data[key] = value
        return data

enemy = Enemy()
while 1:
    resp = Communication(42).wait_for_command()
    if resp["command"] == "attack":
        enemy.take_damage(5)
    display.scroll(str(enemy.health))