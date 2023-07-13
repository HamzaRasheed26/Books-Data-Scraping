from tkinter.ttk import Style
from urllib import response
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# lists for data
titles = []
authors = []
prices = []
words = []
languages = []
publishes = []
Categories = []

def scrapeBookPage(url):
    

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    webpage = response.content

    soup = BeautifulSoup(webpage,"html.parser")

    # the logic
    for parent in soup.find_all('div',id="pageCenterContent"):
        for n,tag in enumerate(parent.find_all('div',class_="library-book row p-2")):
            
            bookName= ""
            author = ""
            price = "0"
            category = []
            publish = ""
            language = ""
            word = "0"
            isbn = ""

            d1 = [x for x in tag.find_all('a', class_="library-title")]
            d2 = [x for x in tag.find_all('span', style="white-space: nowrap")]
            information = [x for x in tag.find_all('span', class_="text-nowrap")]

            for item in d1:
                bookName = item.text.strip()
            for item in d2:
                author = item.text.strip()

            for item in information:
                d3 = item.text.strip()

                if str(d3)[0:1] == "$":
                    price = d3.replace('$', '')
                    price = price.replace(' USD.', '')

                if str(d3)[0:5] == "Words":
                    word = d3.replace('.', '')
                    word = word.replace('Words: ', '')

                if str(d3)[0:8] == "Language":
                    language = d3.replace('.', '')
                    language = language.replace('Language:\n                ', '')

                if str(d3)[0:9] == "Published":
                    publish = d3.replace('Published: ', '')

            d4 = [x for x in tag.find_all('div', class_="subnote")]
            for item in d4:
                d5 = item.find_all('a')
            for item in d5:
                d6 = item.text.strip()
                category.append(str(d6))

            titles.append(bookName)
            authors.append(author)
            prices.append(price)
            words.append(word)
            languages.append(language)
            publishes.append(publish)
            Categories.append(category)

   # return titles, authors, prices, words, languages, publishes, Categories


url = "https://www.smashwords.com/books/category/1/newest/0/any/any/0"
start_time = time.time()

link = 276001
for i in range(4600):
    url = "https://www.smashwords.com/books/category/1/newest/0/any/any/"
    url = url + str(link)
    scrapeBookPage(url)
    link += 20
    print("Complete ",i)


end_time = time.time()
print("Run TIme", end_time-start_time)
print(url)
print(len(titles))
print(len(authors))
print(len(prices))
print(len(words))
print(len(languages))
print(len(Categories))
print(len(publishes))


df = pd.DataFrame({'Title':titles,'Author':authors,'Price':prices,'Words':words,'Language':languages,'Published':publishes,'Category':Categories})
df.to_csv('books4.csv',mode='a', index=False, encoding='utf-8')

