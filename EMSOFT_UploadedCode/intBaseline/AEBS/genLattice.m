%% This script builds the lattice
% The lattice is a 2-d array of custom structs
% Each struct contains the location, distance (and unique ids corresponding
% to the location in the lattice), along with a map struct that maps 
% Ns to an array which corresonds to the lattice points that the K value
% associated with the array index maps to



clear; close all;


%% Define hyper parameters
deltad=2;
deltav=1;
B1=5;
B2=10;
fmu=1;
amax=B2;
Thd=0.5;
xThresh=1.75;
TTCThresh=6;
freq=10;

dMax=100;
vMax=25;


lattice = initLattice(dMax,vMax,deltad,deltav);



%% Add N transitions
nMax=0;
% N=3;
% lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);
% nMax = max(nMax,N);

N=5;
lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);
nMax = max(nMax,N);

% N=15;
% lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);
% nMax = max(nMax,N);


convertLatticeToPRISMModel(lattice,nMax,'PRISMModels/ForPaper/latticePRISMModel.prism');




%% Plot lattice and transitions
dPoints = 0:deltad:dMax;
vPoints = 0:deltav:vMax;
numdPoints = dMax/deltad+1;
numvPoints = vMax/deltav+1;

dPoints = zeros(numdPoints,numvPoints);
vPoints = zeros(numdPoints,numvPoints);

% figure(1); clf;
% hold on
% for i = 1:numvPoints
%     dPoints = 0:deltad:dMax;
%     vPoints = ones(numdPoints,1)*(i-1)*deltav;
%     scatter(-dPoints,vPoints, 'o', 'MarkerFaceColor', 'b')
% end
% xlabel('Distance (-m)')
% ylabel('Velocity (m/s)')
% hold off

% plotLattice(numdPoints,numvPoints,dMax,vMax,deltad,deltav);


% pause(5)
% for i =1:numdPoints
%     for j = 1:numvPoints
%         if(i==1 || j==1)
%             continue
%         end
%         figure(1); 
% %         clf;
%         plotLattice(numdPoints,numvPoints,dMax,vMax,deltad,deltav);
%         currcell = lattice(i,j);
%         cellPoint = [currcell.d currcell.v];
%         cellPointid = [currcell.did currcell.vid];
%         nextPoints = currcell.nextPoints;
%         currKeys{i,j} = keys(nextPoints);
%         currValues{i,j} = values(nextPoints);
%         
%         
%         tempkeys = keys(nextPoints);
%         for keyIter = 1:length(tempkeys)
%             key = tempkeys(keyIter);
%             key = key{1};
%             if key == 0
%                 continue
%             end
%             val = nextPoints(key);
%             for transIter = 1:length(val)
%                 nextPoints = val{transIter};
%                 for k = 1:size(nextPoints,1)
%                     nextPointdid = nextPoints(k,1);
%                     nextPointvid = nextPoints(k,2);
%                     nextPointd = (nextPointdid-1)*deltad;
%                     nextPointv = (nextPointvid-1)*deltav;
%                     arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
%                 end
%             end
%         end
%     end
% end



figure(1); clf;
i=6; j=11;
plotLattice(numdPoints,numvPoints,dMax,vMax,deltad,deltav);
currcell = lattice(i,j);
cellPoint = [currcell.d currcell.v];
% cellPointid = [currcell.did currcell.vid];
nextPoints = currcell.nextPoints;
% currValues = values(nextPoints);
tempkeys = keys(nextPoints);
for i = 1:length(tempkeys)
    key = tempkeys{i};
%     key = key{1};
    if key == 0
        continue
    end
    val = nextPoints(key);
    for j = 1:length(val)
        nextPointsTrans = val{j};
        if(j~=2)
            continue;
        end
        for k = 1:size(nextPointsTrans,1)
            nextPointdid = nextPointsTrans(k,1);
            nextPointvid = nextPointsTrans(k,2);
            nextPointd = (nextPointdid-1)*deltad;
            nextPointv = (nextPointvid-1)*deltav;
            arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
        end
    end
end



i=4; j=9;
currcell = lattice(i,j);
cellPoint = [currcell.d currcell.v];
% cellPointid = [currcell.did currcell.vid];
nextPoints = currcell.nextPoints;
% currValues = values(nextPoints);
tempkeys = keys(nextPoints);
for i = 1:length(tempkeys)
    key = tempkeys{i};
%     key = key{1};
    if key == 0
        continue
    end
    val = nextPoints(key);
    for j = 1:length(val)
        nextPointsTrans = val{j};
        if(j~=4)
            continue;
        end
        for k = 1:size(nextPointsTrans,1)
            nextPointdid = nextPointsTrans(k,1);
            nextPointvid = nextPointsTrans(k,2);
            nextPointd = (nextPointdid-1)*deltad;
            nextPointv = (nextPointvid-1)*deltav;
            arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
        end
    end
end


i=3; j=4;
currcell = lattice(i,j);
cellPoint = [currcell.d currcell.v];
% cellPointid = [currcell.did currcell.vid];
nextPoints = currcell.nextPoints;
% currValues = values(nextPoints);
tempkeys = keys(nextPoints);
for i = 1:length(tempkeys)
    key = tempkeys{i};
