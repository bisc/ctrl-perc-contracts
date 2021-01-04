#!/usr/bin/env wolframscript
(* ::Package:: *)

(*Print[$ScriptCommandLine]*)


(* getting from command line: m, lthis, lnext, "{k1,k2,...kg}" "{n1,n2,...ng}" vote *)


m = ToExpression[$ScriptCommandLine[[2]]];  (* controller window size, works across all intervals *) 
lthis = ToExpression[$ScriptCommandLine[[3]]]; (* detection history for this interval *) 
lnext = ToExpression[$ScriptCommandLine[[4]]];  (* detection history for next  interval *)  
ks = ToExpression[$ScriptCommandLine[[5]]]; 
ns = ToExpression[$ScriptCommandLine[[6]]]; 
vote = StringTrim@ToString@ToExpression[$ScriptCommandLine[[7]]]; (* voting policy, either "maj" or "all" *)

(* maxn = 15;  (* max value of N for both *) 
maxl = 3; (* max conditioning history -- for hot start, for code that iterates over them *) 
 (* window size, roundup(m/2) votes needed for a high-level outcome *) 
pastLen = Max[maxl, m-1]; (* how many steps to preserve and produce the distribution for. This is the length of the starting tuple *)  *)


Print["Solving for m=", m, " lthis=", lthis, " lnext=", lnext, " ks=", ks, " ns=", ns, " vote=", vote];


thisPastLen = Max[lthis, m-1];
nextPastLen = Max[lnext, m-1];


(* Print["Compiling..."]*)


(* get windowed function but in compileable code *) 
(*cf3= FunctionCompile@Function[
{Typed[tuple,TypeSpecifier["NumericArray"]["UnsignedInteger8",1]],Typed[start,TypeSpecifier["NumericArray"]["UnsignedInteger8",1]],
Typed[m,"UnsignedInteger8"]
}, 
Module[{head,winIt,localct=0, kct=0},
kct= 0;
For[head=1,head \[LessEqual] Length@tuple,head++,
localct= 0; 
For[winIt=head, winIt>head-m, winIt--, 
localct += If[winIt>0,tuple[[winIt]],start[[ winIt+m ]]];
(*Print["    ",localct];*)
];
(*Print[kct,localct];*)
If[localct>Quotient[m,Typed[2,"UnsignedInteger8"]], kct++]
]; 
kct
]
];

toNA[list_]:= NumericArray[list, "UnsignedInteger8"];
callCf3[tup_, st_]:= callCf3[tup,st]=cf3[toNA@tup, toNA@st, m];
*)
(*cf4=Compile[{{tuple,_Integer,1}, {start, _Integer,1}, {m,_Integer}},
Module[{head,winIt,localct=0, kct=0},
kct= 0;
For[head=1,head \[LessEqual] Length@tuple,head++,
localct= 0; 
For[winIt=head, winIt>head-m, winIt--, 
localct += If[winIt>0,tuple[[winIt]],start[[ winIt+m ]]];
(*Print["    ",localct];*)
];
(*Print[kct,localct];*)
If[localct>Quotient[m,2], kct++]
]; 
kct
]
];
(*cf3 = CompiledCodeFunction[Signature: {TypeSpecifier[NumericArray][UnsignedInteger8,1],TypeSpecifier[NumericArray][UnsignedInteger8,1],UnsignedInteger8}\[Rule]Integer64];*)
toNA[list_]:= NumericArray[list, "UnsignedInteger8"];
*)
 
 (* how much to look back is determined by the size of the start tuple 
 implication: better pass one here that is m-sized *) 
cf5majvote=Compile[{{tuple,_Integer,1}, {start, _Integer,1}},
Module[{head,winIt,localct=0, kct=0, mlocal = Length@start+1},
kct= 0;
For[head=1,head <= Length@tuple,head++,
localct= 0; 
For[winIt=head, winIt>head-mlocal, winIt--, 
localct += If[winIt>0,tuple[[winIt]],start[[ winIt+mlocal-1 ]]];
(*Print["    ",localct];*)
];
(*Print[kct,localct];*)
If[localct>Quotient[mlocal,2], kct++]
]; 
kct
]
];

cf6allvotes =Compile[{{tuple,_Integer,1}, {start, _Integer,1}},
Module[{head,winIt,localct=0, kct=0, mlocal = Length@start+1},
kct= 0;
For[head=1,head <= Length@tuple,head++,
localct= 0; 
For[winIt=head, winIt>head-mlocal, winIt--, 
localct += If[winIt>0,tuple[[winIt]],start[[ winIt+mlocal-1 ]]];
(*Print["    ",localct];*)
];
(*Print[kct,localct];*)
If[localct>mlocal-1, kct++];
]; 

kct
]
];

callCf5[tup_, st_]:= callCf5[tup,st]=cf5majvote[tup, st];
callCf6[tup_, st_]:= callCf6[tup,st]=cf6allvotes[tup, st];


selectedWinFun = Switch[vote, 
"maj",callCf5 , 
"all",callCf6, 
_, Print["Voting policy error. "];Throw["Voting policy " <> vote <> " is not known. Stopping."]]



(*Print["Compiled"]*)


