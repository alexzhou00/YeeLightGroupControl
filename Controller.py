from LightGroup import LightGroup 
import yeelight as yl
from pynput import keyboard
import time

class Controller():
    def __init__(self, groups):
        self.active = [True, False, False, False, False]
        self.alt = False
        self.groups = groups
        self.presets = []
        self.listener = keyboard.Listener(
            on_press = lambda key: self.on_press(key),
            on_release = lambda key: self.on_release(key)
        )
        self.light_layer = False 
        self.group_layer = False
        self.preset_layer = False 
        self.light_mode = self.groups[0].mode
        self.music_mode = False
        self.last_used = time.time()
        self.listener.start()

    def toggle(self):
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].toggle()
    
    def set_mode(self, mode):
        self.light_mode = mode
        time.sleep(0.2)
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].set_brightness(self.groups[i].brightness)
        time.sleep(0.2)
        if mode == yl.PowerMode.NORMAL:
            for i in range(len(self.groups)):
                if self.active[i]:
                    self.groups[i].set_color_temp(self.groups[i].degrees)
            self.turn_off_music_mode()
        elif mode == yl.PowerMode.RGB:
            for i in range(len(self.groups)):
                if self.active[i]:
                    self.groups[i].set_rgb(self.groups[i].r, self.groups[i].g, self.groups[i].b)
        elif mode == yl.PowerMode.HSV:
            for i in range(len(self.groups)):
                if self.active[i]:
                    self.groups[i].set_hsv(self.groups[i].h, self.groups[i].s)

    def sync(self):
        grp = None
        for i in range(len(self.groups)):
            if self.active[i]:
                grp = i 
        
        if grp is not None and len(self.groups) > grp+1:
            for i in range(grp+1, len(self.groups)):
                if self.active[i]:
                    self.groups[i].brightness = self.groups[grp].brightness
                    if self.light_mode == yl.PowerMode.NORMAL:
                        self.groups[i].degrees = self.groups[grp].degrees
                    elif self.light_mode == yl.PowerMode.RGB:
                        self.groups[i].r = self.groups[grp].r
                        self.groups[i].g = self.groups[grp].g
                        self.groups[i].b = self.groups[grp].b
                    elif self.light_mode == yl.PowerMode.HSV:
                        self.groups[i].h = self.groups[grp].h
                        self.groups[i].s = self.groups[grp].s

    def incr_brightness(self, step=5):
        self.ensure_music_mode()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].incr_brightness(step)
    
    def decr_brightness(self, step=5):
        self.ensure_music_mode()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].decr_brightness(step)
    
    def incr_color_temp(self, step=50):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].incr_color_temp(step)
    
    def decr_color_temp(self, step=50):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].decr_color_temp(step)

    def incr_r(self, step=5):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].incr_r(step)

    def incr_g(self, step=5):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].incr_g(step)

    def incr_b(self, step=5):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].incr_b(step)

    def decr_r(self, step=5):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].decr_r(step)
    
    def decr_g(self, step=5):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].decr_g(step)
    
    def decr_b(self, step=5):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].decr_b(step) 

    def incr_hue(self, step=8):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].incr_hue(step)
    
    def incr_saturation(self, step=5):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].incr_saturation(step)
    
    def decr_hue(self, step=8):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].decr_hue(step)
    
    def decr_saturation(self, step=5):
        self.ensure_music_mode()
        self.sync()
        for i in range(len(self.groups)):
            if self.active[i]:
                self.groups[i].decr_saturation(step) 
    
    def toggle_group(self, group):
        self.active[group] = not self.active[group]
    
    def ensure_music_mode(self):
        self.last_used = time.time()
        self.music_mode = True 
        for group in self.groups:
            group.toggle_music_mode(1)
    
    def turn_off_music_mode(self):
        if self.music_mode:
            for group in self.groups:
                group.toggle_music_mode('0')
        self.music_mode = False
    
    def activate_preset(self, preset):
        pass

    def set_default(self):
        pass

    def reset_default(self):
        pass 

    def reconnect(self):
        pass

    def on_press(self, key):
        if key == keyboard.Key.alt or key == keyboard.Key.alt_l:
            self.alt = True

        if not self.light_layer:
            if key == keyboard.Key.f13:
                self.decr_brightness()
            elif key == keyboard.Key.f14:
                self.incr_brightness()
            elif key == keyboard.Key.f15:
                self.light_layer = True 
                self.preset_layer = False 
                self.group_layer = False
            elif key == keyboard.Key.f16:
                self.toggle()
            else:
                self.turn_off_music_mode()
        else:
            if self.alt:
                if self.group_layer:
                    if key == keyboard.Key.f13:
                        self.toggle_group(0)
                    elif key == keyboard.Key.f14:
                        self.toggle_group(1)
                    elif key == keyboard.Key.f15:
                        self.toggle_group(2)
                    elif key == keyboard.Key.f16:
                        self.toggle_group(3)
                    elif key == keyboard.Key.f17:
                        self.toggle_group(4)
                    elif key == keyboard.Key.f18:
                        self.group_layer = False
                elif self.preset_layer:
                    if key == keyboard.Key.f13:
                        self.activate_preset(0)
                    elif key == keyboard.Key.f14:
                        self.activate_preset(1)
                    elif key == keyboard.Key.f15:
                        self.activate_preset(2)
                    elif key == keyboard.Key.f16:
                        self.activate_preset(3)
                    elif key == keyboard.Key.f17:
                        self.activate_preset(4)
                    elif key == keyboard.Key.f18:
                        self.preset_layer = False
                else:
                    if key == keyboard.Key.f13:
                        self.group_layer = True 
                    elif key == keyboard.Key.f14:
                        self.toggle()
                    elif key == keyboard.Key.f15:
                        self.set_default()
                    elif key == keyboard.Key.f16:
                        self.preset_layer = True 
                    elif key == keyboard.Key.f17:
                        self.reconnect()
                    elif key == keyboard.Key.f18:
                        self.light_layer = False
            else:
                if self.light_mode == yl.PowerMode.NORMAL:
                    if key == keyboard.Key.f13:
                        self.decr_brightness()
                    elif key == keyboard.Key.f14:
                        self.incr_brightness()
                    elif key == keyboard.Key.f15:
                        self.decr_color_temp()
                    elif key == keyboard.Key.f16:
                        self.incr_color_temp() 
                    elif key == keyboard.Key.f17:
                        self.decr_brightness()
                    elif key == keyboard.Key.f18:
                        self.incr_brightness()
                    elif key == keyboard.Key.f19:
                        self.reset_default()
                    elif key == keyboard.Key.f20:
                        self.set_mode(yl.PowerMode.RGB)
                    elif key == keyboard.Key.f21:
                        self.set_mode(yl.PowerMode.HSV)
                elif self.light_mode == yl.PowerMode.RGB:
                    if key == keyboard.Key.f13:
                        self.decr_r()
                    elif key == keyboard.Key.f14:
                        self.incr_r()
                    elif key == keyboard.Key.f15:
                        self.decr_g()
                    elif key == keyboard.Key.f16:
                        self.incr_g() 
                    elif key == keyboard.Key.f17:
                        self.decr_b()
                    elif key == keyboard.Key.f18:
                        self.incr_b()
                    elif key == keyboard.Key.f19:
                        self.set_mode(yl.PowerMode.NORMAL)
                    elif key == keyboard.Key.f20:
                        self.reset_default()
                    elif key == keyboard.Key.f21:
                        self.set_mode(yl.PowerMode.HSV)
                elif self.light_mode == yl.PowerMode.HSV:
                    if key == keyboard.Key.f13:
                        self.decr_hue()
                    elif key == keyboard.Key.f14:
                        self.incr_hue()
                    elif key == keyboard.Key.f15:
                        self.decr_saturation()
                    elif key == keyboard.Key.f16:
                        self.incr_saturation() 
                    elif key == keyboard.Key.f17:
                        self.decr_brightness()
                    elif key == keyboard.Key.f18:
                        self.incr_brightness()
                    elif key == keyboard.Key.f19:
                        self.set_mode(yl.PowerMode.NORMAL)
                    elif key == keyboard.Key.f20:
                        self.set_mode(yl.PowerMode.RGB)
                    elif key == keyboard.Key.f21:
                        self.reset_default()

    def on_release(self, key):
        if key == keyboard.Key.alt or key == keyboard.Key.alt_l:
            self.alt = False 
    
    def stop(self):
        self.listener.stop()
        self.turn_off_music_mode()
        for group in self.groups:
            group.save_state()
