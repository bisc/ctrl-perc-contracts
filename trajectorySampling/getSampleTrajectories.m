%% This script runs trials of the AEBS car with the LEC

%% Define Car Hyperparamters
fmu = 1; amax=10; Thd=0.5;

xThresh=1.75;
TTCThresh=6;

LECprob = 0.2;

init_pos=100;
init_vel=26.8;
B1=5; B2=10;
freq=10;

numTraj=20;
traj=0;

LECTrajectories=cell(numTraj,1);
KsandNs=cell(numTraj,1);
while traj<numTraj
    [locs,vels,LECreadings,controllerRegions,controllerActions,times] = getTrajectory(LECprob,init_pos,init_vel,freq,B1,B2,xThresh,TTCThresh,Thd,fmu,amax);
    if isempty(locs)
        continue;
    end
    traj=traj+1
    LECTrajectories{traj,1}=locs;
    LECTrajectories{traj,2}=vels;
    LECTrajectories{traj,3}=LECreadings;
    LECTrajectories{traj,4}=controllerRegions;
    LECTrajectories{traj,5}=controllerActions;
    LECTrajectories{traj,6}=times;
    
    [safeKs, safeNs] = getKandNsFromSafeTrace(LECreadings, controllerRegions);
    KsandNs{traj}=[safeKs safeNs];
end


%% For each trajectory, compute the K and N values for the contract