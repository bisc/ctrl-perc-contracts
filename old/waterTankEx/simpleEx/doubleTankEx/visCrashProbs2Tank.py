from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


import csv

folderName = './surfPlots/'
crashProbs = []
runTimes = []

# waterLevels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
# waterLevels = [1,10,15,30,40,46,48]
waterLevels = [1,3,5,10,15,20,25,30,35,40,45,47,49]
extraString = 'TwoTank_cont00'

for i in range(len(waterLevels)):
    temp = []
    for j in range(len(waterLevels)):
        temp.append(0)
    crashProbs.append(temp)

with open(folderName + 'crashProbs' + extraString + '.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        row_count = 0
        for prob in row:
            crashProbs[line_count][row_count] = float(prob)
            row_count+=1
        line_count+=1

for i in range(len(crashProbs)):
    for j in range(len(crashProbs)):
        if j>i:
            crashProbs[i][j] = crashProbs[j][i]
            # crashProbs[j].append(crashProbs[i][j])


## Contour Plot
# X,Y = np.meshgrid(waterLevels,waterLevels)
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.contour3D(X, Y, crashProbs, 50, cmap='binary')
# ax.set_xlabel('Tank 1 Water Level')
# ax.set_ylabel('Tank 2 Water Level')
# ax.set_zlabel('Probability of Unsafe')

# plt.show()


## Surface Plot
X,Y = np.meshgrid(waterLevels,waterLevels)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, np.array(crashProbs), rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.set_xlabel('Tank 1 Water Level')
ax.set_ylabel('Tank 2 Water Level')
ax.set_zlabel('Probability of Unsafe')

plt.show()
