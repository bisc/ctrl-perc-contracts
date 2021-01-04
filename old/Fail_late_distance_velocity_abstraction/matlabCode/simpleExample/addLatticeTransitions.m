function [lattice] = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh)
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
%         newMapValue = zeros(N+1,2);
        for K=0:1:N
            if(K==3 && i==3 && j==4)
                a=1;
            end
            [nextds,nextvs] = computeLatticeTransition(d,v,N,K,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh);
%             nextds
%             nextvs
            [nextds,nextvs] = scrubTransitionsWorstCase(nextds,nextvs,deltad,deltav);
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
                nextvid = ceil(nextv/deltav)+1;
                
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

