



numBins = 19

print("    [] seqflag=-1&tankflagPer=1&sink=0 ->",end="")
for i in range(numBins):
    print(" 0.8*" + str(1/numBins) + ": " + "(wl1Per'=wl1+" + str(int ((numBins-1)/2)) + "-" + str(i) + ")&(seqflag'=-1)&(tankflagPer'=2) +",end="")


print(";")


print("    [] seqflag=-1&tankflagPer=2&sink=0 ->",end="")
for i in range(numBins):
    print(" 0.8*" + str(1/numBins) + ": " + "(wl2Per'=wl2+" + str(int ((numBins-1)/2)) + "-" + str(i) + ")&(seqflag'=0)&(tankflagPer'=1) +",end="")


print(";")

