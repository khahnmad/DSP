# Imports
import csv
import re
import sys
import ast
from csv import writer
import collections

# Imports & Setup
def import_csv(csv_file):  # parses data into a nested list
    nested_list = []  # initialize list
    with open(csv_file, newline='', encoding='utf-8') as csvfile:  # open csv file
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            nested_list.append(row)  # add each row of the csv file to a list

    # Introduce case for the list of text that is commonly at the 10th index and imported improperly
    # should i do a try and except insted of this messy if statement business?
    # print(csv_file)
    if len(nested_list)>=2:
        if len(nested_list[1]) >= 10:
            if len(nested_list[1])>=12 and type(nested_list[1][10])==str: # double check that this index/ syntax works
                for i in range(1,len(nested_list)):
                    type_fix = ast.literal_eval(nested_list[i][10])
                    nested_list[i][10] = type_fix
        return nested_list  # return nested list


# Exports and shutting down
def export_nested_list(csv_name, nested_list):
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in nested_list:
            writer.writerow(row)

def export_list(csv_name, list_):
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(list_)

def export_dictionary(csv_name, dictionary):
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for key, value in dictionary.items():
            writer.writerow([key, value])

def fix_field_errors():
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

def import_text_data(all_files):
    # Import all the text data
    # Resolves the huge fields error that you get from importing some of the csv files
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    # Get the text for each of the articles
    all_text = []
    for file in all_files:

        as_list = import_csv(file)  # import the file as a nested list

        # This regex works for the v2 files only
        location = re.findall(r"(?<=2\-)(.*?)(?=\_)",
                              file)  # use this regex to extract the location from the name of the file
        # For example: newspaper-text\v2-Bogue_Text-first-month.csv -> gets between 2- and _
        # This regex works for the unclean files
        if len(location) < 1:
            location = re.findall(r"(?<=clean)(.*?)(?=\_)", file)
            # gets everything between clean and _

        as_list[0].append('Location')  # add a location category to the beginning of each file
        for article in as_list[1:]:
            article.append(location[0])  # tag the location to each article

        # if the location of the last append file matches the current appended file
        if len(all_text) > 0 and all_text[-1][1][-1] == location[0]:
            for item in as_list[1:]:
                all_text[-1].append(item)  # then add the current file to the list for the last file
            # this part combines the three files for each of the shootings into one list
        else:
            all_text.append(as_list)
        """ OUTPUT: list all_text contains a list for each of the *shooting* in all_files
            So, 10 lists, one for each of the ten shootings 
        """
    return all_text


def append_to_csv(csv_name,row):
    with open(csv_name, 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(row)
        f_object.close()


# Cleaning
def remove_capitalization(cap_list):
    return [cap_list[i].lower() for i in range(len(cap_list))]

def get_event_name(file):
    regex = r"[A-Z].*(?=_)"  # regex for getting the location name of each event
    match = re.findall(regex, file)
    if len(match) == 0:
        alternative = r"[A-Z].*(?=\.)"
        match = re.findall(alternative, file)
    return match[0]

# tf-idf
def create_vocab(content): # for unclean content. could make an option for clean content
    all_text, vocab = [],[]
    for i in range(1,len(content)):
        for word in content[i][10]:
            all_text.append(word)
    for word in all_text:
        if word not in vocab:
            vocab.append(word)
    return vocab


def identify_high_scores(tf_idf_file, cleaned_text_file):
    tfidf = import_csv(tf_idf_file)
    text = import_csv(cleaned_text_file)
    vocab = create_vocab(text)
    high_scores = []
    for i in range(len(tfidf)):
        for j in range(len(tfidf[i])):
            if float(tfidf[i][j]) > 5.5 and vocab[j] not in high_scores:
                high_scores.append(vocab[j])
    if len(high_scores) <=15:
        for i in range(len(tfidf)):
            for j in range(len(tfidf[i])):
                if float(tfidf[i][j]) > 4 and vocab[j] not in high_scores:
                    high_scores.append(vocab[j])
    return high_scores

