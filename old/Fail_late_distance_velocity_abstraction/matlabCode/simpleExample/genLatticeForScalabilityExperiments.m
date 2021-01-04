%% This script builds the lattice
% The lattice is a 2-d array of custom structs
% Each struct contains the location, distance (and unique ids corresponding
% to the location in the lattice), along with a map struct that maps
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to

clear; close all;
format long

BoB = 1;

deltad=1.5;
N=3;
H=3;
L=3;

initDists = 120:5:180;
initSpeeds = 10:2:30;

for dist=100:5:200
    for speed=10:4:30
        %% Define hyper parameters
        deltav=0.4;
        B1=4;
        B2=8;
        fmu=1;
        amax=B2;
        Thd=2;
        xThresh=1;
        TTCThresh=6;
        freq=10;
        
        
        dMax=dist;
        vMax=speed;
        
        
        lattice = initLattice(dMax,vMax,deltad,deltav);
        
        safetyThresh=5;
        
        %% Add N transitions
        nMax=0;
        
        %     N=6;
        if BoB==0
            lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh);
        else
        lattice = addLatticeTransitionsBundledK(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq,safetyThresh);
        end       
        nMax = max(nMax,N);
                %     end
        if BoB==0
            fileName = sprintf('PRISMModels/ForPaper/scalability/lattice/LatticeScalabilityN3H3L3d15_initd%f_initv%f.prism', dist,speed);
        else
            fileName = sprintf('PRISMModels/ForPaper/scalability/bobLattice/BoBLatticeScalabilityN3H3L3d15_initd%f_initv%f.prism', dist,speed);
        end
        fileName
        convertLatticeToPRISMModelScalability(lattice,nMax,fileName,deltad,deltav,amax,1,safetyThresh);
    end
end