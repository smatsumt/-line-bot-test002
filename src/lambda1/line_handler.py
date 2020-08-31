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
    TextSendMessage, ImageSendMessage, StickerSendMessage,
    QuickReply, QuickReplyButton, CameraAction, CameraRollAction, LocationAction,
    FollowEvent, SourceUser,
)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET'))
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
    user_id = event.source.user_id
    input_text = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=input_text)
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

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"入力された住所は{address}です")
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    """ StickerMessage handler - スタンプのハンドラ"""
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id)
    )
