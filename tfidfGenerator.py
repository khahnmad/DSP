"""
TODO
- how do i cut donw on time complexity? should i switch to numpy?
- export as csv?
- why do we have repeating word in the vocab???
"""
import glob
import All_Functions as af
import collections
import math


def create_vocab(content): # for unclean content. could make an option for clean content
    all_text, vocab = [],[]
    for i in range(1,len(content)):
        for word in content[i][10]:
            all_text.append(word)
    for word in all_text:
        if word not in vocab:
            vocab.append(word)
    return vocab

def create_tf_matrix(vocab, content):
    matrix = [[] for x in content] # check that this is the right dimension

    # count number of times each term appears in each document
    for i in range(len(content)):
        for word in vocab:
            counter = collections.Counter(content[i][10])
            t_in_d = counter[word]
            matrix[i].append(t_in_d)
    return matrix


def calculate_idf(vocab, content):
    df_matrix = []
    for word in vocab:
        count = 0
        for i in range(len(content)):
            if word in content[i][10]:
                count +=1
        df_matrix.append(count)
    # df indicates the number of documents in the collection that feature each of the words in the vocab
    # so it is of the same dimensions as the vocab
    num_docs = len(content)
    idfs = []
    for df in df_matrix:
        n_df = num_docs/ df
        idf = math.log(n_df, 10)
        idfs.append(idf)
    return idfs

def calculate_tfidf(tf_matrix, idf_matrix):
    matrix =[]
    for i in range(len(tf_matrix)):
        doc_weight = []
        for term in tf_matrix[i]:
            if term == 0: # What is the justification for this?
                doc_weight.append(idf_matrix[i])
            else:
                weight = (1 + math.log(term, 10))*idf_matrix[i]
                doc_weight.append(weight)
        matrix.append(doc_weight)
    return matrix

# Summary function
def generate_tfidf(content, location, round_number=0):
    # Generate tf-idf
    vocab = create_vocab(content)
    tf_matrix = create_tf_matrix(vocab, content[1:])
    idf_matrix = calculate_idf(vocab, content[1:])
    tf_idf_matrix = calculate_tfidf(tf_matrix, idf_matrix)

    if round_number != 0:
        csv_name = 'tf-idf-scores//' + location + '_'+str(round_number)+'-tf-idf.csv'
    else:
        csv_name = 'tf-idf-scores//' + location + '_tf-idf.csv'
    af.export_nested_list(csv_name, tf_idf_matrix)



def identify_high_scores(tf_idf_file, cleaned_text_file):
    tfidf = af.import_csv(tf_idf_file)
    text = af.import_csv(cleaned_text_file)
    vocab = create_vocab(text)
    high_scores = []
    for i in range(len(tfidf)):
        for j in range(len(tfidf[i])):
            if float(tfidf[i][j]) > 3.5:
                high_scores.append(vocab[j])
    return high_scores


# Setup
af.fix_field_errors()

# ROUND 1
# Genderate tf-idf
# all_files = [x for x in glob.glob('article-text' + "/*.csv") if 'cleaned' in x and '0' not in x]  # Get all files in the given folder
# for file in all_files:
#     print(f"Working on {af.get_event_name(file)}...")
#     generate_tfidf(file)

# Inspect tf-idf
# all_files = [x for x in glob.glob('tf-idf-scores\\round-1' + "/*.csv")]  # Get all files in the given folder
# all_high_scores = []
# for file in all_files:
#     all_high_scores.append(identify_high_scores(file))
# print('checkpoint')

# ROUND 2:
# Generate tf-idf only for those now classified as "about" the event
# file = 'Aurora_round_1.csv'
# content = af.import_csv(file)
# relevant = []
# for i in range(len(content)):
#     if content[i][-2] == '1' and content[i][-1] == '1':  # true positives
#         relevant.append(content[i])
#     if content[i][-2] == '1' and content[i][-1] == 'None':  # dict positives
#         relevant.append(content[i])
#     if content[i][-2] == '0' and content[i][-1] == '1':  # false negatives
#         relevant.append(content[i])
# # generate_tfidf(relevant, 1)
#
# high_scores = identify_high_scores('tf-idf-scores/Aurora-1_tf-idf.csv','Aurora_round_1.csv')

# Round 3:
# Generate tf-idf only for those now classified as "about" the event
# file = 'Aurora_round_2.csv'
# content = af.import_csv(file)
# relevant = []
# for i in range(len(content)):
#     if content[i][-2] == '1' and content[i][-1] == '1':  # true positives
#         relevant.append(content[i])
#     if content[i][-2] == '1' and content[i][-1] == 'None':  # dict positives
#         relevant.append(content[i])
#     if content[i][-2] == '0' and content[i][-1] == '1':  # false negatives
#         relevant.append(content[i])
# # add manually classified from last round(s)
# earlier_file = 'Aurora_round_1.csv'
# earlier = af.import_csv(earlier_file)
# old = []
# for i in range(len(earlier)):
#     if earlier[i][-2] == '1' and earlier[i][-1] == '1':  # true positives
#         old.append(earlier[i])
#     if earlier[i][-2] == '1' and earlier[i][-1] == 'None':  # dict positives
#         old.append(earlier[i])
#     if earlier[i][-2] == '0' and earlier[i][-1] == '1':  # false negatives
#         old.append(earlier[i])
# print('c')
# old_ids = [old[x][0] for x in range(len(old))]
# new_ids = [relevant[x][0] for x in range(len(relevant))]
# for i in range(len(old_ids)):
#     if old_ids[i] not in new_ids:
#         relevant.append(old[i])
# generate_tfidf(relevant, 1)

# high_scores = identify_high_scores('tf-idf-scores/Aurora-2_tf-idf.csv','Aurora_round_2.csv')
# print('c')