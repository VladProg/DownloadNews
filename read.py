import os

def category_articles():
    return  {category: [open('categories/' + category + '/' + article, encoding='utf-8').read()
                        for article in os.listdir('categories/' + category)]
             for category in os.listdir('categories')}
