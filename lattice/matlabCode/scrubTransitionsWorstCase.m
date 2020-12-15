function [scrubbedNextds,scrubbedNextvs] = scrubTransitionsWorstCase(nextds,nextvs)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

scrubbedNextds = [];
scrubbedNextvs = [];

for i = 1:size(nextds,1)
    nextd = nextds(i);
    nextv = nextvs(i);
    if(isWorse(nextd,nextv,nextds,nextvs))
        scrubbedNextds = [scrubbedNextds; nextd];
        scrubbedNextvs = [scrubbedNextvs; nextv];
    end
end
end


function worse = isWorse(nextd,nextv,nextds,nextvs)
    for j = 1:size(nextds,1)
        if(isBetter(nextd,nextv,nextds(j),nextvs(j)))
            worse = 0;
            return
        end
    end
    worse = 1;
end

function better = isBetter(d1,v1,d2,v2)
    if (d1>d2 && v1 < v2)
        better = 1;
    else
        better = 0;
    end
end