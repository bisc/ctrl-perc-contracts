#!/usr/bin/env wolframscript
(* ::Package:: *)

If[Length@$ScriptCommandLine < 2, 
Print["Not enough command line params"];
Quit[]
];


ntanks = ToExpression@$ScriptCommandLine[[2]];


If[Length@$ScriptCommandLine != 2+ntanks, 
Print["Not enough command line params"];
Quit[]
];


trueWls = ToExpression/@ ($ScriptCommandLine[[3 ;; 2+ntanks]]);


Clear[ts, is, os, ew]; 
(* tank size *) 
ts  = 101; 
(* inflow speed *) 
is = 13; 
(* outflow speed *) 
os = 4; 
(* upper threshold *) 
ut = 80; 
(* lower threshold *) 
lt = 20; 
(* error window width (applied to both ends); not counting the big false positive and big false negative *) 
ew = 4;


percWlDistrs = With[{truelvl = #}, 
With[{perclvl = #}, 
If[perclvl == 0, p[min] + Plus@@(p/@Range[-ew, -truelvl]), 0] + (* for min level: adding up min and all values too low *) 
If[perclvl == ts, p[max] + Plus@@(p/@Range[ts-truelvl, ew]), 0] + (* for max level:  adding up max and all values too high *) 
If[0 < perclvl < ts, If[-ew <= perclvl-truelvl<= ew, p[perclvl-truelvl], 0]  , 0] 
] & /@ Range[0, ts] 
] &/@ trueWls;


(*Print["Perception distributions:"]
Print[percWlDistrs]*)


(* not filling if the perceived water level is too high in all tanks *)
pNofill = Times@@(Plus@@(#[[lt+1;;]]) & /@ percWlDistrs)


(*Print["Chance of not filling:"]
Print[pNofill]*)


(* probability that one tank with a certain level will have a filling priority over the other:
- either when the second one is perceived too full 
- or when it is below/belowequal the level of the first (depending on lexicographic order)  *) 
pPrior[t1num_, t2num_, t1Wl_]:= 
If[t1Wl<lt+1, (* it will only get filled if this certain level is below the lower threshold *) 
Plus@@(percWlDistrs[[t2num, lt + 1 ;;]]) + (* probability the other tank wont need filling *)
Plus@@If[t1num < t2num,  
percWlDistrs[[t2num, 1;;t1Wl ]] , (* fine to go all the way to that level *)
percWlDistrs[[t2num, 1;;t1Wl - 1]](* need to stop one level below *) 
],
0];


(*Print["Pprior test:"]
Print[pPrior[1, 2, 3]]
Print[pPrior[2, 1, 1]]*)


nextTankProb = With[{tankNum = #},
Plus@@( With[{curlvl = #}, 
percWlDistrs[[tankNum, curlvl]]* (* chance of taking this level *) 
Times@@( (* priority over all the other tanks given this level *)  
pPrior[tankNum, #, curlvl] & /@ (DeleteCases[Range[1, ntanks], tankNum])
) 
] & /@ Range[1, lt+1])  (* going through all fillable levels *) 
] & /@ Range[1, ntanks] (* going through all tanks *) 


(* simplify the expression a bit *) 
nextTankProb = Simplify[#, Plus@@(p/@Range[-ew, ew]) + p[max] + p[min] == 1] &/@ nextTankProb


(*Print["nextTankProb:"]
Print[nextTankProb] *) 


(*Print["Distr test:"]
Print[Simplify[pNofill + Plus@@nextTankProb , Plus@@(p/@Range[-ew, ew]) + p[max] + p[min] \[Equal] 1]]*)


If[Simplify[pNofill + Plus@@nextTankProb , Plus@@(p/@Range[-ew, ew]) + p[max] + p[min] == 1] != 1,
Print["Distribution test failed: not adding up to 1!"]]


Print[pNofill]


Print[#] & /@ nextTankProb
