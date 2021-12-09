# Goal: find gendered language across categories

# Imports
import All_Functions as af
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

gendered_json = af.import_json('gendered_words.json')
"""
About this file: what are the potential biases? How was it created? 
                There are 406 female words and 595 male words, 6923 words total 
                Does it include pronouns? - Yes 
"""
male_words, female_words = ['he','him','his'],['she','her','hers']
for word in gendered_json:
    if word['gender'] ==  'm' and "_" not in word['word'] and word['word'] not in male_words:
        male_words.append(word['word'])
    if word['gender'] == 'f' and "_" not in word['word'] and word['word'] not in female_words:
        female_words.append(word['word'])

# count the number of times gendered words appear in each of the three categories
def count_gendered_words(gendered_words, text_category):
    total = 0
    all_words = 0
    for article in text_category[1:]: # append the number of gendered words to the end of each article
        count = 0
        counter = Counter(article[10])
        for word in gendered_words:
            count += counter[word]
        article.append(count)
        all_words += len(article[10])
        total+= count
    return total/ all_words

af.fix_field_errors()

stranger = af.import_csv('Categorized_Classified/stranger_articles.csv')
coworker = af.import_csv('Categorized_Classified/coworker_articles.csv')
family = af.import_csv('Categorized_Classified/family_articles.csv')

male_stranger = count_gendered_words(male_words, stranger)
female_stranger = count_gendered_words(female_words, stranger)
male_coworker = count_gendered_words(male_words, coworker)
female_coworker = count_gendered_words(female_words, coworker)
male_family = count_gendered_words(male_words, family)
female_family = count_gendered_words(female_words, family)


# data = [[male_stranger, male_coworker, male_family],[female_stranger, female_coworker, female_family ]]
# fig = plt.figure()
#
# barWidth = 0.25
# br1 = np.arange(len(data[0]))
# br2 = [x + barWidth for x in br1]
#
#
# # Make the plot
# plt.bar(br1, data[0], width=barWidth,
#         edgecolor='grey', label='Male Words')
# plt.bar(br2, data[1], width=barWidth,
#         edgecolor='grey', label='Female Words')
# # Adding Xticks
# plt.xlabel('Types of Shooting Events', fontweight='bold', fontsize=15)
# plt.ylabel('Quantity of Gendered Language', fontweight='bold', fontsize=15)
# plt.xticks([r + barWidth for r in range(len(data[0]))],
#            ['Stranger', 'Coworker','Family'])
#
# plt.legend()
# plt.show()

stranger[0].append('Male')
stranger[0].append('Female')
coworker[0].append('Male')
coworker[0].append('Female')
family[0].append('Male')
family[0].append('Female')

stranger_df = pd.DataFrame(columns=stranger[0], data=stranger[1:])
coworker_df = pd.DataFrame(columns=coworker[0], data=coworker[1:])
family_df = pd.DataFrame(columns=family[0],data=family[1:])

stranger_df['Difference'] = stranger_df['Male']-stranger_df['Female']
coworker_df['Difference'] = coworker_df['Male']-coworker_df['Female']
family_df['Difference'] = family_df['Male']-family_df['Female']

print(stranger_df['Difference'].mean())
print(coworker_df['Difference'].mean())
print(family_df['Difference'].mean())

high_difference_stranger = stranger_df[stranger_df['Difference'] > 4.3]
high_difference_coworker = coworker_df[coworker_df['Difference'] > 4.8]
high_difference_family = family_df[family_df['Difference'] > 7]

female_high_difference_stranger = stranger_df[stranger_df['Difference'] <0]
female_high_difference_coworker = coworker_df[coworker_df['Difference'] <0]
female_high_difference_family = family_df[family_df['Difference'] <0]

# print(stranger_df.sort_values(by=['Male'], ascending=False).head())
# print(stranger_df.sort_values(by=['Female'], ascending=False).head())
# print(coworker_df.sort_values(by=['Male'], ascending=False).head())
# print(coworker_df.sort_values(by=['Female'], ascending=False).head())
# print(family_df.sort_values(by=['Male'], ascending=False).head())
# print(family_df.sort_values(by=['Female'], ascending=False).head())
male_subset = stranger_df[stranger_df['Male'] >= 100]
female_subset = stranger_df[stranger_df['Female'] >= 70]

print(male_subset['url'])
print(female_subset['url'])

print('debug')
