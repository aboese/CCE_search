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

    cce_search = None
    word_search = None

# Default Location
    infile = "nvdcce-0.1-feed.xml"

    for opt, arg in opts:
        if opt == '-h':
            print ('collect.py -c <cce_identifier> -w <search word>')
            sys.exit()
        elif opt in ("-f", "--find"):
            findit = arg
        elif opt in ("-i", "--infile"):
            infile = arg

    cce = dict()

# nvdcce-0.1-feed.xml
    audit_data = open(infile,'r',encoding='utf-8').read()

    print (infile +"  opened.")
    if (findit):
        print ("Looking for "+ findit)



    soup = BeautifulSoup(audit_data, "lxml")


# http://scap.nist.gov/schema/configuration/0.1


    customAll = soup.find_all("entry")
    for item in soup.find_all('entry'):
    #print (item.stripped_strings )
#     <config:summary - Probably only one of these...but code as if there were many.
        summaries = item.find_all(['config:summary'])
#     <config:cce-id - Should only ever be one of these....but code as if there were many
        cce_numbers = item.find_all(['config:cce-id'])


        for cce_number in cce_numbers:
#        print ( cce_number.get_text() )
            cnum =  cce_number.get_text()

        for summary in summaries:
            description = summary.get_text()
            hash_index = hashlib.md5(description.encode('utf-8','ignore')).hexdigest()


            if hash_index in cce:
                cce[hash_index].append(cnum.encode('utf-8','ignore'))
            else:
                cce[hash_index] = [description.encode('utf-8','ignore')]
                cce[hash_index].append(cnum.encode('utf-8','ignore'))


#pprint(cce)


    for key in cce:
        this_list = cce[key]
        this_list = map (str, this_list)
        if (findit):
            temp_str = "\n".join(this_list)
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