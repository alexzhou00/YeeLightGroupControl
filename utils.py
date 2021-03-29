import yeelight as yl
import time
from Bulb import Bulb

def get_bulbs(names):
    bulbs = []

    bulb_dicts = yl.discover_bulbs()
    for bulb_dict in bulb_dicts:
        if bulb_dict['capabilities']['name'] in names:
            bulbs.append(Bulb(yl.Bulb(bulb_dict['ip'])))
    
    return bulbs

def toggle_music_mode(bulbs, state=None):
    assert state is None or state == '0' or state == 1
    for bulb in bulbs:
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
        
        while bulb.get_music_mode != target:
            try:
                method()
                break       # break if successful
            except yl.BulbException as e:
                pass        # Sometimes will error even on success.
            except TyperError as e:
                print("Caught error:", e) # Not sure why this error occurs. Just catch for now
    
    return target 

prev_t = time.time()

def set_color_temp(bulbs, degrees):
    global prev_t 
    degrees = min(6500, max(degrees, 1700))

    # Rate limit commands
    if time.time() < prev_t + .1:
        return 0

    for bulb in bulbs:
        try:
            bulb.set_power_mode(yl.PowerMode.NORMAL)
            bulb.set_color_temp(degrees)
        except yl.BulbException as e:
            pass 
    prev_t = time.time()
    return degrees

def set_brightness(bulbs, brightness):
    global prev_t
    brightness = min(100, max(brightness, 0))

    # Rate limit commands
    if time.time() < prev_t + .1:
        return 0

    for bulb in bulbs:
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
    
    prev_t = time.time()
    return brightness 

def set_hsv(hue, saturation):
    global prev_t
    hue = hue % 360 
    saturation = max(0, min(100, saturation))

    if time.time() < prev_t + .1:
        return 0

    for bulb in bulbs:
        try:
            bulb.set_hsv(hue, saturation)
        except yl.BulbException as e:
            pass 
    
    prev_t = time.time()
    return hue, saturation


