"""


"""
# Imports
import All_Functions as af
import glob
import re
import nltk
from nltk.corpus import stopwords
import string
import pandas as pd
import os



# Setup
af.fix_field_errors()


# Functions

def clean_all_csv_files(all_files):
    # Variables
    extra_stopwords = ['``', "'s", '•', "n't", '.', '’', '”', '—', '‘', '“', '©', '___', "''", '==\\']
    for file in all_files:
        print(f'Working on {af.get_event_name(file)}')
        cleaned_content = []
        if '0' not in file: # only look at complete files
            content = af.import_csv(file)
            content[0].append('location') # update the column names to include 'location'
            cleaned_content.append(content[0])
            regex = r"[A-Z].*(?=_)"  # regex for getting the location name of each event
            match = re.findall(regex, file)
            for row in content[1:]: # only look at the content rows, not the column names
                if len(row) == 11:
                    row.append(match[0])  # append the location name to each row

                    tokenized = nltk.word_tokenize(row[10])  # tokenize # is this the right format?

                    lowercase = af.remove_capitalization(tokenized)  # remove capitalization



                    # remove punctuation
                    punct = [str(x) for x in string.punctuation]
                    for item in extra_stopwords:
                        punct.append(item)
                    no_punct = [item for item in lowercase if item not in punct]

                    # remove empty strings
                    while '' in no_punct:
                        no_punct.remove('')

                    row[10] = no_punct
                    cleaned_content.append(row)
            if len(cleaned_content)>1:
                print('   has content')
            csv_file_name = 'full_vector_space\\' + match[0] + '_cleaned-text.csv'

            af.export_nested_list(csv_file_name, cleaned_content)

def look_for_bad_urls(all_files):
    for file in all_files:
        print(f'Working on {af.get_event_name(file)}..')
        relevant_content, bad_urls = [], []
        content = af.import_csv(file)
        relevant_content.append(content[0])
        for row in content[1:]: # don't look at the heading row
            # should the "50" threshold be higher?
            if len(row[10]) >= 50: # if there are more than 50 words, it's probably a real articles
                if 'npr' in row[3]:
                    bad_urls.append(['Resistant to Bots Error', row[3]])
                else:
                    relevant_content.append(row)
            elif len(row[10]) <= 1:
                bad_urls.append(['Unscrapable content error',row[3]])
            elif len(row[10]) < 50 and len(row[10]) > 1: # check that this is the right index
                # Does it contain some of these keywords that suggest it wasn't scraped?
                error_words = ['sorry page','browser supports javascript','address entered correct',
                               'return previous page','subscriber subscribe today',
                               'access page denied','url found server','inc. rights reserved',
                               'old link typed','please update browser','use cookies', 'timeout details',
                               'terms service privacy policy','cache server','subscribe monthly 1']

                count = 0
                joined = " ".join(row[10])
                if '404' in joined:
                    bad_urls.append(['404 Not found', row[3]])
                if '451' in joined:
                    bad_urls.append(['Legal Reasons (GDPR) Error', row[3]])
                if 'please enable cookies' in joined:
                    bad_urls.append(['Resistant to Bots Error', row[3]])
                if 'server error' in joined:
                    bad_urls.append(['Server Error', row[3]])
                for phrase in error_words:
                    if phrase in joined:
                        existing_bad = [x[1] for x in bad_urls]
                        if row[3] not in existing_bad:
                            bad_urls.append(['Unscrapable content - Unknown reason', row[3]])
                            count = 1
                # if count == 0:
                    # Otherwise do mannually check
                    # print('Relevant content? y or n')
                    # print(f'    {row[3]}')
                    # print(f'    {row[10]}')
                    # value = input()
                    # if value == 'y':
                    #     relevant_content.append(row)
                    # elif value == 'n':
                    #     # add to bad_urls
                    #     bad_urls.append(['Unscrapable content error',row[3]]) # is that the right index for the url?
        af.export_nested_list(file, relevant_content) # export good content
        #
        # # Add new bad urls to the appropriate existing file
        # regex = r"[A-Z].*(?=_)"  # regex for getting the location name of each event
        # match = re.findall(regex, file)
        # bad_urls_csvfile = 'bad-urls//'+match[0]+'_bad-urls.csv'
        # for row in bad_urls:
        #     af.append_to_csv(bad_urls_csvfile, row)




# Get files without the stopwords being removed
os.chdir('C:\\Users\\khahn\\Documents\\DSP\\DSP')
# all_files = [x for x in glob.glob('article-text' + "/*.csv") if 'cleaned' not in x and '0' not in x]  # Get all files in the given folder
# # RUN the function
# clean_all_csv_files(all_files)

# Import files
cleaned_files = [x for x in glob.glob('full_vector_space' + "/*.csv") if 'cleaned' in x]  # Get all files in the given folder
# RUN the next function
look_for_bad_urls(cleaned_files)