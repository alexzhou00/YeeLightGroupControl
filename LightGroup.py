import yeelight as yl
import time
from Bulb import Bulb
from utils import read_file_to_dict, write_dict_to_file
class LightGroup():
    def __init__(self, group_name, names, loadfile = None):
        self.group_name = group_name
        self.names = names # store in case you want to reconnect or something idk
        self.loadfile = loadfile
        self.bulbs = []

        bulb_dicts = yl.discover_bulbs()
        for bulb_dict in bulb_dicts:
            if bulb_dict['capabilities']['name'] in names:
                self.bulbs.append(Bulb(yl.Bulb(bulb_dict['ip'])))

        self.prev_t = time.time()

        if loadfile:
            self.load_state()
        else:
            self.loadfile = group_name + '_latest.txt'
            self.turn_on()
            self.on = True 
            self.h = 0
            self.s = 0
            self.brightness = 100
            self.degrees = 3800
            self.r = 255
            self.g = 255
            self.b = 255

            self.set_mode(yl.PowerMode.NORMAL)

    def toggle_music_mode(self, state=None):
        """ Activates music mode on all the bulbs in this LightGroup
            Music mode is necessary when sending more than 60 commands
            per second. This is desirable when controlling lights
            using a rotary encoder!

        Args:
            state: Either '0' (str) or 1 (int) if provided, because 
                    that's how it works in the Python yeelight package. 
                    If None, then music mode is toggled/switched

        Returns:
            The current mode of the LightGroup
        """
        assert state is None or state == '0' or state == 1
        for bulb in self.bulbs:
            try:
                bulb.get_properties()
            except yl.BulbException as e:
                print("Error with bulb ", bulb.name, ":", e)
            
            if state is None:
                if bulb.get_music_mode() == '0':
                    target = 1
                else:
                    target = '0'
            else:
                target = state 
            
            if target == 1:
                method = bulb.start_music
            else:
                method = bulb.stop_music
            
            while bulb.get_music_mode() != target:
                try:
                    method()
                    break       # break if successful
                except yl.BulbException as e:
                    pass        # Sometimes will error even on success.
                except TypeError as e:
                    print("Caught error:", e) # Not sure why this error occurs. Just catch for now
        
        return target 
    
    def set_brightness(self, brightness):
        brightness = min(100, max(brightness, 0))
        self.brightness = brightness

        # Rate limit commands
        if time.time() < self.prev_t + .1:
            return 0

        for bulb in self.bulbs:
            try:
                if brightness == 0:
                    if bulb.on:
                        bulb.turn_off()
                else:
                    if not bulb.on:
                        bulb.turn_on()
                    bulb.set_brightness(brightness)
            except yl.BulbException as e:
                pass 
        
        if brightness == 0:
            self.on = False

        self.prev_t = time.time()
    
    def incr_brightness(self, step=5):
        self.set_brightness(self.brightness + step)
    
    def decr_brightness(self, step=5):
        self.set_brightness(self.brightness - step)

    def set_mode(self, mode):
        time.sleep(0.2)
        self.set_brightness(self.brightness)
        time.sleep(0.2)
        if mode == yl.PowerMode.NORMAL:
            self.set_color_temp(self.degrees)
        elif mode == yl.PowerMode.RGB:
            self.set_rgb(self.r, self.g, self.b)
        elif mode == yl.PowerMode.HSV:
            self.set_hsv(self.h, self.s)

    def set_color_temp(self, degrees):
        self.mode = yl.PowerMode.NORMAL
        degrees = min(6500, max(degrees, 1700))
        self.degrees = degrees

        # Rate limit commands
        if time.time() < self.prev_t + .1:
            return 0

        for bulb in self.bulbs:
            try:
                bulb.set_power_mode(yl.PowerMode.NORMAL)
                bulb.set_color_temp(degrees)
            except yl.BulbException as e:
                pass 
        self.prev_t = time.time()
    
    def incr_color_temp(self, step=50):
        self.set_color_temp(self.degrees + step)
    
    def decr_color_temp(self, step=50):
        self.set_color_temp(self.degrees - step)

    def set_rgb(self, r, g, b):
        self.mode = yl.PowerMode.RGB
        r = min(255, max(0, r))
        g = min(255, max(0, g))
        b = min(255, max(0, b))
        self.r, self.g, self.b = r, g, b

        # Rate limit commands 
        if time.time() < self.prev_t + .1:
            return 0
        
        for bulb in self.bulbs:
            try:
                bulb.set_power_mode(yl.PowerMode.RGB)
                bulb.set_rgb(r, g, b)
            except yl.BulbException as e:
                pass 
        self.prev_t = time.time() 

    def incr_r(self, step=5):
        self.set_rgb(self.r+step, self.g, self.b)
        
    def incr_g(self, step=5):
        self.set_rgb(self.r, self.g+step, self.b)
    
    def incr_b(self, step=5):
        self.set_rgb(self.r, self.g, self.b+step)
    
    def decr_r(self, step=5):
        self.set_rgb(self.r-step, self.g, self.b)
    
    def decr_g(self, step=5):
        self.set_rgb(self.r, self.g-step, self.b)
    
    def decr_b(self, step=5):
        self.set_rgb(self.r, self.g, self.b-step)       

    def set_hsv(self, hue, saturation):
        self.mode = yl.PowerMode.HSV
        hue = hue % 360 
        saturation = max(0, min(100, saturation))
        self.h, self.s = hue, saturation

        if time.time() < self.prev_t + .1:
            return 0

        for bulb in self.bulbs:
            try:
                bulb.set_power_mode(yl.PowerMode.HSV)
                bulb.set_hsv(hue, saturation)
            except yl.BulbException as e:
                pass 
        
        self.prev_t = time.time()

    def incr_hue(self, step=8):
        self.set_hsv(self.h+step, self.s)
    
    def incr_saturation(self, step=5):
        self.set_hsv(self.h, self.s+step)
    
    def decr_hue(self, step=8):
        self.set_hsv(self.h-step, self.s)
    
    def decr_saturation(self, step=5):
        self.set_hsv(self.h, self.s-step)

    def turn_on(self):
        for bulb in self.bulbs:
            try:
                bulb.turn_on()
            except yl.BulbException as e:
                pass 
        self.on = True

    def turn_off(self):
        for bulb in self.bulbs:
            try:
                bulb.turn_off()
            except yl.BulbException as e:
                pass 
        self.on = False

    def toggle(self):
        if self.on:
            self.turn_off()
        else:
            self.turn_on()

    def load_state(self, filename=None):
        assert self.loadfile is not None or filename is not None
        if filename is None:
            filename = self.loadfile 
        
        d = read_file_to_dict(filename)

        self.on = bool(d['on'])
        self.mode = yl.PowerMode(int(d['mode']))
        self.h = int(d['h'])
        self.s = int(d['s'])
        self.brightness = int(d['brightness'])
        self.degrees = int(d['degrees'])
        self.r = int(d['r'])
        self.g = int(d['g'])
        self.b = int(d['b'])
        self.group_name = d['group_name']

        self.set_mode(self.mode)

    def save_state(self, filename=None):
        assert self.loadfile is not None or filename is not None
        if filename is None:
            filename = self.loadfile
        
        d = {}
        d['on'] = self.on
        d['mode'] = int(self.mode)
        d['h'] = self.h
        d['s'] = self.s 
        d['brightness'] = self.brightness 
        d['degrees'] = self.degrees 
        d['r'] = self.r 
        d['g'] = self.g 
        d['b'] = self.b 
        d['group_name'] = self.group_name 
        d['names'] = self.names 

        write_dict_to_file(filename, d)