import uvicorn
from fastapi import FastAPI
from basemodel import input
import numpy as np
import pickle
import pandas as pd

file1 = open('similarity.pkl', 'rb')
similarity = pickle.load(file1)



file = open('data.pkl', 'rb')
df = pickle.load(file)

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello, World'}

@app.post('/recommend')
def RoomList(data:input):
    data = data.dict()
    tags = data["Text"]
    result = set()
    for i in tags:
        x = recommend(i)
        for y in x:
            result.add(y)

    result = list(result)
    return { 
        "recommend" : result
    }
    




def recommend(Tag):
    y=[]
    index = df[df['Tags'] == Tag].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:10]:
        if df.iloc[i[0]].Tags not in (df.iloc[i[0]].Tags).split():
            y.append(df.iloc[i[0]].Tags)
    l = list(set(y))
    x = " ".join(l)
    k = x.split()
    result = []
    if Tag not in set(k):
        result.append(Tag)
    for i in set(k):
        result.append(i)

    return result




#recommend('c++')
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)