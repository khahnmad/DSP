import All_Functions as af
import glob
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns

# Functions
def get_date_numbers(shooting):
    """
    :param shooting: takes a list of lists in which each sublist is an article and the big list is one shooting
    output: adds a 5-day interval range to the end of each article, indicating at which point in the the 3-month period
    the article was written
    """
    # FIRST: find the earliest date in the dataset - this is the day the shooting took place
    just_dates = [x[1] for x in shooting[1:]] # list of just the dates - [1] is the date index
    # convert to datetime so we can compare
    dates_list = []
    for i in range(len(just_dates)):
        if len(just_dates[i]) == 26: # this is for the cases where there are 7 random numbers at the end of the date
            fixed = just_dates[i][:-7]
            date_obj = datetime.strptime(fixed, "%Y-%m-%d %H:%M:%S").date()
            dates_list.append(date_obj)
        if len(just_dates[i]) == 0: # this is for the cases where there is no date information
            dates_list.append(dates_list[i-1])
        if len(just_dates[i])==19: # this is for the "normal" cases
            date_obj = datetime.strptime(just_dates[i], "%Y-%m-%d %H:%M:%S").date()
            dates_list.append(date_obj)
    oldest = min(dates_list)

    # SECOND: append the number of days passed to each of the individual shooting articles
    for i in range(1,len(shooting)):
        if len(shooting[i][1]) == 19:
            datetime_vers = datetime.strptime(shooting[i][1], "%Y-%m-%d %H:%M:%S").date()
            days_passed = datetime_vers - oldest
            shooting[i].append(days_passed)
        elif len(shooting[i][1])==0:
            shooting[i].append(shooting[i-1][-1])
        else:
            date = shooting[i][1][:-7]
            datetime_vers = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
            days_passed = datetime_vers - oldest
            shooting[i].append(days_passed)

def append_date_numbers(text,freq_data): # add the day of publication to the end of ecah article
    if len(text) > 0:  # some files are empty, have to accomodate this
        get_date_numbers(text)  # Get Date Numbers
        for article in text:
            if article[-3] == '1':  # if the article is pos classified
                date = article[-1].days
                freq_data[1][date] += 1
    return text, freq_data # should now have text data with length 25 per list & freq data


def separate_by_relat(file, time_data,counter,family_freq_data,strang_freq_data,coworker_freq_data):
    location = af.get_event_name(file)
    translated_name = translate_name(location)
    for event in shootings_db:
        if event[3] == translated_name:
            relat_level = event[-1]
    if relat_level == '0': # strangers
        strang_freq_data[1] = [x + y for (x, y) in zip(strang_freq_data[1], time_data[1])]
        counter[0]+=1
    if relat_level == '1': # coworkers/ co-students
        coworker_freq_data[1] = [x + y for (x, y) in zip(coworker_freq_data[1], time_data[1])]
        counter[1]+=1
    if relat_level == '2': # family
        family_freq_data[1] = [x + y for (x, y) in zip(family_freq_data[1], time_data[1])]
        counter[2]+=1
    return family_freq_data,strang_freq_data,coworker_freq_data, counter


def get_freq_data(all_files):
    family_freq_data = [[x for x in range(100)], [0 for x in range(100)]]
    strang_freq_data = [[x for x in range(100)], [0 for x in range(100)]]
    coworker_freq_data = [[x for x in range(100)], [0 for x in range(100)]]

    count = [0, 0, 0]
    complete_locations = []  # keep track of each of the events so i don't import an event twice
    for file in all_files:

        freq_data = [[x for x in range(100)], [0 for x in range(100)]]
        location = af.get_event_name(file)
        best_classification = 'dict-development\\'+location+'_round-3.csv'  # using round 3 since it's most often reliable, this could be improved

        if location not in complete_locations: # if we haven't already imported this event
            if best_classification in classified_articles: # get round 3 if possible
                text = af.import_csv(best_classification) # import the text (should be list of lists with length = 24)
                complete_locations.append(location)
                text, freq_data = append_date_numbers(text, freq_data)
                family_freq_data,strang_freq_data,coworker_freq_data, count= separate_by_relat(file, freq_data, count, family_freq_data, strang_freq_data, coworker_freq_data)
            elif best_classification not in classified_articles:
                if location + '_round-2.csv' in classified_articles:  # otherwise try round 2
                    text = af.import_csv('dict-development' + location + '_round-2.csv')
                    complete_locations.append(location)
                    text, freq_data = append_date_numbers(text, freq_data)
                    family_freq_data,strang_freq_data,coworker_freq_data, count= separate_by_relat(file, freq_data, count, family_freq_data, strang_freq_data, coworker_freq_data)
            else: # otherwise try round 1
                text = af.import_csv(file)
                complete_locations.append(location)
                text, freq_data = append_date_numbers(text, freq_data)
                family_freq_data,strang_freq_data,coworker_freq_data, count= separate_by_relat(file, freq_data, count, family_freq_data, strang_freq_data, coworker_freq_data)

    family_data = list(np.array(family_freq_data[1])/count[2])
    coworker_data = list(np.array(coworker_freq_data[1])/count[1])
    stranger_data = list(np.array(strang_freq_data[1])/count[0])

    return family_data,coworker_data , stranger_data



# Setup
af.fix_field_errors()
# Import number of correctly classified articles
classified_articles = [x for x in glob.glob('dict-development' + "/*.csv")]
shootings_db = af.import_csv('generate-sample/intial-sample-w-info.csv')

family_freq_data, coworker_freq_data, strang_freq_data = get_freq_data(classified_articles)

print('debug')


# do we need the first list of freq_data?

time = [x for x in range(100)] # what is the actual limit of this range todo
summary = [time, family_freq_data, coworker_freq_data, strang_freq_data]

summary_df = pd.DataFrame(data=summary).T
summary_df.columns = ['Days Passed','Family Members', 'Colleagues','Strangers']
# plt.figure(figsize=(20, 10))
sns.lineplot(data=summary_df, x="Days Passed", y='Family Members').set_title('Intensity of coverage')
sns.lineplot(data=summary_df, x="Days Passed", y='Colleagues')
sns.lineplot(data=summary_df, x="Days Passed", y='Strangers')
plt.legend(['Family Members','Colleagues','Strangers'])
plt.ylabel("Average Number of Articles")
plt.show()

# Save data as a csv file
summary_df.to_csv('results/intensity_data.csv')


# Get date ranges for the classified articles

# Plot lines x-axis: time, y-axis= number of articles, one line = average for family victims, second = avg for
# co-workers/ students, third = avg for strangers
