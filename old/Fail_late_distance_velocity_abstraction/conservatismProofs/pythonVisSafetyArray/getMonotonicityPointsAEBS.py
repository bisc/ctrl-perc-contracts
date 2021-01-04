
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import itertools


safetyArrayFile = 'C:\\Users\\matth\\eclipse-workspace\\erhts\\src\\main\\java\\PRISMExperimentsJavaMaven\\erhts\\safetyArrayLEC3000SmallDiscretization.txt'
distsArrayFile = 'C:\\Users\\matth\\eclipse-workspace\\erhts\\src\\main\\java\\PRISMExperimentsJavaMaven\\erhts\\distsArrayLEC3000SmallDiscretization.txt'
speedsArrayFile = 'C:\\Users\\matth\\eclipse-workspace\\erhts\\src\\main\\java\\PRISMExperimentsJavaMaven\\erhts\\speedsArrayLEC3000SmallDiscretization.txt'

#safetyArrayFile = 'C:\\Users\\matth\\Downloads\\safetyArraySmallDiscSteepLEC.txt'
#distsArrayFile = 'C:\\Users\\matth\\Downloads\\distsArraySmallDiscSteepLEC.txt'
#speedsArrayFile = 'C:\\Users\\matth\\Downloads\\speedsArraySmallDiscSteepLEC.txt'

with open(safetyArrayFile) as csv_file:
    safetyData = list(csv.reader(csv_file))
#safetyData = list(itertools.chain(*safetyData))
for i in range(0,len(safetyData)):
    safetyData[i] = [float(x) for x in safetyData[i]]
print(np.shape(safetyData))
#print(max(safetyData))

with open(distsArrayFile) as csv_file:
    distData = list(csv.reader(csv_file))
#distData = list(itertools.chain(*distData))
#distData = [float(x) for x in distData]
print(np.shape(distData))


with open(speedsArrayFile) as csv_file:
    speedData = list(csv.reader(csv_file))
#speedData = list(itertools.chain(*speedData))
#speedData = [float(x) for x in speedData]
print(np.shape(speedData))


nonMonotonicSafetyPointDists = []
nonMonotonicSafetyPointSpeeds = []
nonMonotonicSafetyPointSafeties = []

monotonicityViolationCounts = np.zeros(len(safetyData)-1)
monotonicityViolationProbs = np.zeros(len(safetyData)-1)
print(type(distData))
distDataNP = np.array(distData)
dists = distDataNP[:-1,0]
dists = [float(x) for x in dists]

crashData = safetyData
for rowInd in range(1,len(crashData)):
    for colInd in range(0,len(crashData[rowInd])):
        crashVal = crashData[rowInd][colInd]
        if(rowInd==0):
            continue
        prevCrashVal = crashData[rowInd-1][colInd]
        if(crashVal>prevCrashVal):
            # broken assumption about monotonicity of safety
            nonMonotonicSafetyPointSafeties.append(crashVal)
            nonMonotonicSafetyPointDists.append(distData[rowInd][colInd])
            nonMonotonicSafetyPointSpeeds.append(speedData[rowInd][colInd])

            monotonicityViolationCounts[rowInd-1] += 1
            monotonicityViolationProbs[rowInd-1] += crashVal-prevCrashVal

nonMonotonicSafetyPointSafeties = [float(x) for x in nonMonotonicSafetyPointSafeties]
nonMonotonicSafetyPointDists = [float(x) for x in nonMonotonicSafetyPointDists]
nonMonotonicSafetyPointSpeeds = [float(x) for x in nonMonotonicSafetyPointSpeeds]
print(np.shape(nonMonotonicSafetyPointSafeties))
print(np.shape(nonMonotonicSafetyPointDists))
print(np.shape(nonMonotonicSafetyPointSpeeds))

print(min(nonMonotonicSafetyPointDists))
print(max(nonMonotonicSafetyPointDists))

print(min(nonMonotonicSafetyPointSpeeds))
print(max(nonMonotonicSafetyPointSpeeds))

for i in range(0,5):
    print(nonMonotonicSafetyPointSafeties[i])
    print(nonMonotonicSafetyPointDists[i])
    print(nonMonotonicSafetyPointSpeeds[i])

#print(nonMonotonicSafetyPointDists)
#print(nonMonotonicSafetyPointSpeeds)



fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_xlim3d(min(nonMonotonicSafetyPointDists), max(nonMonotonicSafetyPointDists))
ax.set_ylim3d(min(nonMonotonicSafetyPointSpeeds),max(nonMonotonicSafetyPointSpeeds))
ax.set_zlim3d(0,1)
z_points = nonMonotonicSafetyPointSafeties
x_points = nonMonotonicSafetyPointDists
y_points = nonMonotonicSafetyPointSpeeds
#print(type(z_points))
ax.scatter3D(x_points, y_points, z_points, c=z_points, cmap='hsv')
plt.gca().set(title='Probability of Crashing', xlabel='Initial Distance',ylabel='Initial Speed')
#plt.show()


fig = plt.figure()
detectionMin = 5000
detectProbsByDists = []
for dist in nonMonotonicSafetyPointDists:
    if(dist>detectionMin):
        detProb = 0
    else:
        detProb = 1-(dist/detectionMin)
    detectProbsByDists.append(detProb)
plt.plot(nonMonotonicSafetyPointDists,detectProbsByDists,'r+')
#plt.show()

print(len(dists))
print(len(monotonicityViolationCounts))
print(len(monotonicityViolationProbs))

plt.subplot(2,1,1)
plt.plot(dists,monotonicityViolationCounts)
plt.title('Monotonicity Count Violations By Distance')
#plt.xlabel('Distance (0.01m)')
plt.ylabel('Count')

plt.subplot(2,1,2)
plt.plot(dists,monotonicityViolationProbs)
plt.title('Monotonicity Probability Violation Sums By Distance')
plt.xlabel('Distance (0.01m)')
distTicks = np.arange(min(dists),max(dists),10000)
plt.xticks(distTicks)

plt.ylabel('Probability')

plt.show()

