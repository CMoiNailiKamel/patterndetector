import nltk, os, subprocess, code, glob, re, traceback, sys, inspect
from time import clock, sleep
from pprint import pprint
import textract
import json
import zipfile
# import ner
#from convertPDFToText import convertPDFToText
#from convertDocxToText import convertDocxToText


class exportToCSV:
    def __init__(self, fileName='resultsCSV.txt', resetFile=False):
        headers = ['FILE NAME',
                   'NAME',
                   'EMAIL',
                   'PHONE'
                   ]
        if not os.path.isfile(fileName) or resetFile:
            # Will create/reset the file as per the evaluation of above condition
            fOut = open(fileName, 'w')
            fOut.close()
        fIn = open(fileName)  ########### Open file if file already present
        inString = fIn.read()
        fIn.close()
        if len(inString) <= 0:  ######### If File already exsists but is empty, it adds the header
            fOut = open(fileName, 'w')
            fOut.write(','.join(headers) + '\n')
            fOut.close()

    def write(self, infoDict):
        fOut = open('resultsCSV.txt', 'a+')
        # Individual elements are dictionaries
        writeString = ''
        try:
            writeString += str(infoDict['fileName']) + ','
            writeString += str(infoDict['name']) + ','

            if infoDict['email']:
                writeString += str(','.join(infoDict['email'][:4])) + ','
            if infoDict['phone']:
                writeString += str(','.join(infoDict['phone'][:4]))
            writeString += '\n'
            fOut.write(writeString)
        except:
            fOut.write('FAILED_TO_WRITE\n')
        fOut.close()

def read_All_CV(filename):
    extension = filename.split(".")[-1]
    if extension == "pdf":
        text = textract.process(filename, method='pdfminer')
    elif extension == "docx":
        tesxt = textract.process(filename, extension='docx')
    return text.decode('utf-8')


