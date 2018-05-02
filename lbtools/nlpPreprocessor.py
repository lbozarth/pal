'''
Created on Mar 1, 2018

@author: lbozarth
'''
import nltk
from nltk.corpus import stopwords
from nltk import PorterStemmer
from nltk import WordNetLemmatizer
from nltk import word_tokenize
import string, re

import preprocessor as p
p.set_options(p.OPT.MENTION, p.OPT.URL, p.OPT.RESERVED)

#make translator object
punct = str.maketrans('','',string.punctuation)
sw = stopwords.words('english')
custom_sw = ['thank', 'rt', 'https', 'http', 'say', 'ha', 'tweet', 'thanks', 'posted', 'photo', 'via']
sw.extend(custom_sw)
ps = PorterStemmer()
lem = WordNetLemmatizer()

url_marker = r'^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$'
class NLPPrep:
    doc_orig = None
    doc_mod = None
    lst = []
    
    def __init__(self, doc):
        self.doc_orig = doc
        self.doc_mod = doc

    def cleanTweet(self):
        self.doc_mod = p.clean(self.doc_mod)
        return self

    def removePunc(self):
        self.doc_mod = self.doc_mod.translate(punct)
        return self

    def removeUrl(self):
        self.doc_mod = re.sub(url_marker, "", self.doc_mod,  flags=re.MULTILINE)
        # print(self.doc_mod)
        return self
    
    def tokenizeToLst(self):
        lst = word_tokenize(self.doc_mod)
        lst = [x.strip() for x in lst if x.strip()!=""]
        self.lst = lst
        return self
    
    def removeStopwords_lst(self):
        self.lst = [word.strip() for word in self.lst if word.strip() not in sw]
        return self
    
    def stem_lst(self):
        self.lst = [ps.stem(word) for word in self.lst]
        return self
    
    def lemma_lst(self):
        self.lst = [lem.lemmatize(word) for word in self.lst]
        return self
    
    def get_lst(self):
        return self.lst
    
    def get_lst_doc(self, joiner=" "):
        return joiner.join(self.lst)
    
    def get_doc_orig(self):
        return self.doc_orig
    
    def get_doc_mod(self):
        return self.doc_mod
    
if __name__ == '__main__':
    pass