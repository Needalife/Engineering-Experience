import altair as alt,streamlit as st,pandas as pd, numpy as np # type: ignore
import requests,time # type: ignore
from utils.mongo import *
from pymongo import MongoClient # type: ignore

@st.cache_resource
def connectMongo():
    response = requests.get("https://us-central1-project-finance-400806.cloudfunctions.net/get-mongo-uri")
    if response.status_code == 200:
        response.close()
    
    mongoHandler = mongo(response.text,'data')
    
    return mongoHandler

@st.experimental_memo()
def watch_collection(collection):
    with collection.watch() as stream:
        for change in stream:
            st.write(change)
            return

uri = "mongodb+srv://gauakanguyen:AOMhWKFdmlSO6kcU@transactiondata.wecxmij.mongodb.net/?retryWrites=true&w=majority&appName=transactionData"
client = MongoClient(uri)

database = client['data']
collection = database['raw']

rule = database['rule']
rule = rule.find_one({})

#UI start

while True:
    watch_collection(collection)