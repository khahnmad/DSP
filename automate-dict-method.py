# Imports
import glob
import All_Functions as af
import DictMethod as dm
import tfidfGenerator as tg
import time
import word2vec_dict_method as wv
import numpy as np
import pandas as pd
import collections
import ast

# Functions
def run_evaluate(location, round_no):
    time.sleep(5)  # TODO: Need to make this long enough that the new file is created
    new_file = 'dict-development\\' + location + '_round-' + str(round_no) + '.csv'
    try:
        test = af.import_csv(new_file)
        print('Sucessful after a 5 second wait ')
    except FileNotFoundError:
        print('Trying the while loop')
        all_dict_files = [x for x in glob.glob('dict-development' + "/*.csv")]
        while new_file not in all_dict_files:
            print('Waiting')
            time.sleep(5)
            all_dict_files = [x for x in glob.glob('dict-development' + "/*.csv")]
        else:
            dm.eval_dict_method(new_file, round_no)


def tf_idf_identification(tf_idf, file, location, round_no):
    # Identify high scores and add them to the dict
    high_scores = af.identify_high_scores(tf_idf, file)
    print(f'Here are the high scoring words for {location}:')
    print(high_scores)
    print('Which words should be added to the dictionary? Format: word score')
    input1 = input()
    print('Next:')
    input2 = input()
    print('Next: (enter "exit" if there is no additional word)')
    input3 = input()
    if input3 == 'exit' or len(input3.split()) <=1:
        all_dicts[location]['words'].append(input1.split()[0])
        all_dicts[location]['words'].append(input2.split()[0])
        all_dicts[location]['scores'].append(float(input1.split()[1]))
        all_dicts[location]['scores'].append(float(input2.split()[1]))
    else:
        all_dicts[location]['words'].append(input1.split()[0])
        all_dicts[location]['words'].append(input2.split()[0])
        all_dicts[location]['words'].append(input3.split()[0])
        all_dicts[location]['scores'].append(float(input1.split()[1]))
        all_dicts[location]['scores'].append(float(input2.split()[1]))
        all_dicts[location]['scores'].append(float(input3.split()[1]))

    # Apply the dictionary
    dm.apply_dict_method(round_no, file, all_dicts[location])

    # Evaluate the dictionary
    run_evaluate(location, round_no)
    # time.sleep(5) #
    # new_file = 'dict-development\\' + location + '_round-' + str(round_no) + '.csv'
    # try:
    #     test = af.import_csv(new_file)
    #     print('Sucessful after a 5 second wait ')
    # except FileNotFoundError:
    #     print('Trying the while loop')
    #     all_dict_files = [x for x in glob.glob('dict-development' + "/*.csv")]
    #     while new_file not in all_dict_files:
    #         print('Waiting')
    #         time.sleep(5)
    #         all_dict_files = [x for x in glob.glob('dict-development' + "/*.csv")]
    #     else:
    #         dm.eval_dict_method(new_file, round_no)

def run_round2(rd1_file, location):
    # Generate tf-idf only for those now classified as "about" the event
    content = af.import_csv(rd1_file)
    relevant = []
    for i in range(len(content)):
        if content[i][-2] == '1' and content[i][-1] == '1':  # true positives
            relevant.append(content[i])
        if content[i][-2] == '1' and content[i][-1] == 'None':  # dict positives
            relevant.append(content[i])
        if content[i][-2] == '0' and content[i][-1] == '1':  # false negatives
            relevant.append(content[i])
    tg.generate_tfidf(relevant, location,2)
    tf_idf_file = 'tf-idf-scores//' + location + '_2-tf-idf.csv'
    tf_idf_identification(tf_idf_file, rd1_file, location,2)

def run_round3(rd2_file, location):
    shooter_name = all_dicts[location]['words'][0]
    wv.get_similar_words(rd2_file, shooter_name)

    print('Which words should be added to the dictionary? Format: word score')
    input1 = input()
    print('Next:')
    input2 = input()
    print('Next: (enter "exit" if there is no additional word')
    input3 = input()
    if input3 == 'exit':
        all_dicts[location]['words'].append(input1.split()[0])
        all_dicts[location]['words'].append(input2.split()[0])
        all_dicts[location]['scores'].append(float(input1.split()[1]))
        all_dicts[location]['scores'].append(float(input2.split()[1]))
    else:
        all_dicts[location]['words'].append(input1.split()[0])
        all_dicts[location]['words'].append(input2.split()[0])
        all_dicts[location]['words'].append(input3.split()[0])
        all_dicts[location]['scores'].append(float(input1.split()[1]))
        all_dicts[location]['scores'].append(float(input2.split()[1]))
        all_dicts[location]['scores'].append(float(input3.split()[1]))

    # Apply the dictionary
    dm.apply_dict_method(3, rd2_file, all_dicts[location])

    # Evaluate the dictionary
    time.sleep(5)
    dm.eval_dict_method(rd2_file, 3)

def calc_pr(man_list, new_classif):
    positives, negatives, fps, fns, tps, tns = 0, 0, 0, 0, 0, 0
    evaluation = [['positives', 'negatives', 'fps', 'fns', 'tps', 'tns', 'precision', 'recall']]
    for i in range(len(new_classif)):
        if new_classif[i] == '1' and man_list[i] == '0':  # false positives
            fps += 1
        if new_classif[i] == '0' and man_list[i] == '1':  # false negatives
            fns += 1
        if new_classif[i] == '1' and man_list[i] == '1':  # true positives
            tps += 1
        if new_classif[i] == '0' and man_list[i] == '0':  # true negatives
            tns += 1
    precision = tps / (tps + fps)
    recall = tps / (tps + fns)
    return [precision, recall]



