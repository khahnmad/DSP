import All_Functions as af
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt

# Functions
def get_event_name_urls(file):
    regex = r"[A-Z].*(?=\.)"  # regex for getting the location name of each event
    match = re.findall(regex, file)
    return match[0]


# Setup
af.fix_field_errors()

text_files = [x for x in glob.glob('article-text' + "/*.csv")]  # Get all files in the given folder
mc_files = [x for x in glob.glob('mediacloud-urls' + "/*.csv")]
badurl_files = [x for x in glob.glob('bad-urls' + "/*.csv")]

summary_list = [['location', 'unclean', 'clean', 'checkpoint', 'urls', 'bad_urls']]
for file in text_files:
    location = af.get_event_name(file)
    if [location] not in summary_list:
        summary_list.append([location])
for i in range(len(summary_list)):
    while len(summary_list[i]) < 6:
        summary_list[i].append(0)

for file in text_files:
    location = af.get_event_name(file)
    if 'cleaned' not in file and '0' not in file:
        unclean_counter = 0
        unclean_text = af.import_csv(file)
        for article in unclean_text:
            if len(article) == 11:
                unclean_counter += 1
        for i in range(len(summary_list)):
            if summary_list[i][0] == location:
                summary_list[i][1] = unclean_counter

    if 'cleaned' in file:
        clean_text = af.import_csv(file)
        for i in range(len(summary_list)):
            if summary_list[i][0] == location:
                summary_list[i][2] = len(clean_text)

    if '0' in file:
        checkpoint = af.import_csv(file)
        for i in range(len(summary_list)):
            if summary_list[i][0] == location:
                if checkpoint != None:
                    summary_list[i][3] += len(checkpoint)

for file in mc_files:
    location = get_event_name_urls(file)
    urls = af.import_csv(file)
    for i in range(len(summary_list)):
        if summary_list[i][0] == location:
            summary_list[i][4] = len(urls)

for file in badurl_files:
    location = af.get_event_name(file)
    if '0' not in file:
        urls = af.import_csv(file)
        for i in range(len(summary_list)):
            if summary_list[i][0] == location and urls is not None:
                actual_urls = [url for url in urls if url != []]  # get rid of the empty urls that appear often
                check_duplicates = []
                for item in actual_urls:
                    if item not in check_duplicates:
                        check_duplicates.append(item)
                summary_list[i][5] = len(check_duplicates)

df = pd.DataFrame(columns=summary_list[0], data=summary_list[1:])

df.to_csv('data_summary.csv', index=False)

# fig, ax = plt.subplots()
# ax.bar(df['location'],df['clean'],label='Useable text')
# ax.bar(df['location'],df['urls'],bottom=df['urls'],
#        label='Urls Acquired')
# # ax.set_ylabel('Scores')
# # ax.set_title('Scores by group and gender')
# ax.legend()
# plt.show()
