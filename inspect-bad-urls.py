"""
TODO
- create a function to randomly sample urls from different errors and check to see if they are actually unscrapabale
    - could tag the sampled urls with y or no for fixability
"""

import All_Functions as af
import glob
import re
import collections

# Fix the Aurora File format
# DO NOT RUN AGAIN
# bad_aurora = af.import_csv('bad-urls/Aurora_bad-urls.csv')
# fixed_aurora = []
# for i in range(len(bad_aurora[0])):
#     # split = bad_aurora[0][i].split()
#
#     error_regex = r"[A-Z].*[a-z] error"
#     error_match = re.findall(error_regex, bad_aurora[0][i])
#
#     url_regex = r"h.*?[']"
#     url_match = re.findall(url_regex, bad_aurora[0][i])
#
#     fixed_aurora.append([error_match[0], url_match[0][:-1]])
# af.export_nested_list('bad-urls/Aurora_bad-urls.csv', fixed_aurora)

all_files = [x for x in glob.glob('bad-urls' + "/*.csv")]  # Get all files in the given folder
complete_files = [x for x in all_files if '0' not in x]

bad_urls = []
for file in complete_files:
    regex = r"[A-Z].*(?=_)" # regex for getting the location name of each event
    match = re.findall(regex, file)
    imported = af.import_csv(file)
    for row in imported:
        row.append(match[0])
        bad_urls.append(row)

errors = [x[0] for x in bad_urls]
counter=collections.Counter(errors)
print('Most Common Errors:')
for tuple in counter.most_common(3):
    print(f"    {tuple[0]}: {tuple[1]}")

print('Number of bad urls per event')
events = [x[2] for x in bad_urls]
counter=collections.Counter(events)
for tuple in counter.most_common(len(all_files)):
    print(f"    {tuple[0]}: {tuple[1]}")

print('Most common bad websites:')
websites = [x[1] for x in bad_urls]
www = r"(?<=www.).*(?=.com)"
http = r"(?<=http).*(?=.com)"
# website_names = [re.findall(regex, website)[0] for website in websites if len(re.findall(regex, website))>0]
website_names = []
for website in websites:
    if len(re.findall(www, website))>0:
        website_names.append(re.findall(www, website)[0])
    elif len(re.findall(http, website))>0:
        website_names.append(re.findall(http, website)[0][3:])
    else:
        print(website)
counter=collections.Counter(website_names)
for tuple in counter.most_common(10):
    if tuple[1]>5:
        print(f"    {tuple[0]}: {tuple[1]}")