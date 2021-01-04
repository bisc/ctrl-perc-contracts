#!/bin/bash

# First and only parameter: java filename to compile and run

fname=$1 

javac $fname PrismConnectorAPI.java -cp ":lib/*:"

export LD_LIBRARY_PATH=/data2/mcleav/latticeScalability/lib:

java -classpath lib/*:. -Djava.library.path=lib/: ${fname%.java}
