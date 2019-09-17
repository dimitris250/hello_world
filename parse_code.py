# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 01:51:34 2017

@author: Dimitrid
"""

import bs4 as bs
import urllib.request
import pandas as pd
import urllib.parse
import re


source = urllib.request.urlopen('https://messageboards.webmd.com/').read()
source = urllib.request.urlopen('https://messageboards.webmd.com').read()
soup = bs.BeautifulSoup(source,'lxml')

    
df = pd.DataFrame(columns = ['link'],data=[url.a.get('href') for url in soup.find_all('div',class_="link")])
lists =[]
page_links = []
for i in range(0,33):
    link = (df.link.iloc[i])
    req = urllib.request.Request(link)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    temp1=re.findall(r'Filter by</span>(.*?)data-pagedcontenturl',str(respData))
    temp1=re.findall(r'data-totalitems=(.*?)data-pagekey',str(temp1))[0]
    pageunm=round(int(re.sub("[^0-9]","",temp1))/10)
    lists.append(pageunm)
    
    
    for number in range(1, pageunm+1):
        url_pages = link + '?pi157388622=' + str(number)
        page_links.append(url_pages)

lists2=[]
df1= pd.DataFrame (columns=['page'],data=page_links)
for j in range (0,270):
    page = (df1.page.iloc[j])
    url = urllib.request.urlopen(page).read()
    soup1 = bs.BeautifulSoup(url,'lxml')
    for body_links in soup1.find_all('div',class_="thread-detail"):
        body= body_links.a.get('href')
        lists2.append(body)

usernames=[]
bodies=[]
dates=[]
titles=[]
tags=[]
categories=[]

df2= pd.DataFrame(columns =['post'], data= lists2)
for y in range(0,2640):
    post=( df2.post.iloc[y])
    url_post = urllib.request.urlopen(post).read()
    soup2= bs.BeautifulSoup(url_post,'lxml')
    username = soup2.find_all('div', class_="user-name")[0].get_text().strip()
    usernames.append(username)
    body= soup2.find_all('div',class_="thread-body")[0].get_text().strip()
    bodies.append(body)
    date = soup2.find_all('div',class_="thread-ago")[0].get_text().strip()
    dates.append(date)
    title= soup2.find_all('div',class_="thread-detail")[0].a.get_text().strip()
    titles.append(title)
    tag= soup2.find_all('div',class_="thread-tags")[0].get_text().strip()
    tags.append(tag)
    category= soup2.find_all('h1',class_="title")[0].get_text().strip()
    categories.append(category)

    unique_inf_parenting= pd.DataFrame(
                    {'title':titles,
                     'username':usernames,
                     'date':dates,
                     'body':bodies,
                     'link':lists2})
    
posttags=pd.DataFrame({'tags':tags})
posttags.to_csv('tags_final')

categories_final = pd.DataFrame({'category':categories})
categories_final.to_csv('categories')
unique_inf_parenting.to_csv('CORRECT_FINAL')
            
        