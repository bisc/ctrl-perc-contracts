function [scrubbedNextds,scrubbedNextvs] = scrubTransitionsWorstCase(nextds,nextvs)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

scrubbedNextds = [];
scrubbedNextvs = [];

for i = 1:length(nextds)
    nextd = nextds(i);
    nextv = nextvs(i);
    if(isWorse(nextd,nextv,nextds,nextvs))
        alreadyHasPoint = 0;
        for j = 1:length(scrubbedNextds)
            if(abs(nextd - scrubbedNextds(j))<0.0001 && abs(nextv - scrubbedNextvs(j)) < 0.0001)
                alreadyHasPoint = 1;
                break
            end
        end
        if(~alreadyHasPoint)
            scrubbedNextds = [scrubbedNextds; nextd];
            scrubbedNextvs = [scrubbedNextvs; nextv];
        end
    end
end
end


function worse = isWorse(nextd,nextv,nextds,nextvs)
    for j = 1:length(nextds)
        if(isBetter(nextd,nextv,nextds(j),nextvs(j)))
            worse = 0;
            return
        end
    end
    worse = 1;
end

function better = isBetter(d1,v1,d2,v2)
    if(abs(d1-d2)<0.0001)
        d2=d1;
    end
    if(abs(v1-v2)<0.00001)
        v1=v2;
    end
    if (d1>d2 && v1 < v2)
        better = 1;
    elseif (d1>d2 && v1 <= v2)
        better = 1;
    elseif (d1>=d2 && v1 < v2)
        better = 1;
    else
        better = 0;
    end
end