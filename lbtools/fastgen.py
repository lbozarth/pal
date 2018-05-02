'''
Created on Apr 15, 2017

@author: lbozarth
'''
import fasttext

if __name__ == '__main__':
    print("modeling")

    # Skipgram model
    model = fasttext.skipgram('../data/openstate/candidate_votesmart_fastText.txt', 'votesmart_w2v_skipgram_50', dim=50, loss='hs')
    print(len(model.words))  # list of words in dictionary


    #
    #     model = fasttext.skipgram('../data/vectors/orgProfiles_all.txt', 'orgProfile_w2v_skipgram_25',dim=25, loss='hs')
    #     print(len(model.words))  # list of words in dictionary
    #
    #     model = fasttext.skipgram('../data/vectors/orgProfiles_all.txt', 'orgProfile_w2v_skipgram_10_min3',dim=10, min_count=3, loss='hs')
    #     print(len(model.words))  # list of words in dictionary
    #
    #     model = fasttext.skipgram('../data/vectors/orgProfiles_all.txt', 'orgProfile_w2v_skipgram_25_min3',dim=25, min_count=3, loss='hs')
    #     print(len(model.words))  # list of words in dictionary
    #
    #     model = fasttext.skipgram('../data/vectors/org_origTweets.txt', 'orgProfile_w2v_skipgram_25',dim=25, loss='hs')
    #     print(len(model.words))  # list of words in dictionary
    #
    #     model = fasttext.skipgram('../data/vectors/org_origTweets.txt', 'orgProfile_w2v_skipgram_50',dim=50, loss='hs')
    #     print(len(model.words))  # list of words in dictionary

    #     model = fasttext.skipgram('../data/vectors/org_origTweets.txt', 'orgProfile_w2v_skipgram_100',dim=100, loss='hs')
    #     print(len(model.words))  # list of words in dictionary

    #     classifier = fasttext.supervised('data.txt', 'model', label_prefix='__label__')
    #     fasttext.supervised(input_file='data.txt', output='profile_w2v_skipgram_100_supervised', dim=100, word_ngrams=2, pretrained_vectors="../data/vectors/profile_w2v_skipgram_100")
    pass
