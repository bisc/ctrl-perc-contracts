function [lattice] = addOlegBaselineTransitions(lattice,N,deltad,deltav,B,freq,safetyThresh)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
format long
latticeSize = size(lattice);

for i=1:latticeSize(1)
    for j=1:latticeSize(2)
        tempCell = lattice(i,j);
        d = tempCell.d;
        v = tempCell.v;
        newMapKey = N;
        clear newMapValue
        for K=0:1:N
            [nextds,nextvs] = computeOlegBaselineTransition(d,v,N,K,deltad,deltav,B,freq,safetyThresh);
%             nextds
%             nextvs
%             [nextds,nextvs] = scrubTransitionsWorstCase(nextds,nextvs);
            latticeTransitions = [];
%             nextds
%             nextvs
            if(length(nextvs)>1)
                a = 1;
            end
            for iter = 1:length(nextds)
                nextd = max(nextds(iter),0);
                nextv = max(nextvs(iter),0);
                nextdid = floor(nextd/deltad)+1;
                nextvid = floor(nextv/deltav)+1;
                
%                 crashdid = ceil(safetyThresh/deltad);
%                 if(nextd>safetyThresh && nextv<=0 && nextdid<=crashdid)
%                     nextvid=1;
%                     nextdid=crashdid+1;
%                 end
                latticeTransitions = [latticeTransitions; nextdid nextvid];
            end
            newMapValue{K+1}=latticeTransitions;
        end
        tempCell.nextPoints(newMapKey)=newMapValue;
        lattice(i,j)=tempCell;
    end
end
end

