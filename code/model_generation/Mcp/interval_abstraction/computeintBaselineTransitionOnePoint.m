function [dfs,vfs] = computeOlegBaselineTransitionOnePoint(d,v,N,K,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here


dfs = [];
vfs = [];

d0=d;
v0=v;
d0Next=d0-v0/freq;
v0Next=v0-(K==1)*computeAEBSPower(d,v,fmu,amax,Thd,xThresh,TTCThresh,B1,B2,safetyThresh)/freq;

dfs = [d0Next];
vfs = [v0Next];
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