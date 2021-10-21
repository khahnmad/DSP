import All_Functions as af
from bs4 import BeautifulSoup as bs
import requests


a_list = [0,1,2,3,4,0]
leng = [20 for x in a_list]

result = map(lambda x, y: x/y, a_list, leng)
print(list(result))