from typing import Optional

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
async def google_action(request: Request):
    print("IN GOOGLE ACTION")
    print(f" my body {await request.json()}")
    return {
        "fulfillmentText": "response text",
        "fulfillmentMessages": [{"simpleResponses": {"simpleResponses": [{
            "textToSpeech": "response text",
            "displayText": "response text"
        }]}}]
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
