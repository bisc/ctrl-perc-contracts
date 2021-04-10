function [] = convertOlegBaselineToPRISMModel(lattice, maxN, fileName,deltawl,trimmed)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

format long

fid = fopen(fileName, 'wt');

latticeSize = size(lattice);

wlidMax = latticeSize(2);

fprintf(fid, 'mdp\n');
fprintf(fid, '\n \n');
fprintf(fid, 'const int wlidInit;\n');
fprintf(fid, 'const int wlidMax = %i;\n', wlidMax);
fprintf(fid, 'const int Nmax = %i;\n', maxN);
% fprintf(fid, 'const int wlContLowThresh = 15;\n');
% fprintf(fid, 'const int wlContUpThresh = 45;\n');
fprintf(fid, 'const int maxTime = 100;\n');

fprintf(fid, '\n \n');
fprintf(fid, 'module PRISMLattice\n\n');
fprintf(fid, '    wlid : [1..wlidMax] init wlidMax;\n');
fprintf(fid, '    wlidPer : [1..wlidMax] init wlidMax;\n');
fprintf(fid, '    currN : [0..2] init 0;\n');
fprintf(fid, '    contAction : [0..1] init 0;\n');
fprintf(fid, '    sink: [0..1] init 0;\n');
fprintf(fid, '    timesteps: [0..maxTime] init 0;\n');

printLECModelWaterTank(lattice, maxN, fid,deltawl)

printControllerWaterTank(lattice, maxN, fid,deltawl)

%% Filter by reachability
% reachabilityMatrix = zeros(wlidMax,vidMax);
% reachabilityMatrix(wlidMax,vidMax)=1;
% for i=wlidMax:-1:2
%     for j = vidMax:-1:2
%         currcell = lattice(i,j);
%         currdid = currcell.did;
%         currvid = currcell.vid;
%         
%         if(reachabilityMatrix(currdid,currvid)==0)
%             continue
%         end
%      
%         currv = (currvid-1)*deltav;
%         currd = (currdid)*deltad;
%         stoppingDist = (currv^2)/(2*amax);
%         if(stoppingDist+safetyThresh>= currd)
%             continue
%         end
% %         TTC = (currd-safetyThresh)/(currv);
% %         if(TTC<3 && currv>=5)
% %             continue
% %         end
%         
%         currTransMap = currcell.nextPoints;
%         currMapKeys = keys(currTransMap);
%         for k = 1:length(currMapKeys)
%             key = currMapKeys{k};
%             if key == 0
%                 continue
%             end
%    
%             val = currTransMap(key);
%             
%             for l = 1:length(val)
%                     nextPointsTrans = val{l};
%                     for m = 1:size(nextPointsTrans,1)
%                         nextPointdid = nextPointsTrans(m,1);
%                         nextPointvid = nextPointsTrans(m,2);                     
%                         reachabilityMatrix(nextPointdid,nextPointvid)=1;
%                     end
%             end
%         end
%     end
% end

% xs = [];
% ys = [];
% for i=2:wlidMax
%     for j = 2:vidMax
%         if(reachabilityMatrix(i,j)==1)
%             xs = [xs i*deltad];
%             ys = [ys j*deltav];
%         end
%     end
% end


% figure(1); clf;
% plot(xs,ys,'b*');
% xlabel('Distance')
% ylabel('Velocity')

for i=1:wlidMax
    currcell = lattice(i);
    currwlid = currcell.wlid;

%     if(reachabilityMatrix(currdid,currvid)==0 && trimmed)
%         continue
%     end
    currwl = (currwlid+1)*deltawl;
    currTransMap = currcell.nextPoints;
    currMapKeys = keys(currTransMap);
    for k = 1:length(currMapKeys)
        key = currMapKeys{k};
        if key == 0
            continue
        end
        currN = key;
        fprintf(fid, '\n');
        val = currTransMap(key);

        allDidNextAre1=0;

        for l = 1:length(val)
            currK=l-1;
            nextPointsTrans = val{l};

%             allPointsSame=1;
%             for m = 1:size(nextPointsTrans,1)-1
%                 nextPointwlid1 = nextPointsTrans(m,1);
% 
%                 nextPointwlid2 = nextPointsTrans(m+1,1);
% 
%                 if(nextPointwlid1==nextPointwlid2 && nextPointvid1 && nextPointvid2)
%                     continue
%                 end
%                 allPointsSame=0;
%                 break;
%             end
            for m = 1:size(nextPointsTrans,1)
                nextPointwlid = nextPointsTrans(m,1);
                if(nextPointwlid<=1)
                    fprintf(fid, '    [] wlid=%i&currN=%i&contAction=%i&sink=0&timesteps<maxTime -> (sink''=1);\n', currwlid, 2, currK);
                elseif(nextPointwlid>=wlidMax)
                    fprintf(fid, '    [] wlid=%i&currN=%i&contAction=%i&sink=0&timesteps<maxTime -> (sink''=1);\n', currwlid, 2, currK);
                else
                    fprintf(fid, '    [] wlid=%i&currN=%i&contAction=%i&sink=0&timesteps<maxTime -> (wlid''=%i)&(currN''=0)&(timesteps''=timesteps+1);\n', currwlid, 2, currK, round(nextPointwlid));
                end
%                 if(nextPointwlid==(safetyThreshInd+1) && nextPointvid>=2)
%                     fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (did''=1);\n', currvid, currdid, 2, currK);
%                 elseif(nextPointwlid<=(safetyThreshInd))
%                     fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (did''=1);\n', currvid, currdid, 2, currK);
%                 else
                    %% Stateful LEC
%                          fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, currN, currK, nextPointvid, round(nextPointdid));
                   %% Stateless LEC
%                          fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, currN, currK, nextPointvid, round(nextPointdid));
                   %% Stateless LEC precomputed K and N transitions
%                     fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, 2, currK, nextPointvid, round(nextPointwlid));
%                 end
            end
        end
    end
end

fprintf(fid, '\n \n');
fprintf(fid, 'endmodule\n');
fclose(fid);
end

