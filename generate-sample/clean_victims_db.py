import pandas as pd
import All_Functions as af


df = pd.read_csv('victim-db.csv')
print('debug')

victims = af.import_csv('victim-db.csv')
sampled_shootings = af.import_csv('intial-sample-w-info.csv')

relevant_victim_info = []
for i in range(1,len(sampled_shootings)):
    for j in range(1,len(victims)):
        if sampled_shootings[i][-1] == victims[j][0]: # if the victim row is from a shooting in the sample:
            if victims[j][6] == '1': # if the victim is female
                location = sampled_shootings[i][3]
                victim_name = victims[j][4]
                relationship = victims[j][9]
                relevant_victim_info.append([location, victim_name, relationship])
af.export_nested_list('Sampled_Victims.csv', relevant_victim_info)



