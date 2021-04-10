function[] = printControllerWaterTankMultiTank(lattice, maxN, fid,deltawl,numTanks)

wlContLowThresh=20;
wlContUpThresh=80;

wlContLowThreshid = floor((wlContLowThresh+1)/deltawl)+1;
wlContUpThreshid = floor((wlContUpThresh+1)/deltawl)+1;

for i=1:numTanks
    if(mod(wlContLowThresh,2) == 0 && mod(wlContUpThresh,2) == 1)
        fprintf(fid,'    [] currN=1&wlidPer%i<=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=1)&(tankFlag''=%i)&(tankFlag''=%i);\n', i, wlContLowThreshid, i, i, i+1);
        fprintf(fid,'    [] currN=1&contAction%i=0&wlidPer%i>%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=0)&(tankFlag''=%i);\n', i, i, wlContLowThreshid, i, i, i+1);

        fprintf(fid,'    [] currN=1&contAction%i!=0&wlidPer%i<=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=1)&(tankFlag''=%i);\n', i, i, wlContUpThreshid, i, i, i+1);
        fprintf(fid,'    [] currN=1&wlidPer%i>%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=0)&(tankFlag''=%i);\n', i, wlContUpThreshid, i, i, i+1);
    elseif(mod(wlContLowThresh,2) == 0 && mod(wlContUpThresh,2) == 0)
        fprintf(fid,'    [] currN=1&wlidPer%i<=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=1)&(tankFlag''=%i);\n', i, wlContLowThreshid, i, i, i+1);
        fprintf(fid,'    [] currN=1&contAction%i=0&wlidPer%i>%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=0)&(tankFlag''=%i);\n', i, i, wlContLowThreshid, i, i, i+1);

        fprintf(fid,'    [] currN=1&contAction%i!=0&wlidPer%i<=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=1)&(tankFlag''=%i);\n', i, i, wlContUpThreshid, i, i, i+1);
        fprintf(fid,'    [] currN=1&wlidPer%i>=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=0)&(tankFlag''=%i);\n', i, wlContUpThreshid, i, i, i+1);

    elseif(mod(wlContLowThresh,2) == 1 && mod(wlContUpThresh,2) == 1)
        fprintf(fid,'    [] currN=1&wlidPer%i<=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=1)&(tankFlag''=%i);\n', i, wlContLowThreshid, i, i, i+1);
        fprintf(fid,'    [] currN=1&contAction%i=0&wlidPer%i>=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=0)&(tankFlag''=%i);\n', i, i, wlContLowThreshid, i, i, i+1);

        fprintf(fid,'    [] currN=1&contAction%i!=0&wlidPer%i<=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=1)&(tankFlag''=%i);\n', i, i, wlContUpThreshid, i, i, i+1);
        fprintf(fid,'    [] currN=1&wlidPer%i>%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=0)&(tankFlag''=%i);\n', i, wlContUpThreshid, i, i, i+1);

    else
        fprintf(fid,'    [] currN=1&wlidPer%i<=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=1)&(tankFlag''=%i);\n', i, wlContLowThreshid, i, i+1);
        fprintf(fid,'    [] currN=1&contAction%i=0&wlidPer%i>=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=0)&(tankFlag''=%i);\n', i, i, wlContLowThreshid, i, i+1);

        fprintf(fid,'    [] currN=1&contAction%i!=0&wlidPer%i<=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=1)&(tankFlag''=%i);\n', i, i, wlContUpThreshid, i, i+1);
        fprintf(fid,'    [] currN=1&wlidPer%i>=%i&sink=0&tankFlag=%i -> (currN''=1)&(contAction%i''=0)&(tankFlag''=%i);\n', i, wlContUpThreshid, i, i+1);

    end
    fprintf(fid,'\n\n');
end


fprintf(fid,'    [] currN=1&sink=0&tankFlag=%i&contAction1!=contAction2 -> (currN''=2)&(tankFlag''=1);\n',(numTanks+1));
fprintf(fid,'    [] currN=1&sink=0&tankFlag=%i&contAction1=0&contAction2=0 -> (currN''=2)&(tankFlag''=1);\n',(numTanks+1));
fprintf(fid,'    [] currN=1&sink=0&tankFlag=%i&contAction1=1&contAction2=1&wlidPer1<=wlidPer2 -> (currN''=2)&(tankFlag''=1)&(contAction2''=0);\n',(numTanks+1));
fprintf(fid,'    [] currN=1&sink=0&tankFlag=%i&contAction1=1&contAction2=1&wlidPer2<=wlidPer1 -> (currN''=2)&(tankFlag''=1)&(contAction1''=0);\n',(numTanks+1));

fprintf(fid,'\n\n');


% add logic to pick control action

end