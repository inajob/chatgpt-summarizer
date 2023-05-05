#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

jsonDir = os.path.join("out", "hackaday")
outFile = os.path.join("out", "hackaday.json")

files = os.listdir(jsonDir)
obj = {"files": files}

with open(outFile, "w+") as f:
  json.dump(obj, f);
