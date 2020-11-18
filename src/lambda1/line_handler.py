#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, LocationMessage, StickerMessage,
    TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage,
    QuickReply, QuickReplyButton, CameraAction, CameraRollAction, LocationAction,
    FollowEvent, SourceUser,
)

from dialogflow_lib.detect_intent_texts import post_intent_texts

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET'))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-auth.json"
dialogflow_project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
language_code = os.getenv('LANGUAGE_CODE', 'ja-JP')

tmp_dir = Path(os.getenv("TMPDIR", "/tmp"))

logger = logging.getLogger(__name__)


WELLCOME_MESSAGE = """
{nickname_call}はじめまして！😃
友だち追加ありがとうございます。firsttest002 です。

このトークからの通知を受け取らない場合は、画面右上のメニューから通知をオフにしてください。
""".strip()


def callback(headers, body):
    # get X-Line-Signature header value
    signature = headers['X-Line-Signature']

    # get request body as text
    logger.info("Request body: " + body)

    # handle webhook body
    handler.handle(body, signature)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    """ FollowEvent handler """
    user_id = event.source.user_id

    # あいさつメッセージの準備
    nickname_call = ""
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(user_id)
        nickname_call = f"{profile.display_name}さん、"
    welcome_messages = [TextSendMessage(text=WELLCOME_MESSAGE.format(nickname_call=nickname_call))]

    # あいさつメッセージを添えて、初期メッセージを出す
    line_bot_api.reply_message(
        event.reply_token,
        welcome_messages
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """ TextMessage handler """
    # LINE Bot のテストでエラーにならないようにするため see https://qiita.com/q_masa/items/c9db3e8396fb62cc64ed
    if event.reply_token == "00000000000000000000000000000000":
        return

    user_id = event.source.user_id
    input_text = event.message.text

    try:
        results = post_intent_texts(dialogflow_project_id, user_id, [input_text], language_code)
        response_text = results[0]['fulfillment']
    except:
        response_text = "わかりませんでした。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_text)
    )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    """ ImageMessage handler """
    user_id = event.source.user_id

    # 画像をいったんローカルに保存
    message_content = line_bot_api.get_message_content(event.message.id)
    file_path = tmp_dir / f"{event.message.id}.jpg"
    with file_path.open("wb") as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    # メッセージ送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="画像がきました")
    )


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    """ LocationMessage handler """
    user_id = event.source.user_id
    address = event.message.address
    lat = event.message.latitude
    lng = event.message.longitude

    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(title="お店の場所", address=address, latitude=lat, longitude=lng)
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    """ StickerMessage handler - スタンプのハンドラ"""
    # LINE Bot のテストでエラーにならないようにするため see https://qiita.com/q_masa/items/c9db3e8396fb62cc64ed
    if event.reply_token == "ffffffffffffffffffffffffffffffff":
        return

    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id)
    )
