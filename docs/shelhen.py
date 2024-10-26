# -*- encoding: utf-8 -*-
"""
--------------------------------------------------------
@File: shelhen.py
@Project: flower-shop 
@Time: 2024/10/27   04:07
@Author: shelhen
@Email: shelhen@163.com
@Software: PyCharm 
--------------------------------------------------------
# @Brief:
"""
import json

with open('./areas.json', 'r',encoding='utf8') as f:
    areas = json.load(f)

for area in areas:
    print(area)
# print(areas)