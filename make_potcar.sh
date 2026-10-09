#!/bin/bash
# Build POTCAR in the current job folder from the species line of POSCAR.
# Set PP to the cluster's PBE potential directory before use (contains Mo_pv/, S/, Pt/ ...).
PP=${VASP_PP_PATH:?set VASP_PP_PATH to the PBE POTCAR directory}
declare -A MAP=( [Mo]=Mo_pv [S]=S [Pt]=Pt )
rm -f POTCAR
for el in $(sed -n '6p' POSCAR); do
  f="$PP/${MAP[$el]}/POTCAR"
  [ -f "$f" ] || { echo "missing $f"; exit 1; }
  cat "$f" >> POTCAR
done
grep TITEL POTCAR
