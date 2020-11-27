import numpy as np
import os
import json
from pprint import *
import matplotlib.pyplot as plt

folder_path="exp1125/original parameters"
files=[]
parameters={}
names='index, time, power, angle'
for i in os.walk(folder_path):
    files.append(i)
files=files[0][2]
for file in files:
    data=np.genfromtxt(os.path.join(folder_path,file), skip_header=8,names=names)
    if file == 'maximum lazer voltage without iris.txt':
        start=900
    else:
        start=0
    plt.figure()
    plt.plot(data['index'][start:],data['ch0'][start:])
    plt.title(file.split('.')[0])
    plt.show()
    if file == 'beam width.txt':
        pass
    else:
        data = data['ch0'][start:]
        parameters[file.split('.')[0]] = np.average(data)
pprint(parameters)