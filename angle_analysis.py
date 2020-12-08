import numpy as np
from ease_of_live_scripts import *
import json
import matplotlib.pyplot as plt
from pprint import *
import collections
from scipy import optimize as fit
import seaborn as sbs

np.set_printoptions(precision=17)

folder_path = "exp1125/original parameters/angle data/static angles"
files = list_files(folder_path)
names = 'index, time, power, angle'


def write_angle_voltages():
    with open('exp1125/original parameters/angle data/static angles.josn', 'w') as fo:
        json.dump(angle_voltages, fo)

def draw_plots(xdata,ydata,error):
    sbs.set()
    plt.subplot(211)
    plt.plot(xdata, ydata, '.')
    plt.plot(xdata, parameters_optimized[0] * xdata + parameters_optimized[1])
    plt.legend(['meshured data', 'fitted data'])
    plt.xlabel('angle[deg]')
    plt.ylabel('voltage[Volt]')
    plt.title('angle vs voltage')
    ax = plt.subplot(212)
    plt.errorbar(xdata, ydata - (parameters_optimized[0] * xdata + parameters_optimized[1]),yerr=error ,fmt='.')
    plt.xlabel('angle[deg]')
    plt.ylabel('voltage[Volt]')
    plt.title('residuals')
    plt.show()


angle_voltages = collections.OrderedDict()
angle_meshurment_errors = collections.OrderedDict()
for file in files:
    data = np.genfromtxt(os.path.join(folder_path, file), skip_header=8, names=names)
    angle_voltages[int(file.split('.')[0])] = np.average(data['angle'])
    angle_meshurment_errors[int(file.split('.')[0])] = (np.max(data['angle'])-np.min(data['angle']))
angle_voltages = collections.OrderedDict(sorted(angle_voltages.items()))
angle_meshurment_errors = collections.OrderedDict(sorted(angle_meshurment_errors.items()))
xdata=np.array(list(angle_voltages.keys()))
ydata=np.array(list(angle_voltages.values()))
parameters_optimized, parameters_covariance=fit.curve_fit(lambda x,a,b: a*x+b, xdata, ydata)
error=np.max(list(angle_meshurment_errors.values()))
print(np.float64(parameters_optimized))
draw_plots(xdata,ydata,error)