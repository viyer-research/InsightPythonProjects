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

#Initilize globals
count = 0
val = 0
_maxSize=10000
strOut = None
dictWords = { }
lstFileNames = []
cacheWriteLines = []

################################################################################
output_file_name = os.path.join(os.getcwd(),"wc_output","wc_result.txt")
print "Processing dir:", os.path.join(os.getcwd(),"wc_input","....")

###### Check batch environment ####################################################
###################################################################################
# Check output directory
#################################################################################

try:
       output_file_object = open(output_file_name, 'w')
except Exception, error:
       print error
       sys.exit(1)

######## Environment OK ###################################################################
# Process ALL 
#
######################################################################################

for ltemFile in os.listdir(os.path.join(os.getcwd(),"wc_input")):
    if os.path.isfile(os.path.join(os.getcwd(),"wc_input",ltemFile)):
#       print "is a file path", ltemFile
       try:
        lstFileNames.append(ltemFile)
       except Exception, error:
         print error 
         sys.exit(1)
    else:
        print "not a file", ltemFile
print "Processsing total input file counts:", len(lstFileNames), "...\n" 

for inputCurr in lstFileNames:
    file_object = open(os.path.join(os.getcwd(), "wc_input", inputCurr), 'rU')
    try:
        for line in file_object:
            try:
                line.decode('ascii')
            except Exception, error:
                continue ## skip blanks
            for c in string.punctuation:
                line= line.replace(c,"")
            ## Strip Punctuation
            for word in line.split():
            #print word
                count = count + 1
                # make lower case and stem  word
                word = word.lower()
                word = PorterStemmer().stem_word(word)
                if word in dictWords: 
#                   print 'found', d1[word]
                    val = dictWords[word]
                    dictWords[word] = val + 1
                else:
#                   print 'not found'
                    dictWords[word] = 1
    finally:
        file_object.close()
    
print "Completed building index of total words seen:\n", count
print "Total unique words in list:\n", len(dictWords)
keys = dictWords.keys()
keys.sort()
print "Sorted <word,counts> pairs\n"

output_file_object = open(output_file_name, 'w')
print "Writing to output dir:", output_file_name, "\n"

#################################################################################
# Write to output directory
#############################################################################
try:
    for skey in keys:
#	    print skey, "\t", dictWords[skey]
        strOut = str(skey) + "\t\t\t\t" + str(dictWords[skey]) + "\n"
        cacheWriteLines.append(strOut)
        if (len(cacheWriteLines) > _maxSize):
            output_file_object.writelines(cacheWriteLines)
            cacheWriteLines = []
finally:
    if ( len(cacheWriteLines) > 0 and len(cacheWriteLines) < _maxSize ):
        output_file_object.writelines(cacheWriteLines)
        cacheWriteLines = []
    output_file_object.close()
    print "Results writing complete!"
