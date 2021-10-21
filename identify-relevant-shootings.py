# Imports
import All_Functions as af
import re
import random

victims_db = af.import_csv('victim-db.csv')  # import victims database

# identify victims that are female and since 2005
relevant_shootings = []
for i in range(len(victims_db)):
    if victims_db[i][6] == '1': # if a female victim is identified
        if len(re.findall(r'\d$', victims_db[i][3])) > 0:  # checks if date data exists for this row
            if int(victims_db[i][3][-4:]) >= 2005:  # checks if the shooting is from 2005 or later
                relevant_shootings.append(victims_db[i])

# Export list
sampled_shootings = af.export_nested_list('relevant-shootings.csv', relevant_shootings)

# Import newly created list
relevant_events = af.import_csv('relevant-shootings.csv')

# How many unique shootings are in this sample?
unique_events =[]
for i in range(len(relevant_events)):
    if relevant_events[i][1] not in unique_events:
        relevant_events.append(relevant_events[i][1])
print(f'There are {len(relevant_events)} mass shootings with female victims since 2005 in the database')
#                   ^650

# NOW: Create a smaller random sample
perp_names = []
for i in range(len(relevant_events)):
    perp_name = relevant_events[i][2] + ' ' + relevant_events[i][1]
    if perp_name not in perp_names:
        perp_names.append(relevant_events[i][2] + ' ' + relevant_events[i][1])
sample = random.sample(perp_names, int(len(perp_names)*.25)) # take a sample of 25% fo the shootings
af.export_list('initial-sample.csv', sample)
