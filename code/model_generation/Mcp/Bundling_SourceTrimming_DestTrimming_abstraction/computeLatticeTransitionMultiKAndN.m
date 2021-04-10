function [didf,vidf,lattice] = computeLatticeTransitionMultiKAndN(did,vid,lattice,Ns,Ks,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq)
%UNTITLED5 Given a starting point in the lattice and a sequence of K and N
%values, compute the resulting point in the lattice


numTrials = length(Ns);
tempCell = lattice(did,vid);
for i=1:numTrials
    N = Ns(i);
    K = Ks(i);
    cellMap = tempCell.nextPoints;
    if(~isKey(cellMap,N))
        % If the cell doesn't contain the transitions for the given N, add
        % the N transition to all points in the lattice
        % This is a bit dumb, since we could get away with just adding the
        % N to the current cell's mapping, but this way requires less code
        lattice = addLatticeTransitions(lattice,N,deltad,deltav,B1,B2,fmu,amax,Thd,xThresh,TTCThresh,freq);
    end
    nextCellNVals = cellMap(N);
    nextCelldid = nextCellNVals(K+1,1);
    nextCellvid = nextCellNVals(K+1,2);
    tempCell=lattice(nextCelldid,nextCellvid);
end

didf = tempCell.did;
vidf = tempCell.vid;

end

