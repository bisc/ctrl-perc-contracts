%% This script builds the lattice
% The lattice is a 2-d array of custom structs
% Each struct contains the location, distance (and unique ids corresponding
% to the location in the lattice), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to



clear; close all;
format long

%% Define hyper parameters





deltad=1;
deltav=0.4;

B=8;
freq=10;


dMax=160;
vMax=20;


baseline = initOlegBaseline(dMax,vMax,deltad,deltav);

safetyThresh=0;

%% Add N transitions
nMax=0;
N=3;
lattice = addOlegBaselineTransitions(baseline,N,deltad,deltav,B,freq,safetyThresh);
nMax = max(nMax,N);

% convertOlegBaselineToPRISMModel(lattice,nMax,'PRISMModels/ForPaper/latticePRISMModelTrimmedCondLEC.prism',deltad,deltav,amax,0);
convertOlegBaselineToPRISMModelCondLEC(lattice,nMax,'PRISMModels/testing/olegBaselineConstLECWithLECBundling.prism',deltad,deltav,B,1,safetyThresh);
