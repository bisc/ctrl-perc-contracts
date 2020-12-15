
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import itertools

monotonicityViolationCountsByDistFile = 'monotonicityViolationCountsByDist.txt'
monotonicityViolationProbsByDists = 'monotonicityViolationProbsByDists.txt'

dists = []
for i in range(1025,4000,25):
    print(i)
    dists.append(i)

with open(monotonicityViolationCountsByDistFile) as csv_file:
    monotonicityViolationCounts = list(csv.reader(csv_file))
monotonicityViolationCounts = list(itertools.chain(*monotonicityViolationCounts))
monotonicityViolationCounts = [float(x) for x in monotonicityViolationCounts]

with open(monotonicityViolationProbsByDists) as csv_file:
    monotonicityViolationProbs = list(csv.reader(csv_file))
monotonicityViolationProbs = list(itertools.chain(*monotonicityViolationProbs))
monotonicityViolationProbs = [float(x) for x in monotonicityViolationProbs]
#print(np.shape(distData))

plt.subplot(2,1,1)
plt.plot(dists,monotonicityViolationCounts)
plt.title('Monotonicity Count Violations By Distance')
#plt.xlabel('Distance (0.01m)')
plt.ylabel('Count')

plt.subplot(2,1,2)
plt.plot(dists,monotonicityViolationProbs)
plt.title('Monotonicity Probability Violation Sums By Distance')
plt.xlabel('Distance (0.01m)')
plt.ylabel('Probability')

plt.show()