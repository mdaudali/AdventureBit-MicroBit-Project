class Communicator:
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