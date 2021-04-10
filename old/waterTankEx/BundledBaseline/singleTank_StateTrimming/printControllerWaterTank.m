function[] = printControllerWaterTank(lattice, maxN, fid,deltawl)


%     [] currN=1&contAction=0&wlPer<wlContLowThresh&sink=0 -> (currN'=2)&(contAction'=1);
%     [] currN=1&contAction!=0&wlPer<wlContUpThresh&sink=0 -> (currN'=2)&(contAction'=1);
%     [] currN=1&contAction=0&wlPer>=wlContLowThresh&sink=0 -> (currN'=2)&(contAction'=0);
%     [] currN=1&wlPer>=wlContUpThresh&sink=0 -> (currN'=2)&(contAction'=0);

wlContLowThresh=10;
wlContUpThresh=40;

wlContLowThreshid = floor((wlContLowThresh+1)/deltawl)+1;
wlContUpThreshid = floor((wlContUpThresh+1)/deltawl)+1;

% wlContLowThreshid = wlContLowThresh/deltawl;
% wlContUpThreshid=wlContUpThresh/deltawl;

fprintf('\n');

if(mod(wlContLowThresh,2) == 0 && mod(wlContUpThresh,2) == 1)
%     wlContLowThreshid = wlContLowThresh/deltawl;
%     wlContUpThreshid=wlContUpThresh/deltawl;
    fprintf(fid,'    [] currN=1&wlidPer<=%i&sink=0 -> (currN''=2)&(contAction''=1);\n',wlContLowThreshid);
    fprintf(fid,'    [] currN=1&contAction=0&wlidPer>%i&sink=0 -> (currN''=2)&(contAction''=0);\n', wlContLowThreshid);
    
    fprintf(fid,'    [] currN=1&contAction!=0&wlidPer<=%i&sink=0 -> (currN''=2)&(contAction''=1);\n', wlContUpThreshid);
    fprintf(fid,'    [] currN=1&wlidPer>%i&sink=0 -> (currN''=2)&(contAction''=0);\n', wlContUpThreshid);
elseif(mod(wlContLowThresh,2) == 0 && mod(wlContUpThresh,2) == 0)
%     wlContLowThreshid = wlContLowThresh/deltawl;
    fprintf(fid,'    [] currN=1&wlidPer<=%i&sink=0 -> (currN''=2)&(contAction''=1);\n',wlContLowThreshid);
    fprintf(fid,'    [] currN=1&contAction=0&wlidPer>%i&sink=0 -> (currN''=2)&(contAction''=0);\n', wlContLowThreshid);
    
%     wlContUpThreshid=wlContUpThresh/deltawl;
    fprintf(fid,'    [] currN=1&contAction!=0&wlidPer<=%i&sink=0 -> (currN''=2)&(contAction''=1);\n', wlContUpThreshid);
    fprintf(fid,'    [] currN=1&wlidPer>=%i&sink=0 -> (currN''=2)&(contAction''=0);\n', wlContUpThreshid);

elseif(mod(wlContLowThresh,2) == 1 && mod(wlContUpThresh,2) == 1)
%     wlContLowThreshid = wlContLowThresh/deltawl;
    fprintf(fid,'    [] currN=1&wlidPer<=%i&sink=0 -> (currN''=2)&(contAction''=1);\n',wlContLowThreshid);
    fprintf(fid,'    [] currN=1&contAction=0&wlidPer>=%i&sink=0 -> (currN''=2)&(contAction''=0);\n', wlContLowThreshid);

%     wlContUpThreshid=wlContUpThresh/deltawl;
    fprintf(fid,'    [] currN=1&contAction!=0&wlidPer<=%i&sink=0 -> (currN''=2)&(contAction''=1);\n', wlContUpThreshid);
    fprintf(fid,'    [] currN=1&wlidPer>%i&sink=0 -> (currN''=2)&(contAction''=0);\n', wlContUpThreshid);
    
else
%     wlContLowThreshid = wlContLowThresh/deltawl;
    fprintf(fid,'    [] currN=1&wlidPer<=%i&sink=0 -> (currN''=2)&(contAction''=1);\n',wlContLowThreshid);
    fprintf(fid,'    [] currN=1&contAction=0&wlidPer>=%i&sink=0 -> (currN''=2)&(contAction''=0);\n', wlContLowThreshid);

%     wlContUpThreshid=wlContUpThresh/deltawl;
    fprintf(fid,'    [] currN=1&contAction!=0&wlidPer<=%i&sink=0 -> (currN''=2)&(contAction''=1);\n', wlContUpThreshid);
    fprintf(fid,'    [] currN=1&wlidPer>=%i&sink=0 -> (currN''=2)&(contAction''=0);\n', wlContUpThreshid);

    
end
    
fprintf('\n\n');

end