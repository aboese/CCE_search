#!/usr/bin/python
# https://nvd.nist.gov/cce.cfm

import sys, getopt

from bs4 import BeautifulSoup
from lxml import etree
from pprint import pprint
import hashlib

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hf:i:",["find=","infile="])
    except getopt.GetoptError:
        print ('collect.py -c <cce_identifier> -w <search word>')
        sys.exit(2)

# Default Location of input file (in local dir)
    infile = "nvdcce-0.1-feed.xml"
    findit = None

# Check for command line options
    for opt, arg in opts:
        if opt == '-h':
            print ('collect.py -c <cce_identifier> -w <search word>')
            sys.exit()
        elif opt in ("-f", "--find"):
            findit = arg
        elif opt in ("-i", "--infile"):
            infile = arg

# CCE is our dict of lists. Indexing is done by hash of description, to shorten the description,
# and because the CCE number is not always containing a unique description
    cce = dict()

# nvdcce-0.1-feed.xml
    audit_data = open(infile,'r',encoding='utf-8').read()

# user feedback
    print (infile +"  opened.")

# If searching for word, list the item being searched
    if (findit):
        print ("Looking for "+ findit)

# *******************************
# *** Initial Parsing Section ***
# *******************************

# Pull in our xml file
    soup = BeautifulSoup(audit_data, "lxml")

# http://scap.nist.gov/schema/configuration/0.1

#    customAll = soup.find_all("entry")

# Each entry xml is a new item to parse
    for item in soup.find_all('entry'):
#     <config:summary - Probably only one of these...but code as if there were many.
        summaries = item.find_all(['config:summary'])
#     <config:cce-id - Should only ever be one of these....but code as if there were many
        cce_numbers = item.find_all(['config:cce-id'])

# These are cce numbers tags found in each item
        for cce_number in cce_numbers:
# Parse the CCE number itself out of the tag
            cnum =  cce_number.get_text()

# These are summary tags found in each item
        for summary in summaries:
# Parse the summary itself out of the tag
            description = summary.get_text()
# Create a hash of the summary description
            hash_index = hashlib.md5(description.encode('utf-8','ignore')).hexdigest()

# if the new item exists, then there is already a list there - append to the list.
            if hash_index in cce:
                cce[hash_index].append(cnum.encode('utf-8','ignore'))
            else:
# if the new item does not exist, then the first item in the list contains the description
                cce[hash_index] = [description.encode('utf-8','ignore')]
# the second(...N) items contain the associated CCE numbers 
                cce[hash_index].append(cnum.encode('utf-8','ignore'))


# *******************************
# *** Output Printing Section ***
# *******************************

    for key in cce:
        this_list = cce[key]
        this_list = map (str, this_list)
        if (findit):
            temp_str = "\n".join('{} : {}'.format(*k) for k in enumerate(this_list))
# Allow comma delimited list of words
            if ( len(findit.split(',')) > 1 ):
                findthem = findit.split(',')
                foundall = True
                for finditem in findthem:
                    if ( temp_str.find(finditem) < 1):
                        foundall = False
                if ( foundall ):
                    print ("\n")
                    print ( temp_str )                    
            else:
                if ( temp_str.find(findit) > 0):
                    print ("\n")
                    print ( temp_str )
        else:
            print ("\n")
            print ( "\n".join(this_list) )

def in_fragment(phrase, fragments):
    return any(x in phrase for x in fragments)


if __name__ == "__main__":
   main(sys.argv[1:])
