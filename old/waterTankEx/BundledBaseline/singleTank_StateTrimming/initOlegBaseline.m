function [initializedLattice] = initOlegBaseline(wlMax,deltawl)
%initLattice This function creates the lattice structure (2-d array of lattice points)

numPointsDist = ceil(wlMax/deltawl)+1;

for i=0:numPointsDist
%     wl = (i)*deltawl;
    wll = (i-1)*deltawl;
    wlu = (i)*deltawl;
    if(wll >= wlMax/2)
        wl=wlu;
    elseif(wlu <= wlMax/2)
        wl=wll;
    else
        wl=wlMax/2;
    end
    latticePoint.wl = wl;
    latticePoint.wlid = i;
    latticePoint.nextPoints=containers.Map(0,[i 0]);
    initLattice(i+1)=latticePoint;
end
initializedLattice = initLattice;



end