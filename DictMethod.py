import All_Functions as af
import random


def apply_dict_method(round_no:int, cleaned_text, dictionary, threshold=3):
    content = af.import_csv(cleaned_text) # Import csv
    content[0].append('Keywords')
    content[0].append('Count')

    # Classify articles based on current dictionary
    for i in range(1,len(content)): # for article in dataset
        count = 0
        keywords = []
        for j in range(len(content[i][10])): # for word in article
            for ii in range(len(dictionary['words'])): # for word in dictionary
                if content[i][10][j] == dictionary['words'][ii]:
                    count += dictionary['scores'][ii]
                    keywords.append(dictionary['words'][ii])

        if len(keywords)>=2: # Add another count if there is more than 1 unqiue word present
            same_words= [keywords[0] for i in range(len(keywords))]
            if keywords != same_words:
                count += 1

        content[i].append(keywords)
        content[i].append(count)

    content[0].append('Dict Class')
    for i in range(1,len(content)):
        if content[i][-1]>=threshold: # setting threshold at 1
            content[i].append(1) # 1 for yes
        else:
            content[i].append(0) # 0 for no

    # take sample and classify manually
    sample = random.sample(range(len(content)), int(len(content)*0.1))
    print(f'Manually check {len(sample)} articles...')
    content[0].append('Manual Class')
    for i in range(len(content)):
        if i in sample:
            print(content[i][3])
            print(content[i][2])
            print(f'    Classification: {content[i][13]}')
            print('    About event?: y/n')
            x = input()
            # x='y' # DEBUGGING
            if x == 'y':
                content[i].append(1)
            if x =='n':
                content[i].append(0)
                # std_lngth = len(content[i])
    std_length = len(content[0])
    for i in range(len(content)):
        if len(content[i])<std_length:
            content[i].append('None')
    # Export
    csv_name = 'dict-development\\'+af.get_event_name(cleaned_text)+'_round-'+str(round_no)+'.csv'
    af.export_nested_list(csv_name,content)


def eval_dict_method(file,round_no):
    positives, negatives, fps, fns, tps,tns = 0,0,0,0,0,0
    evaluation = [['positives','negatives','fps','fns','tps','tns', 'precision','recall']]
    content = af.import_csv(file)
    for i in range(len(content)):
        if content[i][-2] == '1': # positives
            positives += 1
        if content[i][-2] == '0': # negatives
            negatives +=1
        if content[i][-2] == '1' and content[i][-1] == '0': # false positives
            fps +=1
        if content[i][-2] == '0' and content[i][-1] == '1': # false negatives
            fns +=1
        if content[i][-2] == '1' and content[i][-1] == '1': # true positives
            tps +=1
        if content[i][-2] == '0' and content[i][-1] == '0': # true negatives
            tns +=1
    precision = tps/(tps+fps)
    recall = tps/(tps+fns)
    print(f"    Precision: {precision}")
    print(f"    Recall: {recall}")
    evaluation.append([positives, negatives, fps, fns, tps,tns, precision, recall])
    location = af.get_event_name(file)
    af.export_nested_list(location+'_'+str(round_no)+'-eval.csv', evaluation)


# from the first round of tf-idf
aurora_dict=  {'words':['holmes', '2012'], 'scores':[1, 0.5]}
aurora_dict1 = {'words':['holmes', '2012','batman','.40-caliber','moviegoers'], 'scores':[1, 0.5, 0.75,1,0.75]}
aurora_dict2 = {'words':['holmes', '2012','batman','.40-caliber','moviegoers','apartment','university','aurora','theater','colorado','bale','theaters'],
                'scores':[1, 0.5, 0.75,1,0.75,0.5,0.25,1,.75,.75,0.5,0.75]}
aurora_word2vec_dict = {'words':['aurora','theater', 'shooting','mass','new','night','colorado','friday',
                                 'left','early', 'rampage','latest','killing','gunman','opened','fire','bale','denver','injured','theaters'],
                'scores':[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]}
# apply_dict_method(5,'article-text/Aurora_cleaned-text.csv',aurora_dict2)
# eval_dict_method('Aurora_round_5.csv')

