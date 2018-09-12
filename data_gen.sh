#!/bin/bash
python setgen.py $1 0 > covered.csv
python setgen.py $1 1 > sigstr.csv
python setgen.py $1 1 > sigval.csv
python setgen.py $1 2 > cost.csv
