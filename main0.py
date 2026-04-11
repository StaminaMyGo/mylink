from fastapi import FastAPI
from fastapi import Query
from fastapi import Form
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/search")
async def search(
    q: str = Query(None, min_length=3, max_length=50),
    page: int = Query(1, ge=1, le=100)
):
    return {"q": q, "page": page}

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    tax: float = None

@app.post("/items")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

from fastapi import File, UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "content_type": file.content_type}

@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

from fastapi import Depends

def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/{user_id}/items")
async def read_user_items(
    user_id: int,
    category: str = Query(None, description="Filter by category"),
    q: str = Query(None, alias="search-term"),
    sort: str = Query("name")
):
    return {
        "user_id": user_id,
        "category": category,
        "q": q,
        "sort": sort
    }

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)