function[] = printLECModelWaterTankMultiTank(lattice, maxN, fid,deltawl,numTanks)

numBins = 13;
latticeSize=size(lattice);
wlidMax=latticeSize(2);

fprintf(fid, '\n \n');

% LECProbs = [0.0184    0.0198    0.0181    0.0190    0.0179    0.0215    0.0176    0.0219    0.0174    0.0200    0.0193    0.0162    0.0185];
% LECLowerProb = 0.3801;
% LECUpperProb = 0.3743;

LECProbs = [0.020500000000000   0.024900000000000   0.036800000000000   0.053500000000000   0.076400000000000   0.095200000000000   0.102800000000000   0.093200000000000   0.073300000000000   0.052700000000000   0.040700000000000   0.023000000000000   0.020200000000000];
LECLowerProb = 0.143200000000000;
LECUpperProb = 0.143600000000000;
% LECModel
% LECProbs = [0.0184,0.0198,0.0181,0.0190,0.0179,0.0215,0.0176,0.0219,0.0174,0.0200,0.0193,0.0162,0.0185];

for j=1:numTanks-1
    for k=1:wlidMax
        currcell=lattice(k);
        wlid=currcell.wlid;
        wl = currcell.wl;

        fprintf(fid, '    [] currN=0&sink=0&tankFlag=%i&wlid%i=%i -> ',j,j,wlid);
        fprintf(fid, "%i:(wlidPer%i'=0)&(tankFlag'=%i) + %i:(wlidPer%i'=wlidMax)&(tankFlag'=%i) + ",LECLowerProb,j,j+1,LECUpperProb,j,j+1);
        for i=1:numBins
            nextwl = wl+i-(numBins+1)/2;
            nextwlid = ceil(nextwl/deltawl);
            nextwlid = max(0,nextwlid);
            nextwlid = min(wlidMax-1,nextwlid);
            if i==numBins
                fprintf(fid, ' %i:(wlidPer%i''=%i)&(tankFlag''=%i);\n' , LECProbs(i), j, nextwlid,j+1);
            else
                fprintf(fid, ' %i:(wlidPer%i''=%i)&(tankFlag''=%i) +' , LECProbs(i), j, nextwlid,j+1);
            end
        end
    end
end


j=numTanks;

for k=1:wlidMax
    currcell=lattice(k);
    wlid=currcell.wlid;
    wl = currcell.wl;

    fprintf(fid, '    [] currN=0&sink=0&tankFlag=%i&wlid%i=%i -> ',j,j,wlid);
    fprintf(fid, "%i:(wlidPer%i'=0)&(currN'=1)&(tankFlag'=1) + %i:(wlidPer%i'=wlidMax)&(currN'=1)&(tankFlag'=1) + ",LECLowerProb,j,LECUpperProb,j);
    for i=1:numBins
        nextwl = wl+i-(numBins+1)/2;
        nextwlid = ceil(nextwl/deltawl);
        nextwlid = max(0,nextwlid);
        nextwlid = min(wlidMax-1,nextwlid);
        
        
        if i==numBins
            fprintf(fid, ' %i:(wlidPer%i''=%i)&(currN''=1)&(tankFlag''=1);\n' , LECProbs(i), j, nextwlid);
        else
            fprintf(fid, ' %i:(wlidPer%i''=%i)&(currN''=1)&(tankFlag''=1) +' , LECProbs(i), j, nextwlid);
        end
    end
end
    
    
fprintf(fid, '\n \n');


end