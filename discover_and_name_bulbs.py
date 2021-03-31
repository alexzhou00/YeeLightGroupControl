import yeelight as yl

print("This script will try to connect to all bulbs in your house. \n\
It will set them all to white mode at 40 brightness. \n\
Bulbs to-be-named will be set to full brightness.")

bulb_dicts = yl.discover_bulbs()

bulbs = []

for bulb_dict in bulb_dicts:
    bulbs.append(yl.Bulb(bulb_dict['ip']))

for bulb in bulbs:
    bulb.turn_on()
    bulb.set_power_mode(yl.PowerMode.NORMAL)
    bulb.set_color_temp(4000)
    bulb.set_brightness(40)

for bulb in bulbs:
    bulb.set_brightness(100)
    ans = input("Current name of bulb is '{}'. Would you like to change it? (y/n): ".format(bulb.get_properties()['name']))
    ans = ans.lower 
    if ans == 'y' or ans == 'yes':
        name = input("What would you like the new name to be? ")
        bulb.set_name(name)
    else:
        print("Okay. Skipping...")
    bulb.set_brightness(40)

print("To recap, we have bulbs: ")
for bulb in bulbs:
    print("Bulb named {} with ip {}".format(bulb.get_properties()['name'], bulb._ip))