function [locs,vels,LECreadings,controllerRegions,controllerActions,times] = getTrajectory(LECprob,init_pos,init_vel,freq,B1,B2,xThresh,TTCthresh,Thd,fmu,amax)
%GETTRAJECTORY Summary of this function goes here
%   Detailed explanation goes here
locs=[];
vels=[];
LECreadings=[];
controllerRegions=[];
controllerActions=[];
times=[];

foundTraj=0;

position=init_pos;
velocity=init_vel;
t=0;
while true
    if(position <= 0)
        break
    end
    if(velocity <= 0)
        foundTraj=1;
        break
    end
    
    % Record car state
    locs=[locs; position];
    vels=[vels; velocity];
    times=[times;t];
    
    % Sample LEC reading
    LECreading = (rand<= LECprob);
    LECreadings=[LECreadings;LECreading];
    % Compute controller region
    x = (position - fmu*velocity.^2/(2*amax))./(position*Thd);
    y = (position./velocity);
    
    AEBSRegion = 1*(x<=xThresh) + 1*(y<=TTCthresh);
    controllerRegions=[controllerRegions; AEBSRegion];
    
    brakingPower = LECreading*(B1*(AEBSRegion==1) + B2*(AEBSRegion==2));
    controllerActions=[controllerActions; brakingPower];
    
    position=position-velocity*1/freq;
    velocity=velocity-brakingPower*1/freq;
    t=t+1/freq;
end


if(foundTraj==0)
    % If the trajectory is invalid, return null
    locs=[];
    vels=[];
    LECreadings=[];
    controllerRegions=[];
    controllerActions=[];
    times=[];
    
end

end
