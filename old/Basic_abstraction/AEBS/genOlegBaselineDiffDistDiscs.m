%% This script builds the lattice
% The lattice is a 2-d array of custom structs
% Each struct contains the location, distance (and unique ids corresponding
% to the location in the lattice), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to



clear; close all;
format long

%% Define hyper parameters


distDiscs = [0.1 0.2 0.25 0.4 0.5 1 2];
% distDiscs = [0.2 0.25 0.4];
% distDiscs = [0.1];

onePoint=0;
% distDiscs = [0.25];
rounding=1;
windowLen=3;
initCond=1;
for i=1:length(distDiscs)

    deltad=distDiscs(i);
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
    
    trimmed=1;
    
    if(initCond==1)
        dMax=160;
        vMax=20;
    elseif(initCond==2)
        dMax=90;
        vMax=10;
    end


    baseline = initOlegBaseline(dMax,vMax,deltad,deltav);

    safetyThresh=5;

    %% Add N transitions
    nMax=0;
    N=1;
    lattice = addOlegBaselineTransitions(baseline,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell,rounding,onePoint);
    nMax = max(nMax,N);
    
    if(rounding==1 && initCond==2)
        fileName = sprintf('PRISMModels/testingFixedRounding/olegBaselineAEBSConstLECInitCond2WithRounding%f.prism', deltad);
    elseif(rounding==0 && initCond==2)
        fileName = sprintf('PRISMModels/testingFixedRounding/olegBaselineAEBSConstLECInitCond2NoRounding%f.prism', deltad);
    elseif(rounding==1 && initCond==1)
        fileName = sprintf('PRISMModels/testingFixedRounding/olegBaselineAEBSConstLECInitCond1WithRounding%f.prism', deltad);
    else
        fileName = sprintf('PRISMModels/testingFixedRounding/olegBaselineAEBSConstLECInitCond1NoRounding%f.prism', deltad);
    end
    % convertOlegBaselineToPRISMModel(lattice,nMax,'PRISMModels/ForPaper/latticePRISMModelTrimmedCondLEC.prism',deltad,deltav,amax,0);
%     convertOlegBaselineToPRISMModelCondLEC(lattice,nMax,fileName,deltad,deltav,amax,1,safetyThresh,windowLen);
    convertOlegBaselineToPRISMModelCondLECForDiffInitPoints(lattice,nMax,fileName,deltad,deltav,amax,trimmed,safetyThresh,windowLen);
end