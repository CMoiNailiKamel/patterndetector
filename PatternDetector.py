from gensim.models import Word2Vec, KeyedVectors
#from pattern3 import es
import textract
from os import listdir
from os.path import isfile, join
import numpy as np
from scipy import spatial
from sklearn import decomposition
import matplotlib.pyplot as plt
import pickle
import string
import re
import code
from urlextract import URLExtract
import sys
import subprocess
import os
from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def getPhone(inputString, infoDict, debug=False):
    '''
    Given an input string, returns possible matches for phone numbers. Uses regular expression based matching.
    Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
    Modules required: clock from time, code.
    '''

    number = None
    try:
        pattern = re.compile(
            r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
        # Understanding the above regex
        # +91 or (91) -> [+(]? \d+ -?
        # Metacharacters have to be escaped with \ outside of character classes; inside only hyphen has to be escaped
        # hyphen has to be escaped inside the character class if you're not incidication a range
        # General number formats are 123 456 7890 or 12345 67890 or 1234567890 or 123-456-7890, hence 3 or more digits
        # Amendment to above - some also have (0000) 00 00 00 kind of format
        # \s* is any whitespace character - careful, use [ \t\r\f\v]* instead since newlines are trouble
        match = pattern.findall(inputString)
        # match = [re.sub(r'\s', '', el) for el in match]
        # Get rid of random whitespaces - helps with getting rid of 6 digits or fewer (e.g. pin codes) strings
        # substitute the characters we don't want just for the purpose of checking
        match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el)) > 6]
        # Taking care of years, eg. 2001-2004 etc.
        match = [re.sub(r'\D$', '', el).strip() for el in match]
        # $ matches end of string. This takes care of random trailing non-digit characters. \D is non-digit characters
        match = [el for el in match if len(re.sub(r'\D', '', el)) <= 15]
        # Remove number strings that are greater than 15 digits
        try:
            for el in list(match):
                # Create a copy of the list since you're iterating over it
                if len(el.split('-')) > 3: continue  # Year format YYYY-MM-DD
                for x in el.split("-"):
                    try:
                        # Error catching is necessary because of possibility of stray non-number characters
                        # if int(re.sub(r'\D', '', x.strip())) in range(1900, 2100):
                        if x.strip()[-4:].isdigit():
                            if int(x.strip()[-4:]) in range(1900, 2100):
                                # Don't combine the two if statements to avoid a type conversion error
                                match.remove(el)
                    except:
                        pass
        except:
            pass
        number = match
    except:
        pass

    infoDict['phone'] = number

    if debug:
        print
        "\n", pprint(infoDict), "\n"
        #code.interact(local=locals())
    return number

def getEmail(inputString, infoDict, debug=False):
        '''
        Given an input string, returns possible matches for emails. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''

        email = None
        try:
            pattern = re.compile(r'\S*@\S*')
            matches = pattern.findall(inputString)  # Gets all email addresses as a list
            email = matches
        except Exception as e:
            print
            e

        infoDict['email'] = email

        if debug:
            print
            "\n", pprint(infoDict), "\n"
            #code.interact(local=locals())
        return email


def read_All_CV(filename):
    text = textract.process(filename)
    return text.decode('utf-8')

alltext = ' '
yd = read_All_CV("/tmp/cv.pdf")
alltext += yd + " "
alltext = alltext.lower()

print(alltext)

print ("processing..... \nplease wait....")

resume = alltext
#Tokenizing/ Filtering the resume off stopwords and punctuations
print ("tokenizing the given file ......")
tokens = word_tokenize(resume)
punctuations = ['(',')',';',':','[',']',',']
stop_words = stopwords.words('english')

#storing the cleaned resume
filtered = [w for w in tokens if not w in stop_words and  not w in string.punctuation]
print("removing the stop words....\nCleaning the resumes....\nExtracting Text .......")
print(filtered)

print("removing the stop words....\nCleaning the resumes....\nExtracting Text .......")
print(filtered)
#get the name from the resume
name = str(filtered[0]) + ' ' + str(filtered[1])
print("Name : " + name)
print("removing the stop words....\nCleaning the resumes....\nExtracting Text .......")
print(filtered)

email = ""
website = ""
mobile = ""
info = {}

email = getEmail(resume, info, False)
mobile = getPhone(resume, info, False)

print("Name : ", name)
print("Mobile : ", mobile)
print("Email : ", email)












