function [] = convertLatticeToPRISMModel(lattice, maxN, fileName,deltad,deltav,amax,trimmed,safetyThresh)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

format long

fid = fopen(fileName, 'wt');

latticeSize = size(lattice);

didMax = latticeSize(1);
vidMax = latticeSize(2);

fprintf(fid, 'mdp\n');
fprintf(fid, '\n \n');
fprintf(fid, 'const int didMax = %i;\n', didMax);
fprintf(fid, 'const int vidMax = %i;\n', vidMax);
fprintf(fid, 'const int Nmax = %i;\n', maxN);
fprintf(fid, '\n \n');
fprintf(fid, 'module PRISMLattice\n\n');
fprintf(fid, '    did : [1..didMax] init didMax;\n');
fprintf(fid, '    vid : [1..vidMax] init vidMax;\n\n');
fprintf(fid, '    currN : [0..Nmax] init 0;\n');
fprintf(fid, '    currK : [0..Nmax] init 0;\n');
fprintf(fid, '    s : [0..1] init 1;\n');
fprintf(fid, '    s2 : [0..1] init 1;\n');
fprintf(fid, '    s3 : [0..1] init 1;\n');
fprintf(fid, '    s4 : [0..1] init 1;\n');

%% Stateful LEC
% fprintf(fid, '    prevDet : [0..1] init 1;\n\n');
% fprintf(fid, '    currN : [0..1] init 0;\n');
% fprintf(fid, '    [] currN<Nmax&currK<Nmax&prevDet=0 -> 0.75:(currN''=currN+1)&(currK''=currK+1)&(prevDet''=0) + 0.25:(currN''=currN+1)&(prevDet''=1);\n\n');
% fprintf(fid, '    [] currN<Nmax&currK<Nmax&prevDet=1 -> 0.25:(currN''=currN+1)&(currK''=currK+1)&(prevDet''=0) + 0.75:(currN''=currN+1)&(prevDet''=1);\n\n');

%% Stateless LEC
% fprintf(fid, '    currN : [0..Nmax] init 0;\n');
% fprintf(fid, '    [] currN<Nmax&currK<Nmax -> 0.5:(currN''=currN+1)&(currK''=currK+1) + 0.5:(currN''=currN+1);\n\n');

%% Stateless LEC Precomputed K and N
% fprintf(fid, '    [] currN=0&currK=0 -> 0.001:(currN''=1)&(currK''=0) + 0.027:(currN''=1)&(currK''=1) + 0.243:(currN''=1)&(currK''=2) + 0.729:(currN''=1)&(currK''=3);\n\n');
% fprintf(fid, '    [] currN=0&currK=0 -> 0.125:(currN''=1)&(currK''=0) + 0.375:(currN''=1)&(currK''=1) + 0.375:(currN''=1)&(currK''=2) + 0.125:(currN''=1)&(currK''=3);\n\n');

% N=5, p(det)=0.5
% fprintf(fid, '    [] currN=0&currK=0&did>1&vid>1 -> 0.03125:(currN''=1)&(currK''=0) + 0.15625:(currN''=1)&(currK''=1) + 0.3125:(currN''=1)&(currK''=2) + 0.3125:(currN''=1)&(currK''=3) + 0.15625:(currN''=1)&(currK''=4) + 0.03125:(currN''=1)&(currK''=5);\n\n');


% N=7, p(det)=0.9
% fprintf(fid, '    [] currN=0&currK=0&did>1&vid>1 -> 0.0000001:(currN''=1)&(currK''=0) + 0.0000063:(currN''=1)&(currK''=1) + 0.0001701:(currN''=1)&(currK''=2) + 0.0025515:(currN''=1)&(currK''=3) + 0.0229635:(currN''=1)&(currK''=4) + 0.1240029:(currN''=1)&(currK''=5) + 0.3720087:(currN''=1)&(currK''=6) + 0.4782969:(currN''=1)&(currK''=7);\n\n');
% fprintf(fid, '\n \n');

% N=5, p(det)=0.9
fprintf(fid, '    [] currN=0&currK=0&did>1&vid>1 -> 0.00001:(currN''=5)&(currK''=0) + 0.00045:(currN''=5)&(currK''=1) + 0.0081:(currN''=5)&(currK''=2) + 0.0729:(currN''=5)&(currK''=3) + 0.32805:(currN''=5)&(currK''=4) + 0.59049:(currN''=5)&(currK''=5);\n\n');
fprintf(fid, '\n \n');

% N=3, p(det)=0.9
% fprintf(fid, '    [] currN=0&currK=0&did>1&vid>1 -> 0.001:(currN''=1)&(currK''=0) + 0.027:(currN''=1)&(currK''=1) + 0.243:(currN''=1)&(currK''=2) + 0.729:(currN''=1)&(currK''=3);\n\n');
% fprintf(fid, '\n \n');



%% Filter by reachability
reachabilityMatrix = zeros(didMax,vidMax);
reachabilityMatrix(didMax,vidMax)=1;
for i=didMax:-1:2
    for j = vidMax:-1:2
        currcell = lattice(i,j);
        currdid = currcell.did;
        currvid = currcell.vid;
        
        if(reachabilityMatrix(currdid,currvid)==0)
            continue
        end
     
        currv = (currvid-1)*deltav;
        currd = (currdid)*deltad;
        stoppingDist = (currv^2)/(2*amax);
