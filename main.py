from fastapi import FastAPI
import asyncio
from kafka_test import send_response
from google_trends import get_data_from_gg_trends
print("gg_trends imported successfully!")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Working!"}


@app.get("/trends/{keyword}")
async def say_hello(keyword: str):
    asyncio.create_task( send_data(keyword))
    return {"message": f"Hello {keyword}"}

async def send_data(keyword: str):
    data = get_data_from_gg_trends([keyword])
    send_response(keyword, data, "scrapy")