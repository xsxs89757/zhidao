#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@文件        :items.py
#@说明        :[序列化]
#@时间        :2020/07/28 17:58:09
#@作者        :lei.wang
#@版本        :1.0

from scrapy import Item,Field


class BaiduItem(Item):
    name = 'comment'
    facephoto = Field() #头像
    username = Field() #用户名
    time = Field() #时间
    content = Field() #内容
    post_id = Field() # 关联id