(*Print[callCf3[#[[2]],#[[1]]]&/@Tuples[{ Tuples[{0,1},3], Tuples[{0,1},5]}]];*)


stringifySymb = {p[{}]-> p,p[{x_}]:> Symbol["p" <> ToString@x],  p[{x_,y_}]:> Symbol["p" <> ToString@x <> ToString@y],  p[{x_,y_,z_}]:> Symbol["p" <> ToString@x <> ToString@y <> ToString@z]};
(* less efficient: removeEmptiesAndSingletons =  {{}\[Rule]0,  a_List /;Length@a\[Equal]1 \[RuleDelayed] First@a};*) 
(*also option: _[x_]\[RuleDelayed]x*)
removeEmptiesAndSingletons =  {{}->0,   {a_} :> a };
lst2str[list_]:= StringRiffle[list,", "]; 

(* probability per position 
uses lthis to look back, passed through condlen
start is thisPastLen-long though; we are just adding it, doesn't matter *) 
outcomeHotProbHstarNmax[pos_, tuple_, ourstart_] :=p[Join[ourstart,tuple][[Length@ourstart+pos+#]]&/@Range[-lthis, -1]]/.stringifySymb ;

(* hot-start probability of a whole tuple
it needs to pass start down, otherwise it doesn't care  *) 
tupleHotProbHstarNmax[tuple_, ourstart_,nmax_] := Times@@( 
If[tuple[[#]]==1, outcomeHotProbHstarNmax[#, tuple, ourstart], (1 - outcomeHotProbHstarNmax[#, tuple, ourstart])]&/@ Range[1,nmax]);

(* works well *) 
(*tuplesByVerdictsFast3[start_,k1_,k2_,n1_,n2_] := With[{v1=#[[1]], v2=#[[2]]},
Select[Tuples[{0,1},n2],
 v1\[Equal](callCf3[#[[1;;n1]], start]\[GreaterEqual] k1)\[And] v2\[Equal](callCf3[#, start]\[GreaterEqual] k2)&]
]&/@Tuples[{False, True},2];

(* works well too? *) 
tuplesByVerdictsFast4[start_,k1_,k2_,n1_,n2_] := With[{v1=#[[1]], v2=#[[2]]},
Select[Tuples[{0,1},n2],
 v1\[Equal](callCf4[#[[1;;n1]], start]\[GreaterEqual] k1)\[And] v2\[Equal](callCf4[#, start]\[GreaterEqual] k2)&]
]&/@Tuples[{False, True},2];*)

(*tuplesByVerdictsFast5[start_,k1_,k2_,n1_,n2_] := With[{v1=#[[1]], v2=#[[2]]},
Select[Tuples[{0,1},n2],
 v1==(callCf5[#[[1;;n1]], start]>= k1)\[And] v2==(callCf5[#, start]>= k2)&]
]&/@Tuples[{False, True},2];*)

(* a version for arbitrary count of K and N
needs to know the verdicts, which is easy
passes down the start, which it needs to limit to m-1, otherwise callCf5 judges the controller window wrong *) 
tuplesByVerdictsFast[ourstart_,ks_,ns_,winfun_] := With[{verdicts = #},
Select[Tuples[{0,1},Max@ns],
 With[{tup=#}, verdicts == (winfun[tup[[1;;#[[2]]]], ourstart[[-m+1;;-1]] ]>=#[[1]]&/@Inner[List,ks, ns, List])]
&]
]&/@ (* all possible verdict outcomes *) Tuples[{False, True},Length@ns];

(* within each group of K, organize by the last pastLen tuples *) 
(*tuplesHotByVerdictByEnd[start_,k1_,k2_,n1_,n2_,tbvFun_] := With[{tupForVer = #}, 
With[{end = #},
Select[(*Join[start, tupForVer]*)tupForVer,Join[start, #][[-pastLen ;;-1]]==end&]
]& /@(*all ends*)  Tuples[{0,1},pastLen]
]& /@ tbvFun[start,k1,k2,n1,n2];*)

(* list version: within each group of K, organize by the next interval's pastLen tuples 
dependent on next pastLen because it groups by ends *) 
tuplesHotByVerdictByEndlist[start_,ks_,ns_,winfun_] := With[{tupForVer = #}, 
With[{end = #},
Select[tupForVer,Join[start, #][[-nextPastLen ;;-1]]==end&]
]& /@(*all ends*)  Tuples[{0,1},nextPastLen]
]& /@ tuplesByVerdictsFast[start,ks,ns,winfun];

(* pair version *) 
(*probsByVerdictByEnd[start_, condLen_,k1_,k2_,n1_,n2_, tbvFun_] :=
Apply[Plus, 
Map[
(tupleHotProbHstarNmax[#, start,condLen,Max[n1,n2]]&),tuplesHotByVerdictByEnd[start,k1,k2,n1,n2, tbvFun], {3}
 ], 
{2}];*)

(* list version *) 
probsByVerdictByEndlist[ourstart_, ks_,ns_, winfun_] :=
Apply[Plus, 
Map[
(tupleHotProbHstarNmax[#, ourstart,Max@ns]&),tuplesHotByVerdictByEndlist[ourstart,ks,ns, winfun], {3}
 ], 
{2}];






(*Print[probsByVerdictByEnd[{0,1,0}, 3,2,3,3,5, tuplesByVerdictsFast4]]*)


(*Print[probsByVerdictByEnd[{0,0,0}, pastLen,k1,k2,n1,n1, tuplesByVerdictsFast4]]*)


(*Print["Tuples", Tuples[{0,1}, pastLen]]
Print["Pastlen ",  pastLen]*)




(* final execution breaks it down by our starts *) 
res = {lst2str@#,lst2str@(ToString[#,InputForm]&/@(probsByVerdictByEndlist[#, ks,ns, selectedWinFun]))} & /@ Tuples[{0,1}, thisPastLen];


Print[#[[1]],": ",#[[2]]] & /@ res
