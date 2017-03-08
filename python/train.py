import zerorpc
import json
import StringIO
import pandas as pd
import numpy as np
from pandas_datareader import data as web

import logging
logging.basicConfig(filename='logs/train.log',level=logging.INFO)

from slicematrixIO import SliceMatrix

api_key = open("../.env.example", "r").read().split("=")[-1].replace("\n","")
sm = SliceMatrix(api_key)

#data = pd.read_csv("https://s3.amazonaws.com/static.quandl.com/tickers/dowjonesA.csv")
#data = pd.read_csv("https://s3.amazonaws.com/static.quandl.com/tickers/nasdaq100.csv")
data = pd.read_csv("https://s3.amazonaws.com/static.quandl.com/tickers/SP500.csv")

import datetime as dt

start = dt.datetime(2016, 1, 1)
end = dt.datetime.now()

volume = []
closes = []
good_tickers = []
for ticker in data['ticker'].values.tolist():
    logging.info(ticker)
    try:
        vdata = web.DataReader(ticker, 'yahoo', start, end)
        cdata = vdata[['Close']]
        closes.append(cdata)
        vdata = vdata[['Volume']]
        volume.append(vdata)
        good_tickers.append(ticker)
        logging.info("success")
    except:
        logging.info("x")

closes = pd.concat(closes, axis = 1)
closes.columns = good_tickers

diffs = np.log(closes).diff().dropna(axis = 0, how = "all").dropna(axis = 1, how = "any")
diffs.head()

iso  = sm.Isomap(dataset = diffs, D = 2, K = 6)
logging.info("Isomap created sucessfully")
logging.info(iso.name)

name_file = open("iso.name", "w")
name_file.write(iso.name)
name_file.close()
