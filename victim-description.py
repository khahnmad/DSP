import All_Functions as af
from All_Functions import *
import glob as glob
from ast import literal_eval
import nltk
import collections
from collections import Counter
from gensim.models import Word2Vec
import nltk
# nltk.download('brown')
# nltk.download('treebank')
from nltk.corpus import brown
from nltk.tag import UnigramTagger
from nltk.tag import UnigramTagger, BigramTagger
from nltk.tag.brill_trainer import BrillTaggerTrainer
from nltk.tag.brill import brill24
from nltk.tag import brill, brill_trainer
import time

# Functions
def print_most_common(text):
    counter = Counter(text)
    most = counter.most_common()
    print(most[:20])
    return most[:20]

def create_postagger():
    # POS tagger training
    a = time.time()
    n_cutoff = 20000
    brown_sents_train = brown.tagged_sents()[0:n_cutoff] # training corpus
    b = time.time()

    uni_tagger = UnigramTagger(brown_sents_train)
    # bi_tagger_backoff = BigramTagger(brown_sents_train, backoff=uni_tagger)
    # bi_tagger = BigramTagger(brown_sents_train)
    c = time.time()

    #with the backoff
    templates = nltk.tag.brill.brill24()
    # brill_tagger = brill_trainer.BrillTaggerTrainer(bi_tagger, templates)
    # trainer = brill_tagger.train(brown_sents_train)
    brill_tagger_backoff = brill_trainer.BrillTaggerTrainer(uni_tagger, templates)

    trainer_backoff = brill_tagger_backoff.train(brown_sents_train)
    d = time.time()


    d_a = d-a
    d_c = d-c
    c_b = c-b

    return trainer_backoff
# Imports & Variables
victims = af.import_csv('generate-sample/Sampled_Victims.csv')


# get all classified text
af.fix_field_errors()
classified = [x for x in glob.glob('dict-development' + "/*.csv") if 'round-3' in x] # gather all the classified files
classified_text = []
for file_name in classified:
    file = af.import_csv(file_name)
    for i in range(len(file)):
        if file[i][-2] == '1': # check that this type is right
            classified_text.append(file[i])
# Victim Words: DONT NEED TO RE-RUN
# model = Word2Vec(sentences=classified_text, window=5, min_count=1, workers=4)
# related = model.wv.most_similar('victim', topn=25)
# print(f"Here are the most similar words to 'victim':")
# print(related)
# related = model.wv.most_similar('victims', topn=25)
# print(f"Here are the most similar words to 'victim':")
# print(related)

victim_syn=['victim','victims','survivors','victims.','deceased']



trainer_backoff = create_postagger()

# Find all the sentences that use one of the "victim words"
victim_sentences = []
for i in range(len(classified_text)):
    for word in classified_text[i][10]: # this is being imported correctly, right?
        if word in victim_syn and classified_text[i] not in victim_sentences:
            victim_sentences.append(classified_text[i])

# Collect the POS tags for all of the sentences
for i in range(len(victim_sentences)):
    tags = trainer_backoff.tag(victim_sentences[i][10])
    victim_sentences[i].append(tags)

male_gender,female_gender=[],[]
gendered_json = af.import_json('gendered_words.json')
male_gender, female_gender = ['he','him','his'],['she','her','hers']
for word in gendered_json:
    if word['gender'] ==  'm' and "_" not in word['word'] and word['word'] not in male_gender:
        male_gender.append(word['word'])
    if word['gender'] == 'f' and "_" not in word['word'] and word['word'] not in female_gender:
        female_gender.append(word['word'])
