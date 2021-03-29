class Bulb():
    def __init__(self, bulb):
        self.bulb = bulb 
        self.name = bulb.get_properties()['name']
        self.on = bulb.get_properties()['power'] == 'on'
        self.ip = bulb._ip
        self.connected = True # Need to add functionality for tracking connectedness

    def turn_on(self):
        self.bulb.turn_on()
        self.on = True 
    
    def turn_off(self):
        self.bulb.turn_off()
        self.on = False
    
    def toggle(self):
        if self.on:
            self.turn_off()
        else:
            self.turn_on()
    
    def get_music_mode(self):
        return self.bulb.get_properties()['music_on']

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            return getattr(self.bulb, attr)
        return super().__getattr__(attr)