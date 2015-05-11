################################################################################################
#Title:	        BatchWCApp.py
#Description:   Word Count Program Python Code for Data Engineering (June 2015)
#Author:	    currport2000@msn.com
#Status:	    Active 
#Type:	        <key,Val> pairs
#Created:	    05-May-2015
#Post-History:	05-May-2015
#
################################################################################
import os
import sys
from nltk import PorterStemmer
import string
from optparse import OptionParser

################################################################################
#                               Function Definitions                           #
#                                                                              #
################################################################################
def StripPunc(line):
    for c in string.punctuation:
        line= line.replace(c," ")
    return line

###############################################################################
#                               Initilize globals                             #
#                                                                             #
#                                                                             #
###############################################################################
count = 0
val = 0
_maxSize=10000
strOut = None
dictWords = {}
lstFileNames = []
cacheWriteLines = []

################################################################################
#                                Parse cmd line options                        #
#                                                                              #
#                                                                              #
################################################################################
parser = OptionParser()
inputargs = parser.parse_args()
if len(inputargs) != 2:
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
print "Enter Batch Processing ..>> \n"
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

for inputCurr in lstFileNames:
    file_object = open(input_dir + "//" + inputCurr, 'rU')
    try:
        for line in file_object:
            try:
                line.decode('ascii')
            except Exception, error:
                continue ## skip blanks
            # Strip punctuations
            line = StripPunc(line)
            for word in line.split():
                count = count + 1
                # make word lower case and stem  word
                word = word.lower()
                word = PorterStemmer().stem_word(word)
                if word in dictWords: 
                    val = dictWords[word]
                    dictWords[word] = val + 1
                else:
                    dictWords[word] = 1
    finally:
        file_object.close()
############################################################################
#                    Print Summary Statistics                              #
############################################################################   
print "Completed building index of total words seen:\n", count
print "Total unique words after stemming in list:\n", len(dictWords)
keys = dictWords.keys()

###########################################################################
#                   Sort the dictionary list                              #
###########################################################################
keys.sort()
print ">> Sorted <word,counts> pairs\n"


#############################################################################
#                   Write to output directory with caching                  #
#############################################################################
output_file_object = open(output_file_name, 'w')
print ">> Writing to output dir:", output_file_name, "\n"

try:
    for skey in keys:
        # right justify
        strOut = "%25s%s%s%s" % (str(skey),"\t\t",str(dictWords[skey]), "\n")
        cacheWriteLines.append(strOut)
        if (len(cacheWriteLines) > _maxSize):
            output_file_object.writelines(cacheWriteLines)
            cacheWriteLines = []
finally:
    if ( len(cacheWriteLines) > 0 and len(cacheWriteLines) < _maxSize ):
        output_file_object.writelines(cacheWriteLines)
        cacheWriteLines = []
    output_file_object.close()

#############################################################################
#                   End of Batch Processing                                 #
#############################################################################
print ">> End of batch processing"
print "Results writing complete!"

