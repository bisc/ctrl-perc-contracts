import math
import numpy




l = 3
k=3
for i in range(2**l):
    sVals = []
    print(i)
    for sVal in range(l):
        tempSVal = math.floor((i/(2**sVal)) % 2)
        sVals.append(tempSVal)
    sVals.reverse()
    print(sVals)

    for kIter in range(2**k):
        seqsFailed = []
        for tempKVal in range(k):
            tempKVal = math.floor((kIter/(2**tempKVal)) % 2)
            seqsFailed.append(tempKVal)
        seqsFailed.reverse()
        print(seqsFailed)

        for iNext in range(2**l):
            nextIVals = []
            for tempIVal in range(l):
                tempIVal = math.floor((iNext/(2**tempIVal)) % 2)
                nextIVals.append(tempIVal)
            nextIVals.reverse()
            print(nextIVals)

            # nextProbString = probArray(i,k,iNext)
            print("Prev LEC values were: ")
            for j in range(l):
                print("s" + str(i-j) + "=" + str(sVals[j])+ ",")
            print("Seq Pass/Fail values are: ")
            for j in range(k):
                print("k" + str(k-j) + "=" + str(seqsFailed[j])+ ",")
            print("Next prev LEC values are: ")
            for j in range(l):
                print("s" + str(i-j) + "=" + str(nextIVals[j])+ ",")
            print("\n\n")



Solving for m=2 l=1 ks={1, 2, 2} ns={3, 4, 3}
0: {(1 - p0)^4 + 3*(1 - p0)^2*p0*(1 - p1) + p0^2*(1 - p1)^2, (1 - p0)^3*p0 + 2*(1 - p0)*p0^2*(1 - p1) + (1 - p0)^2*p0*p1 + p0^2*(1 - p1)*p1}, {0, 0}, {0, 0}, {0, 0}, {2*(1 - p0)*p0*(1 - p1)*p1, p0^2*(1 - p1)*p1}, {0, 0}, {0, (1 - p0)*p0*p1^2}, {p0*(1 - p1)*p1^2, p0*p1^3}
1: {(1 - p0)^3*(1 - p1) + 2*(1 - p0)*p0*(1 - p1)^2, (1 - p0)^2*p0*(1 - p1) + p0^2*(1 - p1)^2 + (1 - p0)*p0*(1 - p1)*p1}, {0, 0}, {0, 0}, {0, 0}, {(1 - p0)^2*(1 - p1)*p1 + 2*p0*(1 - p1)^2*p1, (1 - p0)*p0*(1 - p1)*p1}, {0, 0}, {0, 2*p0*(1 - p1)*p1^2}, {(1 - p0)*(1 - p1)*p1^2 + (1 - p1)*p1^3, p0*(1 - p1)*p1^2 + p1^4}
