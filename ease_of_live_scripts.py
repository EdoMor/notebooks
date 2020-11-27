import os
import numpy as np

names='index, time, power, angle'

def list_files(path):
    files = []
    for i in os.walk(path):
        files.append(i)
    files = files[0][2]
    return files

def read(folder,file):
    return np.genfromtxt(os.path.join(folder, file), skip_header=8, names=names)