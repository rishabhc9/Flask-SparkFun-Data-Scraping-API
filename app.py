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
        return f'<h5>{h}</h5>'


if __name__ == "__main__":
    app.run(debug=True)