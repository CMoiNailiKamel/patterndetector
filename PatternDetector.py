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
from urlextract import URLExtract
import sys
import subprocess
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


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
print ("removing the stop words....\nCleaning the resumes....\nExtracting Text .......")
print (filtered)
#get the name from the resume
name  = str(filtered[0])+' ' +str(filtered[1])
print ("Name : " + name)

#using regular expressions we extract phone numbers and mail ids
import re
#get contact info - from resume
#email
email = ""
match_mail = re.search(r'[\w\.-]+@[\w\.-]+', resume)
#match_mail =re.search(r'(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])')
#handling the cases when mobile number is not given
if(match_mail != None):
    email = match_mail.group(0)
print ("Email : " + email)


website = ""
match_website = re.search(r'[\w\.-]+@[\w\.-]+', resume)

if(match_website != None):
    website = match_website.group(0)
print ("Website : " + website)

#mobile number
mobile = ""
match_mobile = re.search(r'((?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?)',resume)
#handling the cases when mobile number is not given
if(match_mobile != None):
    mobile = match_mobile.group(0)

print("Mobile : " +  mobile)











