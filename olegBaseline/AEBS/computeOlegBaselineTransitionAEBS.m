function [dfs,vfs] = computeOlegBaselineTransitionAEBS(d,v,N,K,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here


dfs = [];
vfs = [];

% Construct points to get transitions for
dsVals = d:deltad/numDPerCell:d+deltad;
vsVals = v:deltav/numVPerCell:v+deltav;


Nvec = 1:N;
Kperms = combnk(Nvec,K);

if(K==0)
    Kperms = [-1 -1];
end
K;
N;
Kperms;
for ordering = 1:size(Kperms,1)
    
    detections = Kperms(ordering,:);
    
    for startDist=d:deltad/numDPerCell:d+deltad-deltad/numDPerCell
        for startVel=v:deltav/numVPerCell:v+deltav-deltav/numVPerCell
            dist=startDist;
            vel=startVel;
            for i=1:N
                if(~ismember(i,detections))
                    dist=max(0,dist-vel/freq);
                else
                    dist=max(0,dist-vel/freq);
                    brakingPower = computeAEBSPower(dist,vel,fmu,amax,Thd,xThresh,TTCThresh,B1,B2,safetyThresh);
                    vel=max(0,vel-brakingPower/freq);
                end
            end
            dfs = [dfs; dist];
            vfs = [vfs; vel];
        end
    end
end
end

function braking = computeAEBSPower(d,v,fmu,amax,Thd,xThresh,TTCThresh,B1,B2,safetyThresh)
    AEBSRegion = computeAEBSRegion(d,v,fmu,amax,Thd,xThresh,TTCThresh,safetyThresh);
    braking = (AEBSRegion==0)*0+(AEBSRegion==1)*B1 + (AEBSRegion==2)*B2;
end

function contRegion = computeAEBSRegion(d,v,fmu,amax,Thd,xThresh,TTCThresh,safetyThresh)

    d = d-safetyThresh;
    x = (d - fmu*v.^2/(2*amax))./(v*Thd);
    y = (d./v);

    contRegion = 1*(x<=xThresh) + 1*(y<=TTCThresh);


end