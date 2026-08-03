from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# FastAPI 서버 객체 생성
app = FastAPI()

# 가상 아이템 생성
items_db = [
  {"item_name" : "item1", "price" : 1000},
  {"item_name" : "item2", "price" : 2000},
  {"item_name" : "item3", "price" : 3000},
  {"item_name" : "item4", "price" : 4000}
]

# GET 요청 처리
@app.get('/')
async def root():
  return {"message" : "Hello world!"}

# 경로 매개변수 처리
@app.get('/items/{item_id}')
async def item(item_id: int):
  return {"item" : item_id}

# items_db 전체를 확인하는 부분
@app.get('/item')
async def item_fun():
  return {"items" : items_db}

# 특정 item만 조회
@app.get('/item/{item_id}')
async def item(item_id: int):
  return {"item" : items_db[item_id]}


if __name__ == "__main__":
  uvicorn.run("main0803:app", host = "127.0.0.1", port = 8000, reload = True)