%         if(stoppingDist+safetyThresh>= currd)
%             continue
%         end
%         TTC = (currd-safetyThresh)/(currv);
%         if(TTC<3 && currv>=5)
%             continue
%         end
        
        currTransMap = currcell.nextPoints;
        currMapKeys = keys(currTransMap);
        for k = 1:length(currMapKeys)
            key = currMapKeys{k};
            if key == 0
                continue
            end
   
            val = currTransMap(key);
            
            for l = 1:length(val)
                    nextPointsTrans = val{l};
                    for m = 1:size(nextPointsTrans,1)
                        nextPointdid = nextPointsTrans(m,1);
                        nextPointvid = nextPointsTrans(m,2);                     
                        reachabilityMatrix(nextPointdid,nextPointvid)=1;
                    end
            end
        end
    end
end

xs = [];
ys = [];
for i=2:didMax
    for j = 2:vidMax
        if(reachabilityMatrix(i,j)==1)
            xs = [xs i*deltad];
            ys = [ys j*deltav];
        end
    end
end


% figure(1); clf;
% plot(xs,ys,'b*');
% xlabel('Distance')
% ylabel('Velocity')


safetyThreshInd = floor(safetyThresh/deltad);
for i=safetyThreshInd+1:didMax
    for j = 2:vidMax
%         fprintf(fid, '\n \n');
        currcell = lattice(i,j);
        currdid = currcell.did;
        currvid = currcell.vid;
        
        if(reachabilityMatrix(currdid,currvid)==0 && trimmed)
            continue
        end
        currv = (currvid-1)*deltav;
        currd = (currdid)*deltad;
        stoppingDist = (currv^2)/(2*amax);
%         if(stoppingDist+safetyThresh>= currd)
            %% Stateful LEC
%             fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, currN, currK, nextPointvid, round(nextPointdid));
            %% Stateless LEC
%             fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, currN, currK, nextPointvid, round(nextPointdid));
            %% Stateless LEC precomputed K and N transitions
%             fprintf(fid, '    [] vid=%i&did=%i -> (did''=1);\n', currvid, currdid);
            
%             continue
%         end
%         TTC = (currd-safetyThresh)/(currv);
%         if(TTC<3 && currv>=5)
%             fprintf(fid, '    [] vid=%i&did=%i -> (did''=1);\n', currvid, currdid);
%             continue
%         end
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
            
            allDidNextAre1=1;
            for l = 1:length(val)
                nextPointsTrans = val{l};
                for m = 1:size(nextPointsTrans,1)
                    nextPointdid = nextPointsTrans(m,1);
                    nextPointvid = nextPointsTrans(m,2);
                    if((~(nextPointdid<=safetyThreshInd)) && ~(nextPointdid==(safetyThreshInd+1) && nextPointvid>1))
%                     if((~(nextPointdid<=safetyThreshInd)))
%                     if(nextPointdid>1)
                        allDidNextAre1=0;
                        break
                    end
                end   
            end

            if allDidNextAre1==1
                %% Stateful LEC
%                     fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, currN, currK, nextPointvid, round(nextPointdid));
                %% Stateless LEC
%                     fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, currN, currK, nextPointvid, round(nextPointdid));
                %% Stateless LEC precomputed K and N transitions
                fprintf(fid, '    [] vid=%i&did=%i -> (did''=1);\n', currvid, currdid);
                
            else
                for l = 1:length(val)
                    currK=l-1;
                    nextPointsTrans = val{l};

                    allPointsSame=1;
                    for m = 1:size(nextPointsTrans,1)-1
                        nextPointdid1 = nextPointsTrans(m,1);
                        nextPointvid1 = nextPointsTrans(m,2);
                        
                        nextPointdid2 = nextPointsTrans(m+1,1);
                        nextPointvid2 = nextPointsTrans(m+1,2);
                        
                        if(nextPointdid1==nextPointdid2 && nextPointvid1 && nextPointvid2)
                            continue
                        end
                        allPointsSame=0;
                        break;
                    end
                    for m = 1:size(nextPointsTrans,1)
                        nextPointdid = nextPointsTrans(m,1);
                        nextPointvid = nextPointsTrans(m,2);
                        
                        if(nextPointdid==(safetyThreshInd+1) && nextPointvid>=2)
                            fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (did''=1);\n', currvid, currdid, 1, currK);
                        elseif(nextPointdid<=(safetyThreshInd))
                            fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (did''=1);\n', currvid, currdid, 1, currK);
                        else
                            %% Stateful LEC
%                          fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, currN, currK, nextPointvid, round(nextPointdid));
                           %% Stateless LEC
%                          fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, currN, currK, nextPointvid, round(nextPointdid));
                           %% Stateless LEC precomputed K and N transitions
                            fprintf(fid, '    [] vid=%i&did=%i&currN=%i&currK=%i -> (vid''=%i)&(did''=%i)&(currN''=0)&(currK''=0);\n', currvid, currdid, 1, currK, nextPointvid, round(nextPointdid));
                        end
                    end
                end
            end
        end
    end
end

fprintf(fid, '\n \n');
fprintf(fid, 'endmodule\n');
fclose(fid);
end

