#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import re
from dotenv import load_dotenv
load_dotenv()
# require OPEN_AI_KEY
import openai

filename = sys.argv[1]

s = ""
body = ""
title = ""
obj = None
with open(filename, encoding="utf-8") as f:
  obj = json.load(f)
  s = obj["original_content"]

if obj.get("title") != None:
  print("already processed")
  sys.exit()

response = openai.ChatCompletion.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "あなたは英語の文章を翻訳して50文字の日本語に要約するシステムです"},
    {"role": "user", "content": "私は電子工作に興味があり、自分で物を作ることが好きです。ハードウェアやソフトウェアの知識もあります。"},
    {"role": "user", "content": "以下の記事の50文字程度の日本語に要約してください\n\n"+ s}
  ]
)
body = response["choices"][0]["message"]["content"]

response = openai.ChatCompletion.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "あなたは英語の文章から5つの日本語のタイトルを作成するシステムです。"},
    {"role": "system", "content": "記事の内容を要約し簡潔なタイトルを箇条書きで作成します。このタイトルは電子工作に興味のある読者をターゲットにしています。"},
    {"role": "user", "content": "私は電子工作に興味があり、自分で物を作ることが好きです。ハードウェアやソフトウェアの知識もあります。"},
    {"role": "user", "content": "以下の記事の簡潔な日本語タイトルを5つ考えてください\n\n"+ s}
  ],
  n = 1
)
titles = (list(map(lambda a: re.sub(r'\d\.\s+',"",a),response["choices"][0]["message"]["content"].split("\n"))))
title = titles[0]

obj['title'] = title
obj['body'] = body
obj["titles"] = titles
print(titles)
print(body)

# overwrite
with open(filename, "w+") as f:
  json.dump(obj, f);

time.sleep(60) # wait for prevent throttoling
