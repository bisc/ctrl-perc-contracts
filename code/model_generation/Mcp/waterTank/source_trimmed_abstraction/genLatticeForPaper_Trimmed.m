%% This script builds the lattice
% The lattice is a 1-d array of custom structs
% Each struct contains the water level (and unique id), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to

clear; close all;
format long

%% Define hyper parameters
inflow = 7;
outflow = 3;
deltawl=2;
wlMax=50;
baseline = initOlegBaseline(wlMax,deltawl);

%% Add N transitions
N=1;
lattice = addOlegBaselineTransitions(baseline,N,deltawl,inflow,outflow,1);

% convertOlegBaselineToPRISMModel(lattice,nMax,'PRISMModels/ForPaper/latticePRISMModelTrimmedCondLEC.prism',deltad,deltav,amax,0);
convertOlegBaselineToPRISMModelCondLEC(lattice,N,'PRISMModels/testModel_trimmed.prism',deltawl,1);
