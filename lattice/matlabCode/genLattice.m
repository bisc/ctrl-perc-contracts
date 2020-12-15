%% This script builds the lattice
% The lattice is a 2-d array of custom structs
% Each struct contains the location, distance (and unique ids corresponding
% to the location in the lattice), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to



clear;
%% Define hyper parameters
deltad=1;
deltav=0.5; 
B1=5;
B2=10;
fmu=1;
amax=B2;
Thd=0.5;
xThresh=1.75;
TTCThresh=6;
freq=10;

dMax = 80;
vMax=10;


lattice = initLattice(dMax,vMax,deltad,deltav);



%% Add N transitions
N=5;
lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);

N=1;
lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);

N=10;
lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);


%% Compute the next lattice point for a sequence of Ks and Ns
Ns = [10, 10, 5, 5, 5, 1];
Ks = [4,7,2,4,5,0];

% From the top right point on the lattice
did = 81;
vid = 21;

[did,vid,lattice] = computeLatticeTransitionMultiKAndN(did,vid,lattice,Ns,Ks,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);

nextLatticeCell = lattice(did,vid);


