import sys
from bs4 import BeautifulSoup
from lbtools import  ioTools

def getLexicoderDictionary():
    content = ioTools.readFile_dump("../data_static/lexicon/policy_agendas_english.xml")
    content_xml = BeautifulSoup(content, 'lxml')
    # print(content_xml)
    eles = content_xml.find_all('pnode')
    dn = [c['name'].lower().strip() for c in eles]
    print(len(dn))
    d = set(dn)
    return d

lexi_dictionary = getLexicoderDictionary()
# print(lexi_dictionary)