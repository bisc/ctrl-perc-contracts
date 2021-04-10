import numpy as np
import math






# load data
dists = np.load('vehicleDists.npy')
confs = np.load('LECconfidences.npy')


confThresh = 0.6

maxDist = 200
minDist = 0
distDisc = 10


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

# combine into final model
finalDetectionProbs = np.zeros(len(detectionsByDist))

for index in range(len(detectionsByDist)):
    finalDetectionProbs[index] = detectionsByDist[index]/(detectionsByDist[index]+misdetectionsByDist[index])
    print(detectionsByDist[index]+misdetectionsByDist[index])

f = open('PRISMLECModel.txt', 'w')

for index in range(len(detectionsByDist)):
    detProb = finalDetectionProbs[index]
    if math.isnan(detProb):
        detProb = 0.0
    #if detProb>=0.1:
    #    detProb=detProb-0.1
    distLower = (index*distDisc)
    distUpper = ((index+1)*distDisc)
    modelLine = "    [] seqflag=1&carPos<" + str(distUpper) + "&carPos>=" + str(distLower)+ " -> " + str(detProb) + ":(s'=0)&(seqflag'=2)+ " + str(1-detProb) + ":(s'=1)&(seqflag'=2);\n"
    #print(modelLine)
    f.write(modelLine)
f.close()