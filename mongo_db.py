from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

#establishing the connection

mongo_url = os.getenv("Mongo_Url")
print(f"Connecting to MongoDB...")  # Don't print the actual URL (security)
client = AsyncIOMotorClient(mongo_url)
db = client["test_db_1"]
collection = db["test_coll"]

#print(data)
#object creation of API
app = FastAPI()

#pydantic classes
class TestData(BaseModel):
    name: str
    score: int
    city: str
    team: str

def helper(doc):
    doc["id"] = str(doc["_id"]) 
    del doc["_id"]   #trying to remove the ID part
    return doc

#function to insert data
@app.post("/test/insert")
async def data_insert(data: TestData):
    result = await collection.insert_one(data.model_dump())
    return {"message" : "data inserted successfully"}



@app.get("/test/getdata")
async def get_collection():
    items = []
    cursor = collection.find({})
    async for document in cursor:
        items.append(helper(document))
    return items