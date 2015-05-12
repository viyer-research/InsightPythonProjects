#!/usr/bin/env bash

# example of the run script for running the word count

# first I'll load all my dependencies
apt-get install python-pandas
#
# Dependencies for pip in both the programs
# 1. pip install nltk
# 2. pip install optparse
# 3. pip install numpy
#
#
# next I'll make sure that all my programs (written in Python in this example) have the proper permissions
chmod a+x BatchWC.py
chmod a+x MedianWPLApp.py

# finally I'll execute my programs, with defaults
python ./src/BatchWC.py ./wc_input ./wc_output/wc_result.txt
python ./src/MedianWPLApp.py ./wc_input ./wc_output/med_result.txt
