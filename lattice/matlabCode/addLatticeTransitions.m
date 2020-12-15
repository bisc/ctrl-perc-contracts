function [lattice] = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
latticeSize = size(lattice);

for i=1:latticeSize(1)
    for j=1:latticeSize(2)
        tempCell = lattice(i,j);
        d = tempCell.d;
        v = tempCell.v;
        newMapKey = N;
        newMapValue = zeros(N+1,2);
        for K=0:1:N
            [nextds,nextvs] = computeLatticeTransition(d,v,N,K,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);
            nextds
            nextvs
            [nextds,nextvs] = scrubTransitionsWorstCase(nextds,nextvs);
            latticeTransitions = [];
            nextds
            nextvs
            for iter = size(nextds,1)
                nextd = max(nextds(iter),0);
                nextv = max(nextvs(iter),0);
                nextdid = nextd/deltad+1;
                nextvid = nextv/deltav+1;
                latticeTransitions = [latticeTransitions; nextdid nextvid];
            end
            newMapValue(K+1,:)=latticeTransitions;
        end
        tempCell.nextPoints(newMapKey)=newMapValue;
        lattice(i,j)=tempCell;
    end
end
end

