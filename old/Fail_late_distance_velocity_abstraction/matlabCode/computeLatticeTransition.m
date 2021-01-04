function [dfs,vfs] = computeLatticeTransition(d,v,N,K,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

dinit = d;
vinit = v;

dfs = [];
vfs = [];
% Loop through all possible orderings of K out of N detections
% how to enumerate this?
Nvec = 1:N;
Kperms = combnk(Nvec,K);

if(K==0)
    Kperms = [-1 -1];
end
% K
% N
% Kperms
for ordering = 1:size(Kperms,1)
    
    detections = Kperms(ordering,:);
    
    d=dinit;
    v=vinit;
    
    db=d+deltad;
    vb=v-deltav;
    
    for i=1:N
        v = max(0,v);
        vb = max(0,vb);
        if(~ismember(i,detections))
            d=d-v/freq;
            db=db-vb/freq;
        else
            d=d-v/freq;
            db=db-vb/freq;
            brakingPower = computeAEBSPower(d,v,fmu,amax,Thd,xThresh,TTCThresh,B1,B2,safetyThresh);
            v=v-brakingPower/freq;
            vb=vb-brakingPower/freq;
        end
    end
    d;
    v;
    
    df = d-mod(d,deltad);
    if mod(v,deltav)==0
        vf = v;
    else
        vf = v+deltav-mod(v,deltav);
    end
    
    dfs = [dfs; df];
    vfs = [vfs; vf];
end
dfs;
vfs;
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