
#!/bin/bash


for f in latticeModels/N3H3L3d15/bobLattice/*
do
	echo "Processing $f"
	#cat olegModels/olegBaselineLECModelH3L3DistDisc0.25.prism >> $f
	cat LECModel/boblatticeForScalability-N3H3L3-deltaD1.5.prism >> $f
done

