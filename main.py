from Controller import Controller
from LightGroup import LightGroup 
import time 

controller = None 

try:
    groups = [LightGroup('bedroom', ['bedroom1'])]
    controller = Controller(groups)
    for group in controller.groups:
        print(group.bulbs)
    
    while True:
        time.sleep(5)
finally:
    controller.stop()