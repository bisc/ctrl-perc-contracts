%% This script builds the lattice
% The lattice is a 2-d array of custom structs
% Each struct contains the location, distance (and unique ids corresponding
% to the location in the lattice), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to



clear; close all;
format long

%% Define hyper parameters

rounding=1;
windowLen=3;
initCond=2;

dist=10;
speed=0.8;

deltad=1;
deltav=0.4;

B1=4;
B2=8;
fmu=1;
amax=B2;
Thd=2;
xThresh=1;
TTCThresh=6;
freq=10;

numDPerCell=10;
numVPerCell=10;

dMax = dist;
vMax = speed;

baseline = initOlegBaseline(dMax,vMax,deltad,deltav);

safetyThresh=5;

%% Add N transitions
nMax=0;
N=1;
lattice = addOlegBaselineTransitions(baseline,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell,rounding);
nMax = max(nMax,N);

if(rounding==0)
    fileName = sprintf('PRISMModels/roundingTesting/noRounding.prism');
else
    fileName = sprintf('PRISMModels/roundingTesting/withRounding.prism');
end
% convertOlegBaselineToPRISMModel(lattice,nMax,'PRISMModels/ForPaper/latticePRISMModelTrimmedCondLEC.prism',deltad,deltav,amax,0);
convertOlegBaselineToPRISMModelCondLEC(lattice,nMax,fileName,deltad,deltav,amax,1,safetyThresh,windowLen);
