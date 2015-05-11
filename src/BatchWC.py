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

#Initilize globals
count = 0
val = 0
dictWords = { }
lstFileNames = []

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
            for word in line.split():
            #print word
                count = count + 1
                if word in dictWords: 
#                   print 'found', d1[word]
                    val = dictWords[word]
                    dictWords[word] = val + 1
                else:
#                   print 'not found'
                    dictWords[word] = 1
    finally:
        file_object.close()
    
print "Complete building index of total words:\n", count
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
	    output_file_object.write(str(skey)+"\t"+str(dictWords[skey])+"\n")
finally:
    output_file_object.close()
    print "Results writing complete!"