%     key = key{1};
    if key == 0
        continue
    end
    val = nextPoints(key);
    for j = 1:length(val)
        nextPointsTrans = val{j};
        if(j~=1)
            continue;
        end
        for k = 1:size(nextPointsTrans,1)
            nextPointdid = nextPointsTrans(k,1);
            nextPointvid = nextPointsTrans(k,2);
            nextPointd = (nextPointdid-1)*deltad;
            nextPointv = (nextPointvid-1)*deltav;
            arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
        end
    end
end


i=2; j=4;
currcell = lattice(i,j);
cellPoint = [currcell.d currcell.v];
% cellPointid = [currcell.did currcell.vid];
nextPoints = currcell.nextPoints;
% currValues = values(nextPoints);
tempkeys = keys(nextPoints);
for i = 1:length(tempkeys)
    key = tempkeys{i};
%     key = key{1};
    if key == 0
        continue
    end
    val = nextPoints(key);
    for j = 1:length(val)
        nextPointsTrans = val{j};
        if(j~=2)
            continue;
        end
        for k = 1:size(nextPointsTrans,1)
            nextPointdid = nextPointsTrans(k,1);
            nextPointvid = nextPointsTrans(k,2);
            nextPointd = (nextPointdid-1)*deltad;
            nextPointv = (nextPointvid-1)*deltav;
            arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
        end
    end
end

% i=15;j=20;
% currcell = lattice(i,j);
% cellPoint = [currcell.d currcell.v];
% % cellPointid = [currcell.did currcell.vid];
% nextPoints = currcell.nextPoints;
% % currValues = values(nextPoints);
% tempkeys = keys(nextPoints);
% for i = 1:length(tempkeys)
%     key = tempkeys(i);
%     key = key{1};
%     if key == 0
%         continue
%     end
%     val = nextPoints(key);
%     for j = 1:length(val)
%         nextPoints = val{j};
% %         if(size(nextPoints,1)==1)
% %             continue;
% %         end
%         for k = 1:size(nextPoints,1)
%             nextPointdid = nextPoints(k,1);
%             nextPointvid = nextPoints(k,2);
%             nextPointd = (nextPointdid-1)*deltad;
%             nextPointv = (nextPointvid-1)*deltav;
%             arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
%         end
%     end
% end
% 
% 
% 
% i=20;j=5;
% currcell = lattice(i,j);
% cellPoint = [currcell.d currcell.v];
% % cellPointid = [currcell.did currcell.vid];
% nextPoints = currcell.nextPoints;
% % currValues = values(nextPoints);
% tempkeys = keys(nextPoints);
% for i = 1:length(tempkeys)
%     key = tempkeys(i);
%     key = key{1};
%     if key == 0
%         continue
%     end
%     val = nextPoints(key);
%     for j = 1:length(val)
%         nextPoints = val{j};
%         if(size(nextPoints,1)==1)
%             continue;
%         end
%         for k = 1:size(nextPoints,1)
%             nextPointdid = nextPoints(k,1);
%             nextPointvid = nextPoints(k,2);
%             nextPointd = (nextPointdid-1)*deltad;
%             nextPointv = (nextPointvid-1)*deltav;
%             arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
%         end
%     end
% end
% 
% 
% i=15;j=15;
% currcell = lattice(i,j);
% cellPoint = [currcell.d currcell.v];
% % cellPointid = [currcell.did currcell.vid];
% nextPoints = currcell.nextPoints;
% % currValues = values(nextPoints);
% tempkeys = keys(nextPoints);
% for i = 1:length(tempkeys)
%     key = tempkeys(i);
%     key = key{1};
%     if key == 0
%         continue
%     end
%     val = nextPoints(key);
%     for j = 1:length(val)
%         nextPoints = val{j};
%         if(size(nextPoints,1)==1)
%             continue;
%         end
%         for k = 1:size(nextPoints,1)
%             nextPointdid = nextPoints(k,1);
%             nextPointvid = nextPoints(k,2);
%             nextPointd = (nextPointdid-1)*deltad;
%             nextPointv = (nextPointvid-1)*deltav;
%             arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
%         end
%     end
% end




% plotCell(lattice,3,4,deltad,deltav);
% plotCell(lattice,5,6,deltad,deltav);



function ret = plotCell(lattice,i,j,deltad,deltav)
currcell = lattice(i,j);
cellPoint = [currcell.d currcell.v];
cellPointid = [currcell.did currcell.vid];
nextPoints = currcell.nextPoints;
keys(nextPoints)
currValues = values(nextPoints);
keys = keys(nextPoints);
for i = 1:length(keys)
    key = keys(i);
    key = key{1};
    if key == 0
        continue
    end
    val = nextPoints(key);
    for j = 1:size(val,1)
        nextPointdid = val(j,1);
        nextPointvid = val(j,2);
        nextPointd = (nextPointdid-1)*deltad;
        nextPointv = (nextPointvid-1)*deltav;
        arrow([-cellPoint(1) cellPoint(2)], [-nextPointd nextPointv]);
    end
end

end


function plottedLattice = plotLattice(numdPoints,numvPoints,dMax,vMax,deltad,deltav)

hold on
for i = 1:numvPoints
    dPoints = 0:deltad:dMax;
    vPoints = ones(numdPoints,1)*(i-1)*deltav;
    scatter(-dPoints,vPoints, 'o', 'MarkerFaceColor', 'b', 'MarkerEdgeColor', 'b')
end
xlabel('Distance (-m)')
ylabel('Velocity (m/s)')
hold off

end