def finetune(location):
    pr = []
    dict_files = [x for x in glob.glob('dict-development' + "/*.csv") if location in x and '3' in x]
    round3 = af.import_csv(dict_files[0])
    man_class = ['None' for x in range(len(round3))]
    for i in range(len(round3)):
        if round3[i][15] != 'None':
            man_class[i] = round3[i][15]
        if round3[i][19] != 'None':
            man_class[i] = round3[i][19]
        if round3[i][23] != 'None':
            man_class[i] = round3[i][23]
    new_class = ['None' for x in range(len(round3))]
    numbers = np.arange(0.25,15,0.25)
    for number in numbers:
        for i in range(len(round3)):
            if len(round3[i][20]) > number:
                new_class[i] = '1'
            else:
                new_class[i] = '0'
        p_r = calc_pr(man_class, new_class)
        # pr.append([number, calc_pr(man_class, new_class)[0], calc_pr(man_class, new_class)[0]])
        pr.append([number, p_r[0],p_r[1]])
    df = pd.DataFrame(data=pr, columns=['number', 'precision','recall'])
    df['sum'] = df['precision']+ df['recall']
    column = df['sum']
    max_index = df['sum'].idxmax()
    best_threshold = df['number'][max_index]

    fp_keywords = []
    fn_text = []
    for i in range(len(round3)):
        if round3[i][-2] == '1' and round3[i][-1] == '0':  # false positives
            type_fix = ast.literal_eval(round3[i][-4]) # fix type for keywords
            for word in type_fix:
                fp_keywords.append(word)
        if round3[i][-2] == '0' and round3[i][-1] == '1':  # false negatives
            for word in round3[i][10]:
                fn_text.append(word)
    # most common words that spark a false positive?
    fp_counter = collections.Counter(fp_keywords)
    print('These are the most common keywords among files that trigger a false positive:')
    print(fp_counter.most_common(10))
    print('Choose a word to eliminate?')
    to_eliminate =[]
    x = input()
    to_eliminate.append(x)
    while x != 'exit':
        print("Next: (or exit to quit)")
        x = input()
        to_eliminate.append(x)

    for i in range(len(all_dicts[location]['words'])):
        if all_dicts[location]['words'][i] in to_eliminate:
            del all_dicts[location]['words'][i]
            del all_dicts[location]['scores'][i]

    fn_counter = collections.Counter(fn_text)
    print('These are the most common words in documents that trigger a false negative:')
    print(fn_counter.most_common(20))
    print('Choose a word to add to the dictionary? Format: word score')
    to_add = []
    y=input()
    to_add.append(y)
    while y != 'exit':
        print('Next: or exit to quit')
        y = input()
        if y!= 'exit':
            to_add.append(y)
    else:
        for elt in to_add:
            all_dicts[location]['words'].append(elt.split()[0])
            all_dicts[location]['scores'].append(float(elt.split()[1]))
    print('check')

    dm.apply_dict_method(4, dict_files[0], all_dicts[location], threshold=best_threshold)

    run_evaluate(location, 4)

# Variables

# Action
## Initialize dictionary with location and shooter name
all_files = [x for x in glob.glob('article-text' + "/*.csv") if 'cleaned' in x and '0' not in x]
keys = [af.get_event_name(file) for file in all_files]
all_dicts = dict.fromkeys(keys)
for key in keys:
    all_dicts[key] = {'words': [], 'scores': []}


### initialize location & shooter name
sample_info = af.import_csv('generate-sample/intial-sample-w-info.csv')
for key in keys:
    for i in range(1,len(sample_info)):
        if len(sample_info[i][3].split()) >1:
            location_converted = sample_info[i][3].split()[0]+'_'+sample_info[i][3].split()[1]
        else:
            location_converted = sample_info[i][3]
        if location_converted == key:
            if len(sample_info[i][3].split()) >1:
                cleaned_location = [x.lower() for x in sample_info[i][3].split()]
                cleaned_name = sample_info[i][4].split()[-1].lower()
                all_dicts[key]['words'].append(cleaned_name)
                all_dicts[key]['words'].append(cleaned_location[0])
                all_dicts[key]['words'].append(cleaned_location[1])
                all_dicts[key]['scores'].append(1.25)
                all_dicts[key]['scores'].append(.75)
                all_dicts[key]['scores'].append(.75)

            else:
                cleaned_location = sample_info[i][3].lower()
                cleaned_name = sample_info[i][4].split()[-1].lower()
                all_dicts[key]['words'].append(cleaned_name)
                all_dicts[key]['words'].append(cleaned_location)
                all_dicts[key]['scores'].append(1.25)
                all_dicts[key]['scores'].append(1.25)


# two rounds of tf-idf and 1 round of word2vec
tf_idf_files = [x for x in glob.glob('tf-idf-scores/round-1' + "/*.csv")]
# for file in all_files:
#     location = af.get_event_name(file)
#     for tf_idf in tf_idf_files:
#         if location in tf_idf:
#             tf_idf_identification(tf_idf, file, location,1)
#
#             rd1_file = 'dict-development/'+location+'_round-1.csv'
#             run_round2(rd1_file, location)
#
#             rd2_file = 'dict-development/' + location + '_round-2.csv'
#             run_round3(rd2_file, location)
#

print('CHECKPOINT')
finetune('Aurora')
