from microbit import *
import random
import radio

#swordAn =[Image("00900:00900:00900:09990:00900"),Image("90000:09000:00909:00090:00909"),Image("00009:00090:90900:09000:90900")]
critAni = [Image("00900:00900:00900:09990:00900"),Image("90909:00900:00900:09990:90909"),Image("00900:00900:00900:09990:00900"),Image("90909:00900:00900:09990:90909")]
sheild = Image("99999:99999:90909:09090:00900")

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
        self.maxHealth = 20
        self.health = self.maxHealth
        self.hitProb = 0.6
        self.damageReduction = 1
        self.classDamage = 1

    def attack(self):
        com.send_command("attack", self.lvl*self.classDamage)
            
    def take_damage(self, damage):
        if (random.randint(0,10)/10.0)<=self.hitProb:
            self.health -= (int(damage))
            #display.scroll(str(self.health))
        else:
            pass
            display.show(sheild)
            sleep(500)

    def display_health(self):
        lights = int((self.health/float(self.maxHealth))*100)
        #lights = self.health*10
        board = [["0" for x in range(5)] for y in range(5)]
        for i in range(5):
            if lights >= i * 20:
                board[0][i] = "9"
        return Image(':'.join([''.join(vals) for vals in board]))
        
### Changers ###
class Mage(Player):
    def __init__(self):
        super().__init__()
        self.maxHealth = 10
        self.health = self.maxHealth
        self.hitProb = 0.4
        self.classDamage = 4
        
class Warrior(Player):
    def __init__(self):
        super().__init__()
        self.maxHealth = 20
        self.health = self.maxHealth
        self.hitProb = 1
        self.classDamage = 2
        
class healers(Player):
    def __init__(self):
        super().__init__()
        self.maxHealth = 10
        self.health = self.maxHealth
        self.hitProb = 0.7
        self.classDamage = 0.5
  
        
def test_comms():
    resp = com.wait_for_command(0)
    #display.scroll(resp["command"])
    if resp["command"] == "end_fight":
        display.scroll("dead")
        tim.health = tim.maxHealth
    elif resp["command"] == "enemy_attack":
        tim.take_damage(resp["value"])
        
        
### Changers ###
com = Comm(42)
w, h = 5,5
grid = [[0 for x in range(w)] for y in range(h)]
tim = Warrior()
ori = True
while tim.health>0:
    display.show(tim.display_health())
    test_comms()        
    if accelerometer.is_gesture("face down") and ori:
        tim.attack()
        ori = False
    elif accelerometer.is_gesture("face up") and not ori:
        ori = True
        display.set_pixel(2,2,9)
        
    sleep(100)
    #display.clear()
    #sleep(500)

display.show(Image("90009:09090:00900:09090:90009"))