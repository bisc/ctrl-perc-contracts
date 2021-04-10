%% This script builds the lattice
% The lattice is a 1-d array of custom structs
% Each struct contains the water level (and unique id), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to

clear; close all;
format long

%% Define hyper parameters
inflow = 13;
outflow = 2;
deltawl=1;
wlMax=100;
baseline = initOlegBaseline(wlMax,deltawl);
trimmed = 0;

%% Add N transitions
N=1;
lattice = addOlegBaselineTransitions(baseline,N,deltawl,inflow,outflow,trimmed);
% lattice = addOlegBaselineTransitionsBaseline(baseline,N,deltawl,inflow,outflow,trimmed);

% convertOlegBaselineToPRISMModel(lattice,nMax,'PRISMModels/ForPaper/latticePRISMModelTrimmedCondLEC.prism',deltad,deltav,amax,0);
% convertOlegBaselineToPRISMModelMultiTank(lattice,N,'PRISMModels/testModel2Tank_2.prism',deltawl,trimmed,2);
% convertOlegBaselineToPRISMModelMultiTank(lattice,N,'PRISMModels/testModel2TankTrimmed_2.prism',deltawl,trimmed,2);
% convertOlegBaselineToPRISMModelMultiTank(lattice,N,'PRISMModels/testModel2TankBasline.prism',deltawl,trimmed,2);

convertOlegBaselineToPRISMModelMultiTank(lattice,N,'PRISMModels/testModel2TankBasline_2.prism',deltawl,trimmed,2);
