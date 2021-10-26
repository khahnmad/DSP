import All_Functions as af
import glob
import pandas as pd

af.fix_field_errors()

text_files = [x for x in glob.glob('article-text' + "/*.csv")]  # Get all files in the given folder
mc_files =  [x for x in glob.glob('mediacloud-urls' + "/*.csv")]
badurl_files =  [x for x in glob.glob('bad-urls' + "/*.csv")]


summary_list = [['location', 'unclean','clean','checkpoint','urls','bad_urls']]
for file in text_files:
    location = af.get_event_name(file)
    if [location] not in summary_list:
        summary_list.append([location])
for i in range(len(summary_list)):
    while len( summary_list[i]) < 6:
        summary_list[i].append(0)


for file in text_files:
    location = af.get_event_name(file)
    if 'cleaned' not in file and '0' not in file:
        unclean_text = af.import_csv(file)
        for i in range(len(summary_list)):
            if summary_list[i][0] == location:
                summary_list[i][1] = len(unclean_text)

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
    location = af.get_event_name(file)
    urls = af.import_csv(file)
    for i in range(len(summary_list)):
        if summary_list[i][0] == location:
            summary_list[i][4] = len(urls)

for file in badurl_files:
    location = af.get_event_name(file)
    if '0' not in file:
        urls = af.import_csv(file)
        for i in range(len(summary_list)):
            if summary_list[i][0] == location:
                if urls != None:
                    summary_list[i][5] = len(urls)

df = pd.DataFrame(columns=summary_list[0], data=summary_list[1:])
df.to_csv('data_summary.csv',index=False)
