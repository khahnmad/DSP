# Imports
from bs4 import BeautifulSoup as bs
import requests
from DSP import All_Functions as af
import glob
import requests.exceptions
import re


# FUNCTIONS
def access_article(url): # Acesses a single url and returns all the url's p tags
    soup = bs(requests.get(url, timeout=20).text, "html.parser")
    # timeout for the request is 20 seconds; it never takes longer than 10 seconds for a working link, so this is safe
    if 'rss.cnn' in url:
        body_text = soup.find_all("div", {"class": "zn-body__paragraph"})
        stripped_paragraph = [tag.get_text().strip() for tag in body_text]
    else:
        paragraphs = soup.find_all('p') # justify that this is working for the articles by taking a manual sample
        stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]
    return [url, " ".join(stripped_paragraph)] # [url, text from the url]


def get_text(urls_list, event_name, starting_url=0): # given a list of urls, returns the text from the working urls and a list of the bad urls
    # Initialize variables
    url_text = [['url', 'text']]
    bad_urls, midpoint_urls = [], []
    for i in range(starting_url, len(urls_list)):  # iterate through the urls
        if str(i).endswith('00') == True:
            print(f'    working on number {i}')
        try:
            text = access_article(urls_list[i])
            url_text.append(text) # get the article text
            midpoint_urls.append(text)
        except requests.exceptions.ReadTimeout:
            bad_urls.append(['Timeout error',urls_list[i]])

        except requests.exceptions.ConnectionError:
            bad_urls.append(['Connection error', urls_list[i]])

        except requests.exceptions.TooManyRedirects:
            bad_urls.append(['Too Many Redirects', urls_list[i]])

        if str(i).endswith('000'): # Exports the gathered information before running through all urls
            # Export urls & text that has been gathered so far
            csv_file_name = 'article-text\\' + event_name + '_text_' + str(i) + '.csv'
            af.export_nested_list(csv_file_name, midpoint_urls)

            # Export list of a bad urls
            bad_urls_csv_name = 'bad-urls\\' + event_name + '_bad-urls_'+ str(i)+'.csv'
            af.export_nested_list(bad_urls_csv_name, bad_urls)

    return url_text, bad_urls


# SUMMARY FUNCTION
def extract_article_content(csv_file, event_name):
    mediacloud_content = af.import_csv(csv_file)
    if mediacloud_content != None: # in case 0 urls are gathered from mediacloud from this timeframe
        urls = [mediacloud_content[i][3] for i in range(1,len(mediacloud_content))]
        text, bad_urls = get_text(urls, event_name)
        print('GOT TEXT')

        for i in range(len(mediacloud_content)):
            for j in range(len(text)):
                if text[j][0] == mediacloud_content[i][3]:
                    mediacloud_content[i].append(text[j][1])

        # Export nested list of all mediacloud content + the text from the given url
        csv_file_name = 'article-text\\' + event_name + '_text.csv'
        af.export_nested_list(csv_file_name, mediacloud_content)
        # Export list of a bad urls
        bad_urls_csv_name = 'bad-urls\\' + event_name + '_bad-urls.csv'
        af.export_nested_list(bad_urls_csv_name, bad_urls)
        print('--PROCESS COMPLETE--')


# RUN THE FUNCTIONS
all_files = [x for x in glob.glob('mediacloud-urls' + "/*.csv")]  # Get all files in the given folder

for file in all_files[11:]: # start at 10 for Red_lake
    regex = r"[A-Z].*(?=.c)"
    match = re.findall(regex, file)
    print(f'WORKING ON {match[0]}...')
    extract_article_content(file, match[0])