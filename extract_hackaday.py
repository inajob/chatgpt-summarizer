#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import re
import json
import os
import datetime
from urllib.parse import urlparse, quote

feed = feedparser.parse("https://hackaday.com/blog/feed/")

for entry in feed.entries:
  obj = {}
  obj["pubDate"] = datetime.datetime(*entry.published_parsed[:6]).isoformat()
  print(obj["pubDate"])
  obj['original_title'] = entry.title
  obj["link"] = entry.link
  obj["source"] = "https://hackaday.com/blog/feed/"
  url = urlparse(obj["link"])
  filename = quote(url.netloc + url.path, safe="")
  if entry.get("media_thumbnail") != None:
    for p in entry.media_thumbnail:
      obj['thumbnail'] = p["url"]
      break;
  for c in entry.content:
    m = re.search(r'https://www\.youtube\.com/watch\?v=(\w+)',c.value)
    if m != None:
      obj["youtube"] = m.group(0)
    obj['original_content'] = re.sub('<\/?\w[^>]*>|&(|#)(\w)+;', '', c.value)
    break;
  outDir = os.path.join("out", "hackaday")
  outFile = os.path.join(outDir, filename + ".json")
  if os.path.isfile(outFile):
    print(filename + " already exists")
    continue
  with open(outFile, "w+") as f:
    json.dump(obj, f);