#
adjs = ['JJ','JJS','JJR','RB','RBR','RBS']
shootings = []
male_descriptions, female_descriptions = [[] for x in range(10)],[[] for x in range(10)]
victim_adjs = [[] for x in range(10)] # range should be equal to the number of shootings there are +1
for i in range(len(victim_sentences)):
    # First, get the location & index of the location in "shootings"
    location = victim_sentences[i][11]
    if location not in shootings: # create list of all the shootings in the sample iteratively
        shootings.append(location)
    for j in range(len(shootings)):
        if location == shootings[j]:
            index = j
    # then get all the adjectives from the sentences
    for ii in range(len(victim_sentences[i][-1])): # iterate through the tags
        # there's got to be a better way to do this code
        if ii > 0 and victim_sentences[i][-1][ii][0] in male_gender: # indices meanings: row, tags, word, word-tag
            if victim_sentences[i][-1][ii - 1][1] in adjs:
                male_descriptions[index].append(victim_sentences[i][-1][ii - 1][0]) # get the adjective before the victim word
            if ii >1:
                if victim_sentences[i][-1][ii - 2][1] in adjs:
                    male_descriptions[index].append(victim_sentences[i][-1][ii - 2][0]) # get the adjective two places before the word
                    male_descriptions[index].append(victim_sentences[i][-1][ii - 1][0]) # and the word two places before the word
            try:
                if ii < len(victim_sentences[i][-1]):
                    if victim_sentences[i][-1][ii + 1][1] in adjs:
                        male_descriptions[index].append(victim_sentences[i][-1][ii + 1][0]) # get the adj after the victim word
            except IndexError:
                pass
        if ii > 0 and victim_sentences[i][-1][ii][0] in female_gender: # indices meanings: row, tags, word, word-tag
            if victim_sentences[i][-1][ii - 1][1] in adjs:
                female_descriptions[index].append(victim_sentences[i][-1][ii - 1][0]) # get the adjective before the victim word
            if ii >1:
                if victim_sentences[i][-1][ii - 2][1] in adjs:
                    female_descriptions[index].append(victim_sentences[i][-1][ii - 2][0]) # get the adjective two places before the word
                    female_descriptions[index].append(victim_sentences[i][-1][ii - 1][0]) # and the word two places before the word
            try:
                if ii < len(victim_sentences[i][-1]):
                    if victim_sentences[i][-1][ii + 1][1] in adjs:
                        female_descriptions[index].append(victim_sentences[i][-1][ii + 1][0]) # get the adj after the victim word
            except IndexError:
                pass


# print('Number of words that describe the victims in each shooting:')
# all_victims = [['location','number of descriptor words','most common descriptions']]
# # for k in range(len(victim_adjs)):
# #     print(shootings[k], len(victim_adjs[k]))
#
#
# print('Most common words to describe the victims:')
#
# for m in range(len(victim_adjs)):
#     print(shootings[m])
#     common = print_most_common(victim_adjs[m])
#     all_victims.append([shootings[m],len(victim_adjs[m]), common])
# af.export_nested_list('All_victim_descriptors.csv',all_victims)
print('Most common words to describe the men:')
exp_male_descriptions, exp_female_descriptions = [['location','male_descriptor_words']],[['location','female descriptor words']]
for m in range(len(male_descriptions)):
    # print(shootings[m])
    # common = print_most_common(male_descriptions[m])
    exp_male_descriptions.append([shootings[m],male_descriptions[m]])
af.export_nested_list('Male_descriptors.csv',exp_male_descriptions)
for m in range(len(female_descriptions)):
    # print(shootings[m])
    # common = print_most_common(female_descriptions[m])
    exp_female_descriptions.append([shootings[m],female_descriptions[m]])
af.export_nested_list('Female_descriptors.csv',exp_female_descriptions)
# specific_victims = []
# for n in range(len(victims)):
#     location = victims[n][0]
#     name = victims[n][1].split()[1].lower()
#     specific_adjectives = []
#     for p in range(len(classified_text)):
#         if classified_text[p][11] == location:
#             if name in classified_text[p][10]:
#                 tagged_text = trainer_backoff.tag(classified_text[p][10])
#
#                 for q in range(len(tagged_text)):
#                     if q > 0 and tagged_text[q][0] == name:  # indices meanings: row, tags, word, word-tag
#                         if tagged_text[q - 1][1] in adjs:
#                             specific_adjectives.append(tagged_text[q - 1][0])
#                         if q > 1:
#                             if tagged_text[q - 2][1] in adjs:
#                                 specific_adjectives.append(tagged_text[q - 2][0])
#                                 specific_adjectives.append(tagged_text[q - 1][0])
#     victims[n].append(specific_adjectives)
# af.export_nested_list('Specific_victim_descriptors.csv', victims)

print('check')