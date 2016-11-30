import ujson
class Communication:
    def __init__(self, group):
        self.group = group
        radio.on()
        radio.channel(group)

    def send_command(self, command, value):
        vals  = {}
        vals["command"] = command
        vals["value"] = value
        dmp = ujson.dumps(vals)
        radio.send(dmp)