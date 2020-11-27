import numpy as np
from ease_of_live_scripts import *
import json
import matplotlib.pyplot as plt
from pprint import *
import collections

folder_path="exp1125/original parameters/angle data/static angles"
files=list_files(folder_path)
names = 'index, time, power, angle'

def write_angle_voltages():
    with open('exp1125/original parameters/angle data/static angles.josn', 'w') as fo:
        json.dump(angle_voltages, fo)

angle_voltages=collections.OrderedDict()
for file in files:
    data = np.genfromtxt(os.path.join(folder_path, file), skip_header=8, names=names)
    angle_voltages[int(file.split('.')[0])]=np.average(data['angle'])
angle_voltages=collections.OrderedDict(sorted(angle_voltages.items()))
folder_path="exp1125/original parameters/angle data"
data=read(folder_path,'sweep -10 to +10.txt')
plt.figure()
plt.plot(list(angle_voltages.keys()),list(angle_voltages.values()),'.')
plt.figure()
plt.plot(data['index'],data['angle'])
for voltage in list(angle_voltages.values()):
    plt.plot(data['index'],np.ones(len(data['index']))*voltage)
    plt.legend(['voltages']+list(angle_voltages.keys()))
plt.show()