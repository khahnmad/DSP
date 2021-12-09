import All_Functions as af
import os
import glob
#packages for part1
from gensim import utils
import gensim.models
import json

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

#part 2
import re
from sklearn import cluster
from scipy.spatial.distance import cosine
import pandas as pd

"""
Create a word embedding space for the full corpus
In this space, check to see what words are closest to the female pronouns/words/victim names, and the same for the male
Subtract the distance between some words to see if some are closer to female, some closer to male
"""
# Import things to search for
female_words = ['she','her','hers','woman','girl','daughter','mother','wife','niece','aunt','grandmother','granddaughter','sister-in-law','ex-wife','girlfriend','female','mom']
male_words= ['he','his','him','man','boy','son','father','husband','nephew','uncle','grandfather','grandson','ex-husband','brother-in-law','boyfriend','male','dad']

victim_syn=['victim','victims','survivors','victims.','deceased','injured']

os.chdir('C:\\Users\\khahn\\Documents\\DSP\\DSP')
victims = af.import_csv('generate-sample/Sampled_Victims.csv')
female_victim_names = [victims[n][1].split()[1].lower() for n in range(len(victims))]

explanations = ['mental','terrorism','anti-semitism','domestic']
# Create word embeddings
# create full text
# af.fix_field_errors()
# all_files = [x for x in glob.glob('full_vector_space' + "/*.csv") if 'cleaned' in x]
# full_text = []
# for file in all_files:
#     imported = af.import_csv(file)
#     for article in imported[1:]:
#         full_text.append(article[10])

# model = gensim.models.Word2Vec(sentences=full_text)
# model.save('complete_word2vec')
model = gensim.models.Word2Vec.load("complete_word2vec")


def find_related(words_list):
    related_words=[]
    existing_words = []
    for word in words_list:
        try:
            related = model.wv.most_similar(word, topn=10)
            # related_words.append(related)
            for pair in related:
                if pair[0] not in existing_words:
                    related_words.append(pair)
        except KeyError:
            print(f'{word} not in vocab')

    return related_words

related_female = find_related(female_words)
related_male= find_related(male_words)
related_victims =find_related(victim_syn)
specific_victims = find_related(female_victim_names)
print('checking')

#
# print(model.wv.most_similar(positive=['sister', 'he'],
#                        negative=['she']))


print(model.wv.most_similar('victim'))
print(model.wv.most_similar('hero'))
print(model.wv.most_similar('helpless'))
print(model.wv.most_similar('sacrificed'))
simple_gender = ['woman','girl','man','boy']
full_gender = female_words+male_words
interesting_words = ['victim','hero','helpless','savior','survivor','attacker','revenge','retribution','strength','vulnerable','targeted','bravery','forgiveness','abuse','violent']
interest_vectors = []
for word in interesting_words:
    interest_vectors.append(model.wv[word])

gendered_similarities = []
for word in interesting_words:
    closest = 0
    for gender in full_gender:
        new_closest = model.wv.similarity(gender, word)
        if new_closest > closest:
            closest = new_closest
            words = [gender, word]
    gendered_similarities.append([words[1],words[0],closest])


df = pd.DataFrame(gendered_similarities)




# pca = PCA(n_components=2)
# reduced = pca.fit_transform(interest_vectors)
#
# x = [arr[0] for arr in reduced]
# y = [arr[1] for arr in reduced]
#
# for i in range(len(x)):
#     plt.text(x=x[i],y=y[i],s=interesting_words[i])
#
# plt.scatter(x,y)
# plt.show()



print('debug')