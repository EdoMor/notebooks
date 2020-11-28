import os
import numpy as np
from typing import Callable


names = 'index, time, power, angle'


def list_files(path: str):
    '''
    list files under path (dose not search subdirectories)
    '''
    files = []
    for i in os.walk(path):
        files.append(i)
    files = files[0][2]
    return files


def read(folder:str, file:str):
    '''
    read D-scope file
    '''
    return np.genfromtxt(os.path.join(folder, file), skip_header=8, names=names)

def function():
    pass
function=function()
def Rsquared(x: list, data: list, funciton: Callable , popt: np.ndarray):
    '''calculate R^2'''
    residual_sum_of_squares = np.sum((np.array(data) - funciton(np.array(x), *popt)) ** 2)
    total_sum_of_squares = np.sum((np.array(data) - np.mean(data)) ** 2)
    return 1 - (residual_sum_of_squares / total_sum_of_squares)
