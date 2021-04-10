function [dfs] = computeOlegBaselineTransitionWaterTank(wl,K,deltawl,inflow,outflow,numWLPerCell)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here


dfs = [];

N=1;
Nvec = 1:N;
Kperms = combnk(Nvec,K);

if(K==0)
    Kperms = [-1 -1];
end

for ordering = 1:size(Kperms,1)
    
    detections = Kperms(ordering,:);
    
    tempWL=wl;
    for i=1:N
        if(~ismember(i,detections))
            tempWL=max(0,tempWL-outflow);
        else
            tempWL=max(0,tempWL-outflow+inflow);
        end
    end
    dfs = [dfs; tempWL];
end
end