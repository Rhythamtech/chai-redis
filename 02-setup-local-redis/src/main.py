import json
import uvicorn
from redis import Redis
from pymongo import MongoClient
from fastapi import FastAPI


app = FastAPI()

r = Redis(host='localhost', port=6379, db=0, decode_responses=True)
mongo_client = MongoClient("mongodb://localhost:27017/chai_aur_redis")



@app.get("/redis")
async def redis_reply():
    response = r.ping()

    return {
        "redis" : response
    }  

@app.get("/mongo")
async def redis_reply():

    return {
        "mongo" : mongo_client.admin.command('ping')
    }  

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
