from bs4 import BeautifulSoup
from urllib import request
import urllib
import nltk
import re


def unknown(url):
    with urllib.request.urlopen(url) as text:
        text = (text.read())
        print(str(text))
        text = str(text)
        text = re.sub(r'\<script(?:.|\n)*?\<\/script\>', '', text)
        text = re.sub(r'\<style(?:.|\n)*?\<\/style\>', '', text)
        soup = BeautifulSoup(text)
        content = soup.get_text()
        lowercased = re.findall(r'[\s\(\[\{]([a-z]+)', content)
        words = nltk.corpus.words.words()
        return set([w for w in lowercased if w not in words])

nltk.download('words')
print(unknown('https://www.bbc.com/news'))
