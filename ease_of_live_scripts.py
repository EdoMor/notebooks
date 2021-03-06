import os
import numpy as np
from typing import Callable
from scipy.special import erf, erfi, sici
import matplotlib.pyplot as plt

np.set_printoptions(precision=17)

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


def read(folder: str, file: str):
    '''
    read D-scope file
    '''
    return np.genfromtxt(os.path.join(folder, file), skip_header=8, names=names)


offset = np.mean(read('exp1125/original parameters/angle data/', 'offset.txt')['angle'])


def Rsquared(xdata: list, ydata: list, funciton: Callable, popt: np.ndarray):
    '''calculate R^2'''
    residual_sum_of_squares = np.sum((np.array(ydata) - funciton(np.array(xdata), *popt)) ** 2)
    total_sum_of_squares = np.sum((np.array(ydata) - np.mean(ydata)) ** 2)
    return 1 - (residual_sum_of_squares / total_sum_of_squares)


def csc(x):
    return 1 / np.sin(x)


def single_slit_model(x, A, z, d, wl, offset):
    return A * (2 * z * np.sin((d * (2 * np.pi / wl) * (x - offset)) / (2 * z)) ** 2) / (
            (2 * np.pi / wl) * np.pi * (x - offset) ** 2)


def single_slit_model_redunced(xp, xp0, p2):
    return ((np.sin(xp - xp0) ** 2) / ((xp - xp0) ** 2)) * p2


def single_slit_model_with_integration(x, A, z, d, wl, s, offset):
    return A * (2 * z * (-(z - z * np.cos((d * (2 * np.pi / wl) * (s - (x - offset))) / z) + d * (2 * np.pi / wl) * (
            s - (x - offset)) * sici((d * (2 * np.pi / wl) * (-s + (x - offset))) / z)[0]) / (
                                 2. * (s - (x - offset)) * z) + (
                                 (-1 + np.cos((d * (2 * np.pi / wl) * (s + (x - offset))) / z)) / (
                                 s + (x - offset)) + (
                                         d * (2 * np.pi / wl) *
                                         sici((d * (2 * np.pi / wl) * (s + (x - offset))) / z)[0]) / z) / 2.)) / (
                   (2 * np.pi / wl) * np.pi)


def single_slit_near_field_model(x, A, z, d, wl, offset):
    return np.real(A * (-0.25j * (erf((0.25 + 0.25j) * (d - 2 * (x - offset)) * np.sqrt(((2 * np.pi) / wl) / z)) + erf(
        (0.25 + 0.25j) * (d + 2 * (x - offset)) * np.sqrt(((2 * np.pi) / wl) / z))) * (erfi(
        (0.25 + 0.25j) * (d - 2 * (x - offset)) * np.sqrt(((2 * np.pi) / wl) / z)) + erfi(
        (0.25 + 0.25j) * (d + 2 * (x - offset)) * np.sqrt(((2 * np.pi) / wl) / z)))))


def double_slit_model(x, p1, p2, offset):
    '''

    :param x'=pi*L/wl*z*x:
    :param p1=d/L:
    :param p2=wl*z/4*A*L:
    :param offset'=pi*L/wl*z*x*offset:
    :return:
    '''
    return ((np.cos(x - offset)) ** 2 * (np.sin(p1 * (x - offset))) ** 2) / (p2 * (x - offset) ** 2)


def n_slits_model(x, A, z, d, wl, L, n, offset):
    return A * (2 * z * csc(((2 * np.pi / wl) * L * (x - offset)) / (2 * z)) ** 2 * np.sin(
        (d * (2 * np.pi / wl) * (x - offset)) / (2 * z)) ** 2 * np.sin(
        ((2 * np.pi / wl) * L * (1 + 2 * n) * (x - offset)) / (2 * z)) ** 2) / (
                   (2 * np.pi / wl) * np.pi * (x - offset) ** 2)


def model_integrate(xdata, model, s, p1, p2, of):
    '''
    used to create a model function with integration

    :param xdata:
    :param model: model function
    :param s: integration width
    :param args: additional model arguments
    :return: integrative model function
    '''
    ydata=np.zeros(len(xdata))
    for i in range(len(xdata)):
        v = np.linspace(xdata[i] - s / 2, xdata[i] + s / 2, 1000)
        for j in v:
            ydata[i] += (model(j+1, p1, p2, of)-model(j, p1, p2, of))/2*(s/1000)
    return ydata


def volt_to_angle(data: list):
    '''

    :param data:
    :return: angle in degrees
    '''
    return (1 / (-0.16758777796461088)) * np.array(data) - (0.00218044751831026 / (-0.16758777796461088))


def add_subplot_minimap(ax, rect):
    '''
    add a miniplot to a subplot ax

    :param ax: subplot

    :param rect: a list [x,y,sx,sy] where x,y are the location of the lower left corner of the miniplot and sx,sy are the side length

    :return: miniplot object

    Example
    -------
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> plt.plot(xdata,ydata) #this is the main plot
    >>> ax1 = es.add_subplot_minimap(ax,[0.7,0.7,0.3,0.3])
    >>> ax1.plot(minixdata,miniydata) #this plots the minimap
    >>> plt.show()
    '''
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x, y, width, height])
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2] ** 0.5
    y_labelsize *= rect[3] ** 0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax
