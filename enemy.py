from microbit import *
import radio


class Comm:
    def __init__(self, radio_group, **kargs):
        self.kargs = kargs
        radio.on()
        radio.config(group=radio_group, queue=10)

    def send_command(self, command, value):
        vals = self.kargs
        vals["command"] = command
        vals["value"] = value
        data = ":".join([str(x) + "," + str(vals[x]) for x in vals])
        radio.send(data)

    def wait_for_command(self, blocking = 1):
        if blocking:
            while True:
                msg = radio.receive()
                if msg:
                    break
        else:
            msg = radio.receive()
        if not msg:
            return {"command": "", "value": ""}
        vals = msg.split(":")
        data = {}
        for x in vals:
            key, value = x.split(",")
            data[key] = value
        return data


class Enemy:
    def __init__(self):
        self.max_health = 9
        self.health = self.max_health
        self.attack = 10
        self.level = 2
        self.defence = 2
        self.sp_defence = 2

    def take_damage(self, response):
        if response["command"] == "phys_attack":
            damage = int(resp["value"]) // self.defence
        elif response["command"] == "magic_attack":
            damage = int(resp["value"]) // self.sp_defence
        else:
            return
        self.health -= int(damage)
        if self.health <= 0:
            com.send_command("end_fight", 1)

    def display_health(self):
        lights = self.health*10
        board = [["0" for x in range(5)] for y in range(5)]
        for i in range(5):
            if lights >= i * 20 + 20:
                board[0][i] = "9"
        return Image(':'.join([''.join(vals) for vals in board]))

    def aoe_attack(self):
        com.send_command("enemy_attack", self.level)

    def attack(self):
        self.aoe_attack()

    def wake(self):
        com.send_command("start_fight", 1)
        display.show(Image("00900:00900:00900:00000:00900"))
        sleep(500)
        for x in range(11):
            display.show(Image.ANGRY.shift_right(x - 5))
            sleep(200)

    def start(self):
        while True:
            resp = com.wait_for_command(0)
            if resp["command"] == "start_fight":
                while not resp["command"] == "end_fight":
                    resp = com.wait_for_command(0)
                    if button_a.is_pressed() or button_b.is_pressed():
                        display.scroll("Finish fight...")
            if button_a.is_pressed() or button_b.is_pressed():
                enemy.wake()
                break
        while enemy.health > 0:
            display.show(enemy.display_health())

com = Comm(42, group_id = 1)
enemy = Enemy()
enemy.start()
