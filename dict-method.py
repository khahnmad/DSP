import All_Functions as af
import random

aurora = [['holmes',1],['2012',0.5]] # from the first round of tf-idf
aurora_words = ['holmes','2012']
aurora_scores = [1,0.5]

aurora = af.import_csv('article-text//Aurora_cleaned-text.csv')
aurora[0].append('Count')
for i in range(1,len(aurora)): # for article in dataset
    count = 0
    for j in range(len(aurora[i][10])): # for word in article
        for ii in range(len(aurora_words)): # for word in dictionary
            if aurora[i][10][j] == aurora_words[ii]:
                count += aurora_scores[ii]
    aurora[i].append(count)

aurora[0].append('About event?')
for i in range(1,len(aurora)):
    if aurora[i][-1]>=1: # setting threshold at 1
        aurora[i].append('Yes')
    else:
        aurora[i].append('No')

# take manual sample and classify
sample = random.sample(range(len(aurora)), int(len(aurora)*0.05))
print('checkpoint')
manually_classified =[[] for x in range(len(aurora))]
for i in range(len(aurora)):
    if i in sample:
        print(aurora[i][3])
        print(f'    About event?: {aurora[i][13]}')
        print('    Accurate?: y/n')
        x = input()
        if x == 'y':
            manually_classified[i]= [i,aurora[i][3], 'y']
        if x =='n':
            manually_classified[i] = [i, aurora[i][3], 'n']
