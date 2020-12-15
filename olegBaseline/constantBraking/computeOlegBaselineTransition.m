function [dfs,vfs] = computeOlegBaselineTransition(d,v,N,K,deltad,deltav,B,freq,safetyThresh)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

dfs = [];
vfs = [];

d0=d;
v0=v;
d0Next=d0-v0/freq;
v0Next=v0-(K==1)*B/freq;
nextdid0 = max(0,floor(d0Next/deltad)+1);
nextvid0 = max(0,floor(v0Next/deltav)+1);

d1=d;
v1=v+deltav;
d1Next=d1-v1/freq;
v1Next=v1-(K==1)*B/freq;
nextdid1 = max(0,floor(d1Next/deltad)+1);
nextvid1 = max(0,floor(v1Next/deltav)+1);

d2=d+deltad;
v2=v;
d2Next=d2-v2/freq;
v2Next=v2-(K==1)*B/freq;
nextdid2 = max(0,floor(d2Next/deltad)+1);
nextvid2 = max(0,floor(v2Next/deltav)+1);

d3=d+deltad;
v3=v+deltav;
d3Next=d3-v3/freq;
v3Next=v3-(K==1)*B/freq;
nextdid3 = max(0,floor(d3Next/deltad)+1);
nextvid3 = max(0,floor(v3Next/deltav)+1);

dfs = [dfs; d0Next];
vfs = [vfs; v0Next];

if(~(nextdid1==nextdid0 && nextvid1==nextvid0))
    dfs = [dfs; d1Next];
    vfs = [vfs; v1Next];
end

if(~((nextdid2==nextdid0 && nextvid2==nextvid0) || (nextdid2==nextdid1 && nextvid2==nextvid1)))
    dfs = [dfs; d2Next];
    vfs = [vfs; v2Next];
end

if(~((nextdid3==nextdid0 && nextvid3==nextvid0) || (nextdid3==nextdid1 && nextvid3==nextvid1) || (nextdid3==nextdid2 && nextvid3==nextvid2)))
    dfs = [dfs; d3Next];
    vfs = [vfs; v3Next];
end
end
% Nvec = 1:N;
% Kperms = combnk(Nvec,K);
% 
% if(K==0)
%     Kperms = [-1 -1];
% end
% 
% 
% for ordering = 1:size(Kperms,1)
%     
%     detections = Kperms(ordering,:);
%     
%     d0=d;
%     v0=v;
%     
%     d1=d;
%     v1=v+deltav;
%     
%     d2=d+deltad;
%     v2=v;
%     
%     d3=d+deltad;
%     v3=v+deltav;
%     
% %     db=d+deltad;
% %     vb=v-deltav;
%     
%     for i=1:N
% %         v = max(0,v);
% %         vb = max(0,vb);
%         if(~ismember(i,detections))
%             d0=d0-v0/freq;
%             d1=d1-v1/freq;
%             d2=d2-v2/freq;
%             d3=d3-v3/freq;
% %             db=db-vb/freq;
%         else
%             d0=d0-v0/freq;
%             d1=d1-v1/freq;
%             d2=d2-v2/freq;
%             d3=d3-v3/freq;
%             
%             v0=v0-B/freq;
%             v1=v1-B/freq;
%             v2=v2-B/freq;
%             v3=v3-B/freq;
%         end
%     end
%     nextdid0 = floor(d0/deltad)+1;
%     nextvid0 = floor(v0/deltav)+1;
%     nextdid1 = floor(d1/deltad)+1;
%     nextvid1 = floor(v1/deltav)+1;
%     nextdid2 = floor(d2/deltad)+1;
%     nextvid2 = floor(v2/deltav)+1;
%     nextdid3 = floor(d3/deltad)+1;
%     nextvid3 = floor(v3/deltav)+1;
%     
%     dfs = [dfs; d0];
%     vfs = [vfs; v0];
% 
%     if(~(nextdid1==nextdid0 && nextvid1==nextvid0))
%         dfs = [dfs; d1];
%         vfs = [vfs; v1];
%     end
% 
%     if(~((nextdid2==nextdid0 && nextvid2==nextvid0) || (nextdid2==nextdid1 && nextvid2==nextvid1)))
%         dfs = [dfs; d2];
%         vfs = [vfs; v2];
%     end
% 
%     if(~((nextdid3==nextdid0 && nextvid3==nextvid0) || (nextdid3==nextdid1 && nextvid3==nextvid1) || (nextdid3==nextdid2 && nextvid3==nextvid2)))
%         dfs = [dfs; d3];
%         vfs = [vfs; v3];
%     end
% %     dfs = [dfs; d0; d1; d2; d3];
% %     vfs = [vfs; v0; v1; v2; v3];
% end
% dfs;
% vfs;
% end

function braking = computeAEBSPower(d,v,fmu,amax,Thd,xThresh,TTCThresh,B1,B2,safetyThresh)
    AEBSRegion = computeAEBSRegion(d,v,fmu,amax,Thd,xThresh,TTCThresh,safetyThresh);
    braking = (AEBSRegion==0)*0+(AEBSRegion==1)*B1 + (AEBSRegion==2)*B2;
end

function contRegion = computeAEBSRegion(d,v,fmu,amax,Thd,xThresh,TTCThresh,safetyThresh)

    d = d-safetyThresh;
    x = (d - fmu*v.^2/(2*amax))./(v*Thd);
    y = (d./v);

    contRegion = 1*(x<=xThresh) + 1*(y<=TTCThresh);


end