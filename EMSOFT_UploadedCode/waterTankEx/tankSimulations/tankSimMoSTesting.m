
numTrials = 1000;

inflow = 13;
outflow = 4;
wlMax=100;
wlInit=50;
ctrlThreshLower = 20;
ctrlThreshUpper = 80;

numSteps = 25;

crashProbs = [];

wls = 1:wlMax;
[wl1s,wl2s] = meshgrid(wls,wls);

for wl1Init=1:wlMax
    tempCrashProbs = [];
    for wl2Init=1:wlMax
        unsafes = 0;
        for j=1:numTrials
            contAction1 = 0;
            contAction2 = 0;

            unsafe = 0;
            % noise params
            mul = 0;
            muu = 0;
            skew = 0;
            sigmau=2;
            sigmal=1;

            wl1 = wlInit;
            wl2 = wlInit;
            noises1 = [];
            noises2 = [];
            wls1 = [];
            wlPers1 = [];
            wls2 = [];
            wlPers2 = [];
            for i=1:numSteps
                % run perception
                r=rand;
                if(r<0.1)
                    noise=-100;
                elseif(r>0.9)
                    noise=100;
                else
                    if(wl1<30 || wl1>70)
                        sigma=sigmau;
                    else
                        sigma=sigmal;
                    end
                    mu=muu-muu*wl1/wlMax+mul;
                    n1 = randn;
                    n2 = randn;
                    delta = skew/(sqrt(1+skew^2));
                    noise = mu + sigma*(delta*abs(n1) + n2*sqrt(1-delta^2));
                end
                noises1 = [noises1; noise];
                %     noise = randn*sigma + mu;
                wlPer1 = wl1+noise;
                wlPers1 = [wlPers1;wlPer1];

                % compute control
                if wlPer1<ctrlThreshLower || (wlPer1<ctrlThreshUpper && contAction1==1)
                    contAction1=1;
                else
                    contAction1=0;
                end

                %% tank 2 perception
                r=rand;
                if(r<0.1)
                    noise=-100;
                elseif(r>0.9)
                    noise=100;
                else
                    if(wl2<30 || wl2>70)
                        sigma=sigmau;
                    else
                        sigma=sigmal;
                    end
                    mu=muu-muu*wl2/wlMax+mul;
                    n1 = randn;
                    n2 = randn;
                    delta = skew/(sqrt(1+skew^2));
                    noise = mu + sigma*(delta*abs(n1) + n2*sqrt(1-delta^2));
                end
                noises2 = [noises2; noise];
                %     noise = randn*sigma + mu;
                wlPer2 = wl2+noise;
                wlPers2 = [wlPers2;wlPer2];
                %     wlPer

                % compute control
                if wlPer2<ctrlThreshLower || (wlPer2<ctrlThreshUpper && contAction2==1)
                    contAction2=1;
                else
                    contAction2=0;
                end    




                %% Global controller
                contActionG1=contAction1;
                contActionG2=contAction2;
                if(contAction1==1 && contAction2==1 && wlPer1<=wlPer2)
                    contActionG2=0;
                    contActionG1=1;
                elseif(contAction1==1 && contAction2==1 && wlPer1>wlPer2)
                    contActionG1=0;
                    contActionG2=1;
                end

                %% Uupdate water levels
                %     contAction
                % simulate tanks
                wl1=wl1-outflow+contActionG1*inflow;
                wl2=wl2-outflow+contActionG2*inflow;
                if(wl1<=0 || wl1>wlMax || wl2<=0 || wl2>wlMax)
                    unsafe=1;
                    break
                end
                wls1 = [wls1;wl1];
                wls2 = [wls2;wl2];

            end

            %     unsafe
            unsafes=unsafes+unsafe;
        end
        unsafes/numTrials
        tempCrashProbs = [tempCrashProbs unsafes/numTrials];
        
    end
    crashProbs = [crashProbs; tempCrashProbs];
    
end

figure(1)
surf(wl1s,wl2s,crashProbs)
