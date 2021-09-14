from flask import Flask,jsonify
import requests
import os
import json
from bs4 import BeautifulSoup
import pandas as pd

from flask import Flask, request, \
render_template, redirect, url_for, \
session, send_file
from flask import (Flask,request,redirect,session)


app = Flask(__name__)

@app.route('/<url>',  methods=["GET", "POST"])
def sparkfun(url):
        uri=str(url)
        compurl="https://www.sparkfun.com/categories/"+uri
        result = requests.get(compurl)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        prodtitle=[]
        products = soup.find_all('div', attrs={'class': 'main'})
        for i in products:
            for j in i.find_all('h3'):
                for k in j.find_all('a'):
                    prodtitle.append(k.text)
        li=[]
        pics=soup.find_all('div', attrs={'class': 'actions-wrap'})
        for p in pics:
            for q in p.find_all('a'):
                for r in q.find_all('img'):
                    s= li.append(r['src'])
        pricelist=[]
        prices=soup.find_all('div', attrs={'class': 'prices'})
        for a in prices:
                pricelist.append(a.text)

        #lists of different parameter to dictionary
        data={'Product Title':prodtitle,'Product Image Links':li,"prices":pricelist}
        
        #dictionary to dataframe
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()

        #df to json
        result = df.to_json(orient="index")
        parsed = json.loads(result)
        h=json.dumps(parsed, indent=4)
        return h

@app.route('/productdetails/<url1>',  methods=["GET", "POST"])
def sparkfun2(url1):
    uri=str(url1)
    compurl="https://www.sparkfun.com/products/"+uri
    result = requests.get(compurl)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    prodesc=[]
    products = soup.find_all('div', attrs={'id': 'description-tab'})
    for u in products:
            for v in u.find_all('p'):
                    prodesc.append(v.text)
    
    prodprice=[]
    pprices = soup.find_all('div', attrs={'class': 'display-price'})
    for pp in pprices:
            for tt in pp.find_all('h3'):
                    oo=tt.text
    prodprice.append(oo)

    prodtitle=[]
    ptitle = soup.find_all('div', attrs={'class': 'product-title'})
    for pt in ptitle:
            for title in pt.find_all('h1'):
                oott=title.text
    prodtitle.append(oott)

    aggrating=[]
    rating = soup.find_all('div', attrs={'itemprop': 'aggregateRating'})
    for g in rating:
            for h in g.find_all('h3'):
                    aggrating.append(h.text)

    reviewdes=[]
    reviews = soup.find_all('div', attrs={'class': 'review-text'})
    for a in reviews:
            for f in a.find_all('p'):
                reviewdes.append(f.text)
    
    reviewperson=[]
    author = soup.find_all('p', attrs={'class': 'review-byline text-muted'})
    for au in author:
            for auid in au.find_all('a'):
                    reviewperson.append(auid['href'])
    
    proddata={'Product Name':prodtitle,'Product Description':prodesc,'Product Price':prodprice,'Product Rating':aggrating,"Produc Reviews":reviewdes,"Reviewed By":reviewperson}
    return proddata

if __name__ == "__main__":
    app.run(debug=True)