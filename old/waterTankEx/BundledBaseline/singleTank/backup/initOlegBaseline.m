function [initializedLattice] = initOlegBaseline(wlMax,deltawl)
%initLattice This function creates the lattice structure (2-d array of lattice points)

if(deltawl==2)
    numPointsDist = ceil(wlMax/deltawl)+1;

    for i=1:numPointsDist
        wl = (i-1)*deltawl-1;
        latticePoint.wl = wl;
        latticePoint.wlid = i;
        latticePoint.nextPoints=containers.Map(0,[i 0]);
        initLattice(i)=latticePoint;
    end
    initializedLattice = initLattice;

elseif(deltawl==1)
    numPointsDist = ceil(wlMax/deltawl)+1;

    for i=1:numPointsDist
        wl = (i-1)*deltawl;
        latticePoint.wl = wl;
        latticePoint.wlid = i;
        latticePoint.nextPoints=containers.Map(0,[i 0]);
        initLattice(i)=latticePoint;
    end
    initializedLattice = initLattice;

    
    
else
    fprintf('Need to add this case explicitly');  
        
end

end