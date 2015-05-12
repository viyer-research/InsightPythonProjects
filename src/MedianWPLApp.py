
################################################################################################
#Title:	        Running Median Words Per Line (WPL) Program Python Code for Insight Data Engineering (June 2015)
#File:          MeanWPLApp.py
#Author:	    currport2000@msn.com
#Status:	    Active 
#Type:	        <WPL>
#Created:	    05-May-2015
#Post-History:	05-May-2015
# Dependency:   numpy   for median
#               pip     for installation
################################################################################

import os
import sys
import numpy as np
import string
from optparse import OptionParser

###############################################################################
#                         Functions definitions                               #
#                                                                             #
###############################################################################
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

def medianWPLfn(lstWordCount):
    lstWordCount.sort()
    return np.median(lstWordCount)

###############################################################################
#                         Global variables                                    #
#                                                                             #
###############################################################################

#Initilize globals
count_words_per_line = 0.0
running_median = 0.0
val = 0
_maxSize = 10000
dictWords = {}
lstFileNames = []
lst_running_median = list()
output_file_object=None
input_file_object=None
curr_line_no = 0
write_cache = []


################################################################################
#                                Parse cmd line options                        #
#                                                                              #
#                                                                              #
################################################################################
parser = OptionParser()
inputargs = parser.parse_args()
if len(inputargs[1]) < 2:
   print "incorrect number of arguments\n"
   print "usage: prog <./input_dir> <./output_dir>/wc_result.txt\n"
   sys.exit(1)

output_file_name = inputargs[1][1]
input_dir = inputargs[1][0]
print "Processing dir:", input_dir,"....\n"

##################################################################################
#                            Check batch environment                             #
#                             Check output directory                             #
##################################################################################

try:
       output_file_object = open(output_file_name, 'w')
except Exception, error:
       print error
       sys.exit(1)

#####################################################################################
#                                                                                   #
#                               Program Environment OK                              #
#                                Process ALL files                                  #
#                                                                                   #
#####################################################################################
print "Enter Batch Processing WPL-Median..>> \n"
try:
    for ltemFile in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir,ltemFile)):
           try:
            lstFileNames.append(ltemFile)
           except Exception, error:
                print error 
                sys.exit(1)
        else:
                print "not a file", ltemFile
except Exception, error:
       print error 
       sys.exit(1)

print ">> Processsing total input file counts:", len(lstFileNames), "...\n" 

curr_line_no = 0

for inputCurr in lstFileNames:
    input_file_object = open(input_dir + "//" + inputCurr, 'rU')
    try:
        for line in input_file_object:
            count_words_per_line = 0
            for word in line.split():
                count_words_per_line = count_words_per_line + 1

            try:
                  lst_running_median.append(count_words_per_line)
                  running_median = medianWPLfn(lst_running_median)
                  write_cache.append(str(running_median)+"\n")
            except Exception, error:
                  print error
                  sys.exit(1)
            # flush to disk
            if (len(write_cache) >= _maxSize):
                output_file_object.writelines(write_cache)
                write_cache = []
            curr_line_no = curr_line_no + 1
    finally:
        if (len(write_cache) > 0 and len(write_cache) < _maxSize):
           output_file_object.writelines(write_cache)
           write_cache = []

        input_file_object.close()

######################################################################################
#            Print Summary of Median Word Per Line Statistics                        #
#                                                                                    #
######################################################################################

print "Total number of lines processed:", curr_line_no
output_file_object.close()

#############################################################################
#                   End of Batch Processing                                 #
#############################################################################
print ">> End of batch processing"
print "Results writing complete."




