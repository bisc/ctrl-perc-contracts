function [initializedLattice] = initOlegBaseline(dMax,vMax,deltad,deltav)
%initLattice This function creates the lattice structure (2-d array of lattice points)

numPointsDist = ceil(dMax/deltad)+1;
numPointsVel = ceil(vMax/deltav)+1;


for i=1:numPointsDist
    for j=1:numPointsVel
        dist = (i-1)*deltad;
        vel = (j-1)*deltav;
        latticePoint.d = dist;
        latticePoint.did = i;
        latticePoint.v = vel;
        latticePoint.vid = j;
        latticePoint.nextPoints=containers.Map(0,[i j]);
        initLattice(i,j)=latticePoint;
    end
end
initializedLattice = initLattice;

end

