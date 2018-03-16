#! /usr/bin/env python3

import newspaper

from py_apify import ApifyClient

import nltk


if __name__ == '__main__':
    
    apify = ApifyClient()

    listFile = open('urllist.txt','r')

    for url in listFile:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        article.nlp()
        for var in vars(article):
            print(var)
        apify.pushData({
            'authors': article.authors,
            'text': article.text,
            'title': article.title,
            'movies': article.movies,
            'images': article.images,
            'top_img': article.top_img
            'summary': article.summary,
            'publish_date': article.publish_date,
            'canonical_link': article.canonical_link,
            'url': article.url,
            'imgs': article.imgs,
            'keywords': article.keywords
            })
        
