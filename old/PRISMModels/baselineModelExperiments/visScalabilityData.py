import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits import mplot3d







probs = []
dists = [120,130,140,150,160,170,180]
speeds = [10,14,18,22,26,30]
X,Y = np.meshgrid(dists,speeds)
baselineCrashProbs = []
with open('scalabilityData/crashProbsBaselined1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(csv_reader)
    for row in csv_reader:
        row = [float(row_) for row_ in row]
        print(row)
        baselineCrashProbs.append(row)
print(baselineCrashProbs)


baselineRuntimes = []
with open('scalabilityData/runtimesBaselined1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(csv_reader)
    for row in csv_reader:
        row = [float(row_) for row_ in row]
        print(row)
        baselineRuntimes.append(row)
print(baselineRuntimes)



print(X)
print(Y)
# ax = plt.axes(projection='3d')
# ax.scatter3D(X, Y, baselineRuntimes, cmap='Greens')




lattice175CrashProbs = []
with open('scalabilityData/crashProbs175.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(csv_reader)
    for row in csv_reader:
        row = [float(row_) for row_ in row]
        print(row)
        lattice175CrashProbs.append(row)
print(lattice175CrashProbs)


lattice175Runtimes = []
with open('scalabilityData/runTimes175.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(csv_reader)
    for row in csv_reader:
        row = [float(row_) for row_ in row]
        print(row)
        lattice175Runtimes.append(row)
print(lattice175Runtimes)



print(X)
print(Y)

ax = plt.axes(projection='3d')
ax.scatter3D(X, Y, baselineCrashProbs, cmap='Greens')
ax.scatter3D(X, Y, lattice175CrashProbs)
plt.xlabel('Initial Distance (m)')
plt.ylabel('Initial Speed (m/s)')
# plt.zlabel('Crash Chance')
plt.title('Computed Crash Probabilities')
plt.show()

ax = plt.axes(projection='3d')
ax.scatter3D(X, Y, baselineRuntimes, cmap='Greens')
ax.scatter3D(X, Y, lattice175Runtimes)
plt.xlabel('Initial Distance (m)')
plt.ylabel('Initial Speed (m/s)')
# plt.zlabel('Runtime (ns)')
plt.title('Modle Checking Runtimes')
plt.show()
# ax = plt.axes(projection='3d')
# ax.scatter3D(X, Y, lattice175Runtimes, cmap='Greens')

# ax = plt.axes(projection='3d')
# ax.scatter3D(X, Y, baselineRuntimes-lattice175Runtimes, cmap='Greens')

plt.show()
