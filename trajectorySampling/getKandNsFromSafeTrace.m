function [Ks,Ns] = getKandNsFromSafeTrace(LECReadings,ControllerRegions)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here



% Compute the difrerent intervals from the safe  trace
% An interval is defined as a sequence of LEC misdetections, followed by a
% sequence of LEC detections, ALL with the same controller region

Ks=[];
Ns=[];

currRegion=0;
lecFlag=0;

tempK=0;
tempN=0;
for i=1:length(LECReadings)
    LECreading = LECReadings(i);
    contRegion = ControllerRegions(i);
    
    if(i==1)
        tempK=LECreading;
        tempN=1;
        lecFlag=LECreading;
        currRegion=contRegion;
        continue
    end
    
    if(currRegion==contRegion)
        if(lecFlag==0 && LECreading==0)
            tempK=tempK;
            tempN=tempN+1;
        elseif (lecFlag==0 && LECreading==1)
            tempK=tempK+1;
            tempN=tempN+1;
            %lecFlag=1;
        elseif(lecFlag==1 && LECreading==0)
            if(currRegion ~= 0)
                Ks=[Ks; tempK];
                Ns=[Ns; tempN];
            end
            tempK=0;
            tempN=1;
            %lecFlag=0;
        else % lecFlag==1 && LECreading==1
            tempK=tempK+1;
            tempN=tempN+1;
        end
    else % New controller region
        if(LECreading==0)
            if(currRegion ~= 0)
                Ks=[Ks; tempK];
                Ns=[Ns; tempN];
            end
            tempK=0;
            tempN=1;
            %lecFlag=0;
        else % LECreading==1
            if(currRegion ~= 0)
                Ks=[Ks; tempK];
                Ns=[Ns; tempN];
            end
            tempK=1;
            tempN=1;
            %lecFlag=1;            
        end
    end
    lecFlag=LECreading;
    currRegion=contRegion;
end

Ks=[Ks; tempK];
Ns=[Ns; tempN];
end


