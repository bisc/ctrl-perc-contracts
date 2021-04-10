# Perception Bundle Abstractions
A repository for models and source code related to probabilistic safety estimation via perception bundle abstractions. 

The directory structure is as follows:
- code: This directory contains the code for generating and running the models, along with code for generting counter examples to the monotonicity of safety rule.
- models: This directory contains the generated models for the NFM 2021 submission.
- results: This directory contains the data and visuals for the NFM 2021 submission, along with the code to generate the visuals.
- old: old stuff, miscellaneous stuff. This directory can be ignored.

## Using Wolfram/Mathematica Implementations

All of the perception bundling, some visualizations, and some experiments are implemented on the Wolfram language/Mathematica stack. It has different parts described below.

### Installing Wolfram Script

Requirements: [Wolfram Script](https://www.wolfram.com/wolframscript/) version 1.5+. 

To run the scripts in this software package, you need to dowload and install a free version of the Wolfram Engine: 

1) Download and install the [Wolfram Engine](https://www.wolfram.com/engine/) for your OS. 
2) Create a Wolfram ID account (if you do not have one). 
3) Accept the terms of the [free license](https://www.wolfram.com/engine/free-license)
4) Run "wolframscript" in your command line
5) Input your Wolfram ID and password into the prompt

### Running Wolfram scripts

The scripts are files with .wls extensions that generate bundled perception distributions. Their output is typically sent to the command line or in a set of files, depending on the script. 

All scripts are standalone and run as follows: 
```wolframscript <scriptname.wls> <arg1> <arg2> ... 
```

### Running Mathematica notebook 
The notebooks implement various exploratory experiments, visualizations, and cached bundlings.

Requirements: For editing access, you require [Wolfram Mathematica](https://www.wolfram.com/mathematica/), version 12.1+. You can obtain a [free 30-day trial](https://www.wolfram.com/mathematica/trial/) or you find yourself be at an instutition with an [academic license](https://www.wolfram.com/mathematica/pricing/colleges-universities/). For read-only access, you can download a free [Wolfram Player](https://www.wolfram.com/player/).

Instructions:
1) Open a desired .nb notebook, 
2) Either run all it (Ctrl+A, Shift+Enter) or line-by-line (select a line, Shift+Enter).
