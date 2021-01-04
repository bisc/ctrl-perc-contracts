
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import itertools

#safetyArrayFile = 'C:\\Users\\matth\\eclipse-workspace\\erhts\\src\\main\\java\\PRISMExperimentsJavaMaven\\erhts\\safetyArrayLEC10000SmallDiscretization.txt'
#distsArrayFile = 'C:\\Users\\matth\\eclipse-workspace\\erhts\\src\\main\\java\\PRISMExperimentsJavaMaven\\erhts\\distsArrayLEC10000SmallDiscretization.txt'
#speedsArrayFile = 'C:\\Users\\matth\\eclipse-workspace\\erhts\\src\\main\\java\\PRISMExperimentsJavaMaven\\erhts\\speedsArrayLEC10000SmallDiscretization.txt'

safetyArrayFile = "C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\lattice\\\\conservatismProofs\\\\PRISMExperiments\\\\ForPaper\\\\AEBSdiscreteLECsafetyProbs.txt"
distsArrayFile = "C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\lattice\\\\conservatismProofs\\\\PRISMExperiments\\\\ForPaper\\\\AEBSdiscreteLECdistsArraysafetyProbs.txt"
speedsArrayFile = "C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\lattice\\\\conservatismProofs\\\\PRISMExperiments\\\\ForPaper\\\\AEBSdiscreteLECspeedsArraysafetyProbs.txt"

with open(safetyArrayFile) as csv_file:
    safetyData = list(csv.reader(csv_file))
safetyData = list(itertools.chain(*safetyData))
safetyData = [float(x) for x in safetyData]
print(np.shape(safetyData))
print(max(safetyData))

with open(distsArrayFile) as csv_file:
    distData = list(csv.reader(csv_file))
distData = list(itertools.chain(*distData))
distData = [float(x) for x in distData]
print(np.shape(distData))


with open(speedsArrayFile) as csv_file:
    speedData = list(csv.reader(csv_file))
speedData = list(itertools.chain(*speedData))
speedData = [float(x) for x in speedData]
print(np.shape(speedData))


fig = plt.figure()
ax = plt.axes(projection="3d")
z_points = safetyData
x_points = distData
y_points = speedData
#print(type(z_points))
ax.scatter3D(x_points, y_points, z_points, c=z_points, cmap='hsv')
plt.gca().set(title='Probability of Crashing Less Steep LEC', xlabel='Initial Distance',ylabel='Initial Speed')
plt.show()


