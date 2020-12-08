import numpy as np
import os
import json
from pprint import *
import matplotlib.pyplot as plt
import ease_of_live_scripts as es
from scipy.signal import find_peaks

folder_path="exp1125/original parameters/parameters"
files=[]
parameters={}
names='index, time, power, angle'
for i in os.walk(folder_path):
    files.append(i)
files=files[0][2]
for file in files:
    data=np.genfromtxt(os.path.join(folder_path,file), skip_header=8,names=names)
    plt.figure()
    if file == 'maximum lazer voltage without iris.txt':
        start=900
    else:
        start=0
    if file == 'beam width.txt':
        plt.plot(0.8396455694334474 *np.sin(np.deg2rad((es.volt_to_angle(data['angle'][start:-1])))), np.abs(np.diff(-data['power'][start:])), '.')
        plt.figure()
        indecies=find_peaks(np.abs(-data['power'][start:]), height=0.8)[0]
        plt.plot([0.8396455694334474 *np.sin(np.deg2rad((es.volt_to_angle(data['angle'][start:-1]))))[i] for i in indecies], [-data['power'][start:][i] for i in indecies], 'x')
    else:
        data = data['power'][start:]
        parameters[file.split('.')[0]] = np.average(data)
    plt.plot(0.8396455694334474 *np.sin(np.deg2rad((es.volt_to_angle(data['angle'][start:])))),-data['power'][start:],'.')
    plt.title(file.split('.')[0])
    plt.show()
pprint(parameters)

