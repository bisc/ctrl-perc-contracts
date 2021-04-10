import numpy as np
import matplotlib.pyplot as plt
import math

# load data
dists = np.load('vehicleDists.npy')
confs = np.load('LECconfidences.npy')

print(len(dists))
print(len(confs))

if(len(confs) != len(dists)):
    raise Exception('Array lengths not equal. CODE BETTER!')


confThreshs = (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99)

print(max(dists))

maxDist = 200
minDist = 0
distDisc = 10


for confThresh in confThreshs:
    detectionsByDist = np.zeros(math.ceil((maxDist-minDist)/distDisc))
    misdetectionsByDist = np.zeros(math.ceil((maxDist-minDist)/distDisc))


    for i in range(len(confs)):
        conf = confs[i]
        dist = dists[i]

        # compute array index
        distArrayIndex = math.floor(dist/distDisc)

        if(conf >= confThresh):
            # Detection
            detectionsByDist[distArrayIndex] += 1
        else:
            misdetectionsByDist[distArrayIndex] += 1

    plt.clf()
    plt.plot(detectionsByDist)
    plt.savefig('detectionsByDist.png')

    plt.clf()
    plt.plot(misdetectionsByDist)
    plt.savefig('misdetectionsByDist.png')

    # combine into final model
    finalDetectionProbs = np.zeros(len(detectionsByDist))

    for index in range(len(detectionsByDist)):
        finalDetectionProbs[index] = detectionsByDist[index]/(detectionsByDist[index]+misdetectionsByDist[index])
        print(detectionsByDist[index]+misdetectionsByDist[index])

    #print(len(finalDetectionProbs))
    detectionDists = range(math.floor(minDist+distDisc/2),math.floor(maxDist+distDisc/2),distDisc)
    plt.clf()
    plt.plot(detectionDists,finalDetectionProbs)
    plt.savefig('finalDetectionProbsByDist_conf%03d.png' % (confThresh*100))
