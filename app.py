from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('lA5i0rokZ0dMwGKv5k8xI+I81tbBsYKlg/fszBP8ztEoQmr82cb9Pl9vjI8jSRVzd6dyoD48kPXtnhVqBZHVXTtUyj0gX6qWIGGn8ob4ZtDUJBZ5zhZdGHCMAT5uhaZn+oLMiFG5kVyXybg3J6nUegdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b3ec89409e0a68012dde622580ba8bb7')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()