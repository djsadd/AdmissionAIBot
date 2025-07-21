from fastapi import FastAPI

from db.models import AskRequest
from server.ask_groq import ask_ai
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Привет, мир!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/ask_ai/")
async def ask_ai_endpoint(data: AskRequest):
    print(data.query, data.uuid,  data.platform)
    # data.query — текст запроса
    # data.platform — PlatformEnum.whatsapp или telegram
    answer = await ask_ai(data.query, data.uuid , data.platform)
    return {"answer": answer}

    # return {"you_asked": data.query, "platform": data.platform.value}