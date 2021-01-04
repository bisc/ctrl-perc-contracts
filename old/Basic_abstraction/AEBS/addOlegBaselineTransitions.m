function [lattice] = addOlegBaselineTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell,rounding,onePoint)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
format long
latticeSize = size(lattice);

for i=1:latticeSize(1)
    for j=1:latticeSize(2)
        tempCell = lattice(i,j);
        d = tempCell.d;
        v = tempCell.v;
        if(d==10 && v==0.8)
            aegre=3;
        end
        newMapKey = N;
        clear newMapValue
        for K=0:1:N
            if(onePoint==0)
                [nextds,nextvs] = computeOlegBaselineTransitionAEBS(d,v,N,K,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell);
            else
                [nextds,nextvs] = computeOlegBaselineTransitionOnePoint(d,v,N,K,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell);
            end
%             nextds
%             nextvs
            if(rounding==1)
                [nextds,nextvs] = scrubTransitionsWorstCase(nextds,nextvs,deltad,deltav);
            end
            latticeTransitions = [];
%             nextds
%             nextvs
            if(length(nextvs)>1)
                a = 1;
            end
            for iter = 1:length(nextds)
                nextd = max(nextds(iter),0);
                nextv = max(nextvs(iter),0);
                if(onePoint==0)
                    nextdid = floor(nextd/deltad)+1;
                    nextvid = floor(nextv/deltav)+1;
                else
                    nextdid = round(nextd/deltad)+1;
                    nextvid = round(nextv/deltav)+1;
                end
                
%                 crashdid = ceil(safetyThresh/deltad);
%                 if(nextd>safetyThresh && nextv<=0 && nextdid<=crashdid)
%                     nextvid=1;
%                     nextdid=crashdid+1;
%                 end
                if(length(latticeTransitions)==0)
                    latticeTransitions = [latticeTransitions; nextdid nextvid];
                else
                    I = sum(latticeTransitions(:, 1) == nextdid & latticeTransitions(:, 2) == nextvid);
                    if(I==0)
                        latticeTransitions = [latticeTransitions; nextdid nextvid];
                    end
                end
            end
            newMapValue{K+1}=latticeTransitions;
        end
        tempCell.nextPoints(newMapKey)=newMapValue;
        lattice(i,j)=tempCell;
    end
end
end

