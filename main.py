from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

app = FastAPI()

line_bot_api = LineBotApi(os.getenv("ChannelAccessToken"))
parser = WebhookParser(os.getenv("ChannelSecret"))
openai.api_key = os.getenv("OPENAI_API_KEY")

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
            user_message = event.message.text

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "あなたは恋愛相談に強い優しい会話相手です。"},
                        {"role": "user", "content": user_message}
                    ]
                )
                reply_text = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                print("OpenAI error:", e)
                reply_text = "ちょっと考えさせて！もう一度送ってみてくれる？"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )

    return PlainTextResponse("OK")
