from bs4 import BeautifulSoup as bs
import requests

print('hello')
url = 'http://www.kansascity.com/2012/05/16/3613338/website-set-up-by-killers-mom.html#storylink=rss'
second = 'http://www.miamiherald.com/2012/04/20/2759259/suspected-texas-cockfight-organizers.html'
third='http://www.polygon.com/2015/4/21/8457673/life-is-strange-suicide'
soup = bs(requests.get(url, timeout=5).text, "html.parser")
print(soup)