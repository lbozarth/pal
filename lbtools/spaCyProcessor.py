import spacy
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
import pandas as pd
import numpy as np
from multiprocessing import Pool

nlp = spacy.load('en')
def get_POS(x, poses):
    doc = nlp(x)
    resss = []
    for token in doc:
        if token.pos_ in poses:
            resss.append(token.lemma_)
    return resss

nlp = spacy.load('en')
def get_POS_map(x, poses):
    doc = nlp(x)
    resss = [[token.lemma_, token.pos_] for token in doc]
    df = pd.DataFrame(resss, columns=['lemma', 'pos'])
    df= df[df['pos'].isin(poses)]
    return df['lemma'].tolist()

if __name__ == '__main__':
    pass