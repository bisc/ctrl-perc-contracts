function[] = printLECModelWaterTank(lattice, maxN, fid,deltawl)

numBins = 18;
numBinsid = numBins/deltawl;

maxwlid = size(lattice,2);

fprintf(fid, '\n \n');

fprintf(fid, '    [] currN=0&sink=0 -> ');

for i=0:1:numBinsid-1
    if(i==numBinsid-1)
        fprintf(fid, ' %i: (wlidPer''=wlid+%i)&(currN''=1);\n' , 1/numBinsid, (numBinsid-1)/2-i);
    else
        fprintf(fid, ' %i: (wlidPer''=wlid+%i)&(currN''=1) +' , 1/numBinsid, (numBinsid-1)/2-i);
    end
    
end


fprintf(fid, '\n \n');


end