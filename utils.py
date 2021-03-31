import yeelight as yl
import time
from Bulb import Bulb

def read_file_to_dict(filename):
    f = open(filename, "r+")
    lines = f.readlines() 
    d = {}

    for line in lines:
        if line == '':
            continue
        attr, vals = line.split(":")
        vals = vals.strip()
        vals = vals.split(",")
        d[attr] = vals if len(vals) > 1 else vals[0]
    f.close()
    return d

def write_dict_to_file(filename, d):
    f = open(filename, "w+")

    for attr in d:
        f.write("{}: ".format(attr))
        if type(d[attr]) is list:
            l = d[attr]
            f.write(str(l[0]))
            for i in range(1, len(l)):
                f.write(',')
                f.write(str(l[i]))
        else:
            f.write(str(d[attr]))
        f.write('\n')
    
    f.close()