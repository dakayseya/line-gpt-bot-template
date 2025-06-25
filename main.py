from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = FastAPI()

line_bot_api = LineBotApi(os.getenv("ChannelAccessToken"))
parser = WebhookParser(os.getenv("ChannelSecret"))

@app.get("/")
def health_check():
    return PlainTextResponse("LINE GPT Bot is running!")

@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Line-Signature")

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except Exception as e:
        print("Webhook error:", e)
        return PlainTextResponse("Bad Request", status_code=400)

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"あなたのメッセージ: {event.message.text}")
            )

    return PlainTextResponse("OK")
