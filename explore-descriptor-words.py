# What are the most common descriptor words?
# What descriptor words are unique?
# Where do the words lie in the vector space?

import All_Functions as af
import ast

def fix_import_error(nested_list):
    for i in range(1,len(nested_list)):
        type_fix = ast.literal_eval(nested_list[i][1])
        nested_list[i][1] = type_fix
    return nested_list

male =fix_import_error( af.import_csv('Male_descriptors.csv'))
female = fix_import_error(af.import_csv('Female_descriptors.csv'))

all_male=[]
for event in male[1:]:
    for word in event[1]:
        all_male.append(word)
all_female=[]
for event in female[1:]:
    for word in event[1]:
        all_female.append(word)
male_common = af.print_most_common(all_male)
female_common = af.print_most_common(all_female)
print('What are the most common words?')

female_unique, male_unique = [],[]
for word in all_female:
    if word not in all_male:
        female_unique.append(word)
for word in all_male:
    if word not in all_female:
        male_unique.append(word)
unqiue_female_common = af.print_most_common(female_unique)
unqiue_male_common = af.print_most_common(male_unique)
print('What are the unique male and female words?')

