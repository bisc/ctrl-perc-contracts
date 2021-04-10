%% This script builds the lattice
% The lattice is a 2-d array of custom structs
% Each struct contains the location, distance (and unique ids corresponding
% to the location in the lattice), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to



clear; close all;
format long

BoB = 1;

deltaDs = [0.5 1 1.1 1.2 1.3 1.4 1.5 1.6 1.65 1.7 1.75 1.8 1.9 2];
% deltaDs = [0.25 0.5];
% deltaDs = [1.8,1.9];
% deltaDs = [1.45 1.55 1.6 1.65];

for i=1:size(deltaDs,2)
    %% Define hyper parameters
    deltad=deltaDs(i);
    deltav=0.4;
    % B1=10;
    % B2=20;
    % fmu=1;
    % amax=B2;
    % Thd=1;
    % xThresh=20;
    % TTCThresh=10;
    % freq=10;

    B1=4;
    B2=8;
    fmu=1;
    amax=B2;
    Thd=2;
    xThresh=1;
    TTCThresh=6;
    freq=10;


    dMax=160;
    vMax=20;


    lattice = initLattice(dMax,vMax,deltad,deltav);

    safetyThresh=5;

    %% Add N transitions
    nMax=0;

    N=3;
    if BoB == 1
        lattice = addLatticeTransitionsBundledK(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh);
    else
        lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh);
    end
    nMax = max(nMax,N);

%     % convertLatticeToPRISMModel(lattice,nMax,'PRISMModels/ForPaper/latticePRISMModelTrimmedCondLEC.prism',deltad,deltav,amax,0);\
%     if deltad==0.75
%        fileName = sprintf('PRISMModels/ForPaper/windows/N5/diffDeltaDs/TTCThresh/latticePRISMModelTrimmedCondLECN5d075.prism');
%     elseif deltad==1
%         fileName = sprintf('PRISMModels/ForPaper/windows/N5/diffDeltaDs/TTCThresh/latticePRISMModelTrimmedCondLECN5d075.prism');
%     elseif deltad==1.25
%         fileName = sprintf('PRISMModels/ForPaper/windows/N5/diffDeltaDs/TTCThresh/latticePRISMModelTrimmedCondLECN5d075.prism');
%     elseif deltad==1.5
%         fileName = sprintf('PRISMModels/ForPaper/windows/N5/diffDeltaDs/TTCThresh/latticePRISMModelTrimmedCondLECN5d075.prism');
%     end
    if BoB==1
        fileName = sprintf('PRISMModels/ForPaper/windows/N3H3L3/diffDeltaDsBoBLattice/latticePRISMModelTrimmedCondLECN3H3L3d%f.prism', deltad);
    else
        fileName = sprintf('PRISMModels/ForPaper/windows/N3H3L3/diffDeltaDs/latticePRISMModelTrimmedCondLECN3H3L3d%f.prism', deltad);
    end
%     fileName = sprintf('latticePRISMModelTrimmedCondLECN3H3L3d%f.prism', deltad);
    fileName
    convertLatticeToPRISMModelCondLEC(lattice,nMax,fileName,deltad,deltav,amax,1,safetyThresh);

end