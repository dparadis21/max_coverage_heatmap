#!/bin/bash
python setgen.py $1 > tmp
python settest.py tmp $2
