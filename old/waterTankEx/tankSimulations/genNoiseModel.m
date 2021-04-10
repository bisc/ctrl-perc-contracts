
numTrialsPerWl = 100;
wlMax=100;

totalTrials = numTrialsPerWl*wlMax;


mul = 0;
muu = 0;
skew = 0;
sigmau=5;
sigmal=2;

noiseCounts = [0 0 0 0 0 0 0 0 0 0 0 0 0];
noiseUpperCounts = 0;
noiseLowerCounts = 0;
for wl=1:wlMax
    for j=1:numTrialsPerWl
        % run perception
        r=rand;
        if(r<0.1)
            noise=-100;
        elseif(r>0.9)
            noise=100;
        else
            if(wl<30 || wl>70)
                sigma=sigmau;
            else
                sigma=sigmal;
            end
            mu=muu-muu*wl/wlMax+mul;
            n1 = randn;
            n2 = randn;
            delta = skew/(sqrt(1+skew^2));
            noise = mu + sigma*(delta*abs(n1) + n2*sqrt(1-delta^2));
        end
        noise = round(noise);
        if(noise<-6)
            noiseLowerCounts=noiseLowerCounts+1;
        elseif(noise>6)
            noiseUpperCounts=noiseUpperCounts+1;
        else
            noiseInd = noise+7;
            noiseCounts(noiseInd)=noiseCounts(noiseInd)+1;
        end
    end
    
end

noiseLowerCounts/totalTrials
noiseUpperCounts/totalTrials
noiseCounts/totalTrials
