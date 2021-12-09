import All_Functions as af
import tfidfGenerator as tf
import nltk
import string
import collections
import math

def preprocessing(tweet):
    cleaned = []
    punct = string.punctuation
    lowercase = tweet.lower()
    tokenized = nltk.word_tokenize(lowercase)
    for word in tokenized:
        if 'mention' not in word and 'rt' != word and word.startswith('#') == False and word not in punct:
            word = word.replace("\\", '')
            word = word.replace("\n", '')
            word = word.replace('\'\'', '')
            word = word.replace('``', '')
            word = word.replace('...', '')
            if word != "":
                cleaned.append(word)
    return cleaned

def create_vocab(content): # for unclean content. could make an option for clean content
    # input: content: list of lists in which the sublists are tokenized and preprocessed to whatever degree wanted
    # output: a list of every unique word in the document
    all_text, vocab = [],[]
    for i in range(len(content)):
        for word in content[i]:
            all_text.append(word)
    for word in all_text:
        if word not in vocab:
            vocab.append(word)
    return vocab


def create_tf_matrix(vocab, content):
    #input: vocab; content: list of lists where sublists are the "documents"
    # output: matrix: same number of lists as the content, each sublist has the dimenions of the vocab
    matrix = [[] for x in content] # check that this is the right dimension

    # count number of times each term appears in each document
    for i in range(len(content)):
        for word in vocab:
            counter = collections.Counter(content[i])
            t_in_d = counter[word] # number of times the word appears in the document
            matrix[i].append(t_in_d)
    return matrix


def calculate_idf(vocab, content):
    #input: vocab, content
    # output: idfs with the same dimensions as the vocab
    df_matrix = []
    for word in vocab:
        count = 0
        for i in range(len(content)):
            if word in content[i]:
                count +=1
        df_matrix.append(count)
    # df indicates the number of documents in the collection that feature each of the words in the vocab
    # so it is of the same dimensions as the vocab, a list with length as the number of unique words
    num_docs = len(content)
    idfs = []
    for df in df_matrix:
        n_df = num_docs/ df
        idf = math.log(n_df, 10)
        idfs.append(idf)
    return idfs

annotations = af.import_csv('sexism_annotations.csv')
sexist_tweets_db = af.import_csv('sexism_data.csv')
sexist_tweets_db = sexist_tweets_db[1:] # get rid of the heading row
sexist_annotations = [x for x in annotations[1:] if x[0] != 3] # gets everything labeled as sexist; includes duplicates
ids = []
for x in sexist_annotations: # remove duplicates
    if int(x[3]) not in ids:
        ids.append(int(x[3]))
# so if one worker has labled the tweet as sexist, we count it
# this could be more sophisticated
sexist_tweets = []
to_remove = ['\\','\n']
for i in range(len(ids)):
    identified = sexist_tweets_db[ids[i]]
    cleaned_tweet = preprocessing(identified[2])
    sexist_tweets.append(cleaned_tweet)