class Parse ():
    # List (of dictionaries) that will store all of the values
    # For processing purposes
    information = []
    inputString = ''
    tokens = []
    lines = []
    sentences = []

    def __init__(self, verbose=False):
        print('Starting Programme')
        fields = ["name", "address", "email", "phone", "mobile", "telephone", "residence status"]

        # Glob module matches certain patterns
        doc_files = glob.glob("/tmp/resumes/*.doc")
        docx_files = glob.glob("/tmp/resumes/*.docx")
        pdf_files = glob.glob("/tmp/resumes/*.pdf")
        rtf_files = glob.glob("/tmp/resumes/*.rtf")
        text_files = glob.glob("/tmp/resumes/*.txt")

        files = set(doc_files + docx_files + pdf_files + rtf_files + text_files)
        files = list(files)
        print("%d files identified" % len(files))

        for f in files:
            print("Reading File %s" % f)
            # info is a dictionary that stores all the data obtained from parsing
            info = {}

            #self.inputString = self.readFile(f)
            self.inputString = read_All_CV(f)
            info['extension'] = self.inputString
            info['fileName'] = f

            self.tokenize(self.inputString)

            self.getEmail(self.inputString, info)

            self.getPhone(self.inputString, info)

            self.getName(self.inputString, info)

            csv = exportToCSV()
            csv.write(info)
            self.information.append(info)
            print(info)

    def preprocess(self, document):
        '''
        Information Extraction: Preprocess a document with the necessary POS tagging.
        Returns three lists, one with tokens, one with POS tagged lines, one with POS tagged sentences.
        Modules required: nltk
        '''
        try:
            # Try to get rid of special characters
            try:
                document = document.decode('ascii', 'ignore')
            except:
                document = document.encode('ascii', 'ignore')
            # Newlines are one element of structure in the data
            # Helps limit the context and breaks up the data as is intended in resumes - i.e., into points
            lines = [el.strip() for el in document.split("\n") if len(el) > 0]  # Splitting on the basis of newlines
            lines = [nltk.word_tokenize(el) for el in lines]  # Tokenize the individual lines
            lines = [nltk.pos_tag(el) for el in lines]  # Tag them
            # Below approach is slightly different because it splits sentences not just on the basis of newlines, but also full stops
            # - (barring abbreviations etc.)
            # But it fails miserably at predicting names, so currently using it only for tokenization of the whole document
            sentences = nltk.sent_tokenize(document)  # Split/Tokenize into sentences (List of strings)
            sentences = [nltk.word_tokenize(sent) for sent in
                         sentences]  # Split/Tokenize sentences into words (List of lists of strings)
            tokens = sentences
            sentences = [nltk.pos_tag(sent) for sent in
                         sentences]  # Tag the tokens - list of lists of tuples - each tuple is (<word>, <tag>)
            # Next 4 lines convert tokens from a list of list of strings to a list of strings; basically stitches them together
            dummy = []
            for el in tokens:
                dummy += el
            tokens = dummy
            # tokens - words extracted from the doc, lines - split only based on newlines (may have more than one sentence)
            # sentences - split on the basis of rules of grammar
            return tokens, lines, sentences
        except Exception as e:
            print(e)

    def tokenize(self, inputString):
        try:
            self.tokens, self.lines, self.sentences = self.preprocess(inputString)
            return self.tokens, self.lines, self.sentences
        except Exception as e:
            print(e)

    def getEmail(self, inputString, infoDict, debug=False):
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
            print(e)


        infoDict['email'] = email

        if debug:
            print
            "\n", pprint(infoDict), "\n"
            code.interact(local=locals())
        return email

    def getPhone(self, inputString, infoDict, debug=False):
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
            code.interact(local=locals())
        return number

    def getName(self, inputString, infoDict, debug=False):
        '''
        Given an input string, returns possible matches for names. Uses regular expression based matching.
        Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
        Modules required: clock from time, code.
        '''

        # Reads Indian Names from the file, reduce all to lower case for easy comparision [Name lists]
        indianNames = open("allNames.txt", "r").read().lower()
        # Lookup in a set is much faster
        indianNames = set(indianNames.split())

        nameHits = []
        name = None

        try:
            # tokens, lines, sentences = self.preprocess(inputString)
            tokens, lines, sentences = self.tokens, self.lines, self.sentences
            # Try a regex chunk parser
            # grammar = r'NAME: {<NN.*><NN.*>|<NN.*><NN.*><NN.*>}'
            grammar = r'NAME: {<NN.*><NN.*><NN.*>*}'
            # Noun phrase chunk is made out of two or three tags of type NN. (ie NN, NNP etc.) - typical of a name. {2,3} won't work, hence the syntax
            # Note the correction to the rule. Change has been made later.
            chunkParser = nltk.RegexpParser(grammar)
            all_chunked_tokens = []
            for tagged_tokens in lines:
                # Creates a parse tree
                if len(tagged_tokens) == 0: continue  # Prevent it from printing warnings
                chunked_tokens = chunkParser.parse(tagged_tokens)
                all_chunked_tokens.append(chunked_tokens)
                for subtree in chunked_tokens.subtrees():
                    #  or subtree.label() == 'S' include in if condition if required
                    if subtree.label() == 'NAME':
                        for ind, leaf in enumerate(subtree.leaves()):
                            if leaf[0].lower() in indianNames and 'NN' in leaf[1]:
                                # Case insensitive matching, as indianNames have names in lowercase
                                # Take only noun-tagged tokens
                                # Surname is not in the name list, hence if match is achieved add all noun-type tokens
                                # Pick upto 3 noun entities
                                hit = " ".join([el[0] for el in subtree.leaves()[ind:ind + 3]])
                                # Check for the presence of commas, colons, digits - usually markers of non-named entities
                                if re.compile(r'[\d,:]').search(hit): continue
                                nameHits.append(hit)
                                # Need to iterate through rest of the leaves because of possible mis-matches
            # Going for the first name hit
            if len(nameHits) > 0:
                nameHits = [re.sub(r'[^a-zA-Z \-]', '', el).strip() for el in nameHits]
                name = " ".join([el[0].upper() + el[1:].lower() for el in nameHits[0].split() if len(el) > 0])


        except Exception as e:
            print
            traceback.format_exc()
            print
            e

        infoDict['name'] = name


        if debug:
            print
            "\n", pprint(infoDict), "\n"
            code.interact(local=locals())
        return name

if __name__ == "__main__":
    verbose = False
    if "-v" in str(sys.argv):
        verbose = True
p = Parse(verbose)