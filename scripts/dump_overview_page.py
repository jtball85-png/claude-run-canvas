# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from push_course import api_get

page = api_get("/courses/456/pages/business-math-welcome")
body = page["body"]
idx = body.find(">Day 9<")
print(repr(body[idx-250:idx+900]))
