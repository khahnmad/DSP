import All_Functions as af
import glob


def get_relationship(location,shootings_data,text,stranger_articles,coworker_articles,family_articles):
    translated_location = af.translate_name(location)
    for event in shootings_data:
        if event[3] == translated_location:
            relationship = event[-1]
    if relationship == '0':
        for article in text:
            if article[-2] == '1': # if positive classification
                stranger_articles.append(article)
    if relationship == '1':
        for article in text:
            if article[-2] == '1':  # if positive classification
                coworker_articles.append(article)
    if relationship == '2':
        for article in text:
            if article[-2] == '1':  # if positive classification
                family_articles.append(article)
    return stranger_articles, coworker_articles, family_articles

def sort_articles(dict_files, shootings_data):
    stranger_articles, coworker_articles, family_articles, complete_locations = [['stories_id', 'publish_date', 'title', 'url', 'language', 'ap_syndicated', 'themes', 'media_id', 'media_name', 'media_url', 'text', 'location', 'Keywords', 'Count', 'Dict Class', 'Manual Class', 'Keywords', 'Count', 'Dict Class', 'Manual Class', 'Keywords', 'Count', 'Dict Class', 'Manual Class']],\
                                                                                [['stories_id', 'publish_date', 'title', 'url', 'language', 'ap_syndicated', 'themes', 'media_id', 'media_name', 'media_url', 'text', 'location', 'Keywords', 'Count', 'Dict Class', 'Manual Class', 'Keywords', 'Count', 'Dict Class', 'Manual Class', 'Keywords', 'Count', 'Dict Class', 'Manual Class']],\
                                                                                [['stories_id', 'publish_date', 'title', 'url', 'language', 'ap_syndicated', 'themes', 'media_id', 'media_name', 'media_url', 'text', 'location', 'Keywords', 'Count', 'Dict Class', 'Manual Class', 'Keywords', 'Count', 'Dict Class', 'Manual Class', 'Keywords', 'Count', 'Dict Class', 'Manual Class']],\
                                                                                []
    for file in dict_files:
        location = af.get_event_name(file)
        best_classification = 'dict-development\\'+location+'_round-3.csv'  # using round 3 since it's most often reliable, this could be improved
        if location not in complete_locations: # if we haven't already imported this event
            if best_classification in dict_files: # get round 3 if possible
                complete_locations.append(location) # keep track that we've already imported it
                text = af.import_csv(best_classification) # import the text (should be list of lists with length = 24)
                stranger_articles, coworker_articles, family_articles = get_relationship(location, shootings_data, text,
                                                                                         stranger_articles,
                                                                                         coworker_articles,
                                                                                         family_articles)
            elif best_classification not in dict_files:
                if location + '_round-2.csv' in dict_files:  # otherwise try round 2
                    complete_locations.append(location)
                    text = af.import_csv('dict-development' + location + '_round-2.csv')
                    stranger_articles, coworker_articles, family_articles = get_relationship(location, shootings_data,
                                                                                             text,
                                                                                             stranger_articles,
                                                                                             coworker_articles,
                                                                                             family_articles)
            else: # otherwise try round 1
                complete_locations.append(location)
                text = af.import_csv(file)
                stranger_articles, coworker_articles, family_articles = get_relationship(location, shootings_data, text,
                                                                                         stranger_articles,
                                                                                         coworker_articles,
                                                                                         family_articles)
    af.export_nested_list('Categorized_Classified/stranger_articles.csv',stranger_articles)
    af.export_nested_list('Categorized_Classified/coworker_articles.csv', coworker_articles)
    af.export_nested_list('Categorized_Classified/family_articles.csv', family_articles)

af.fix_field_errors()
# Import number of correctly classified articles
classified_articles = [x for x in glob.glob('dict-development' + "/*.csv")]
intial_sample = af.import_csv('generate-sample/intial-sample-w-info.csv')

# Categorize the classified articles
sort_articles(classified_articles, intial_sample)

# coworker = af.import_csv('Categorized_Classified/coworker_articles.csv')
print('debug')
