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

def csc(x):
    return 1/np.sin(x)

def single_slit_model(x,A,z,d,k):
    return A*(2*z*np.sin((d*k*x)/(2*z))**2)/(k*np.pi*x**2)

def double_slit_model(x,A,z,d,k,L):
    return A*(8*z*np.cos((k*L*x)/(2*z))**2*np.sin((d*k*x)/(2*z))**2)/(k*np.pi*x**2)

def n_slits_model(x,A,z,d,k,L,n):
    return A*(2*z*csc((k*L*x)/(2*z))**2*np.sin((d*k*x)/(2*z))**2*np.sin((k*L*(1 + 2*n)*x)/(2*z))**2)/(k*np.pi*x**2)
