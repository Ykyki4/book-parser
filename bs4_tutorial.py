import requests
from bs4 import BeautifulSoup
import lxml

url = 'https://www.franksonnenbergonline.com/blog/life-lessons-become-the-best-version-of-yourself/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text
image_url = soup.find('img', class_='attachment-post-image')['src']
post_text = soup.find('div', class_='entry-content').text
print(image_url)
print(title_text)
print(post_text)
