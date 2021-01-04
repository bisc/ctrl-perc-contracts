%% This script builds the lattice
% The lattice is a 2-d array of custom structs
% Each struct contains the location, distance (and unique ids corresponding
% to the location in the lattice), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to



clear; close all;
format long

%% Define hyper parameters

rounding=0;
windowLen=3;
initCond=2;
onePoint=0;

initDists = 120:5:140;
initSpeeds = 10:4:26;

for dist=100:5:115
    for speed=10:4:26

        dist
        speed
        
        deltad=0.25;
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
        lattice = addOlegBaselineTransitions(baseline,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh,numDPerCell,numVPerCell,rounding,onePoint);
        nMax = max(nMax,N);

        if(rounding==0)
            fileName = sprintf('PRISMModels/roundingConservatismTest/distDisc025/noRounding/olegBaselineAEBS_initd%f_initv%f.prism', dist,speed);
        else
            fileName = sprintf('PRISMModels/roundingConservatismTest/distDisc025/withRounding/olegBaselineAEBS_initd%f_initv%f.prism', dist,speed);
        end
        % convertOlegBaselineToPRISMModel(lattice,nMax,'PRISMModels/ForPaper/latticePRISMModelTrimmedCondLEC.prism',deltad,deltav,amax,0);
        convertOlegBaselineToPRISMModelCondLECForDiffInitPoints(lattice,nMax,fileName,deltad,deltav,amax,1,safetyThresh,windowLen);
    end
end