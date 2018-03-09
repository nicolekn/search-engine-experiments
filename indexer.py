import sys
import re
import string
import json

# global declarations for doclist, postings, vocabulary
docids = []
postings = {}
vocab = []


# main is used for offline testing only
def main():
    # code for testing offline
    if len(sys.argv) != 2:
        print('usage: ./indexer.py file')
        sys.exit(1)
    filename = sys.argv[1]

    try:
        input_file = open(filename, 'r')
    except (IOError) as ex:
        print('Cannot open ', filename, '\n Error: ', ex)

    else:
        page_contents = input_file.read()  # read the input file
        url = 'http://www.' + filename + '/'
        print(url, page_contents)
        make_index(url, page_contents)

    finally:
        input_file.close()


def write_index():
    # declare refs to global variables
    global docids
    global postings
    global vocab

    # writes to index files: docids, vocab, postings
    outlist1 = open('docids.txt', 'w')
    outlist2 = open('vocab.txt', 'w')
    outlist3 = open('postings.txt', 'w')

    json.dump(docids, outlist1)
    json.dump(vocab, outlist2)
    json.dump(postings, outlist3)

    outlist1.close()
    outlist2.close()
    outlist3.close()

    return

from html.parser import HTMLParser

class HTMLCleaner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def clean_html(page_contents):
    # function to remove mark up
    cleaner=HTMLCleaner()
    cleaner.feed(page_contents)
    return cleaner.get_data()

from bs4 import BeautifulSoup
	

def make_index(url, page_contents):
    # declare refs to global variables
    global docids
    global postings
    global vocab

    # first convert bytes to string if necessary
    if isinstance(page_contents, bytes):
        page_contents = page_contents.decode('utf-8','ignore')

    print('===============================================')
    print('make_index: url = ', url)
    print('===============================================')
    
    
    #page_text = clean_html(page_contents)
    soup=BeautifulSoup(page_contents);
    for i in soup.findAll(['script','style']):
        i.extract();
    page_text=soup.get_text();
    #add url to docids table
    docids.append(url)
    #retive document id
    document_id=docids.index(url)
    #vocab table
    
    #remove punctuation
    translationNoPunct=page_text.maketrans('','',string.punctuation) 
    nopunct=page_text.translate(translationNoPunct)
    #remove whitespace characters
    translationNoTabs=nopunct.maketrans('','','\t')
    notabs=nopunct.translate(translationNoTabs)
    translationNoLines=notabs.maketrans('','','\n')
    nolines=notabs.translate(translationNoLines)
    translationNoReturns=nolines.maketrans('','','\r')
    nospaces=nolines.translate(translationNoReturns)

    
    
    tokens=nospaces.split(' ')
    #add word to vocab if not already there
    #otherwise retrieve the word's index in the list
    for word in tokens:
        if(word.lower() in vocab):
            term_id=vocab.index(word.lower())
            theword,docid,instances=postings[term_id]
            instances=instances+1
            postings[term_id]=theword,docid,instances
            #postings[term_id][1]=postings[term_id][1]+1
        else:
            vocab.append(word.lower())
            term_id=vocab.index(word.lower())
            postings[term_id]=word.lower(),document_id,0
    
    
    

    #### end of your code ####
    return


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
