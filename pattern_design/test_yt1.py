from bs4 import BeautifulSoup
import urllib

html = urllib.urlopen('http://comic.naver.com/index.nhn')
soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify())
print(soup.title)
print(soup.title.name)
print(soup.title.string)
print(soup.a)
#print(soup.find_all('a'))
for link in soup.find_all('a'):
    aaa = (link.get('href'))
