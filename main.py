from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def health_check():
    return PlainTextResponse("LINE GPT Bot is running!")

@app.post("/callback")
async def callback(request: Request):
    data = await request.body()
    print("Received webhook:", data)
    return PlainTextResponse("OK")
