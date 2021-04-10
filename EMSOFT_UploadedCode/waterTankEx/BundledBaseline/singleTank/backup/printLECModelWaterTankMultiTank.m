function[] = printLECModelWaterTankMultiTank(lattice, maxN, fid,deltawl,numTanks)

numBins = 9;
numBinsid = ceil(numBins/deltawl);

maxwlid = size(lattice,2);

fprintf(fid, '\n \n');

for j=1:numTanks-1
    fprintf(fid, '    [] currN=0&sink=0&tankFlag=%i -> ',j);
    fprintf(fid, "0.1:(wlidPer%i'=0)&(currN'=0)&(tankFlag'=%i) + 0.1:(wlidPer%i'=101)&(currN'=0)&(tankFlag'=%i) + ",j,j+1,j,j+1);

    for i=0:1:numBinsid-1
        if(i==numBinsid-1)
            fprintf(fid, ' %i: (wlidPer%i''=wlid%i+%i)&(currN''=0)&(tankFlag''=%i);\n' , 0.8*1/numBinsid, j, j, (numBinsid-1)/2-i,j+1);
        else
            fprintf(fid, ' %i: (wlidPer%i''=wlid%i+%i)&(currN''=0)&(tankFlag''=%i) +' , 0.8*1/numBinsid, j, j, (numBinsid-1)/2-i,j+1);
        end

    end

end

j=numTanks;
fprintf(fid, '    [] currN=0&sink=0&tankFlag=%i -> ',j);
fprintf(fid, "0.1:(wlidPer%i'=0)&(currN'=1)&(tankFlag'=1) + 0.1:(wlidPer%i'=101)&(currN'=1)&(tankFlag'=1) + ",j,j);

for i=0:1:numBinsid-1
    if(i==numBinsid-1)
        fprintf(fid, ' %i: (wlidPer%i''=wlid%i+%i)&(currN''=1)&(tankFlag''=1);\n' , 0.8*1/numBinsid, j, j, (numBinsid-1)/2-i);
    else
        fprintf(fid, ' %i: (wlidPer%i''=wlid%i+%i)&(currN''=1)&(tankFlag''=1) +' , 0.8*1/numBinsid, j, j, (numBinsid-1)/2-i);
    end

end

    
    
    
    
    
fprintf(fid, '\n \n');


end