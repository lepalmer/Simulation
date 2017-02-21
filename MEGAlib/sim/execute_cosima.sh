#!/bin/bash
FILES=/Users/reginamcaputo/Desktop/BurstCube/Simulations/MEGAlib/source/FarFieldPointSource_test.source
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  cosima $f
done
