#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@文件        :config.py
#@说明        :[]
#@时间        :2020/07/29 10:11:57
#@作者        :lei.wang
#@版本        :1.0

import json
import os
import sys
import MySQLdb
import warnings
import time
import csv
from io import open

class config:
    config_path = 'config.json'
    config = None

    def __init__(self):
        with open(self.config_path, 'r', encoding='utf8') as f:
            self.config = json.loads(f.read())
            # loads后若有中文 为unicode
    def save(self):
        with open(self.config_path, 'wb') as f:
            s = json.dumps(self.config, indent=4, ensure_ascii=False).encode('utf8')
            f.write(s)

class log:
    log_path = 'spider.log'
    
    def __init__(self, question_name, dbname, begin_page):
        if not os.path.isfile(self.log_path):
            with open(self.log_path, 'wb') as f:
                row = ['start_time','end_time','elapsed_time','question_name','database_name','pages']
                s = '\t'.join(row) + '\n'
                if not isinstance(s, bytes):
                    s = s.encode('utf8')
                f.write(s)
        self.question_name = question_name
        self.dbname = dbname
        self.begin_page = begin_page
        self.start_time = time.time()
        
    def log(self, end_page):
        end_time = time.time()
        elapsed_time = '%.4g' % (end_time - self.start_time)
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time))
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
        question_name = self.question_name

        pages = '%d~%d'%(self.begin_page, end_page) if end_page >= self.begin_page else 'None'
        with open(self.log_path, 'ab') as f:
            row = [start_time, end_time, elapsed_time, question_name, self.dbname, pages]
            s = '\t'.join(row) + '\n'
            if not isinstance(s, bytes):
                s = s.encode('utf8')
            f.write(s)
        
        
def init_database(host, user, passwd, port, dbname):
    warnings.filterwarnings('ignore', message = ".*exists.*")  
    warnings.filterwarnings('ignore', message = ".*looks like a.*") 
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, port=port)
    tx = db.cursor()
    tx.execute('set names utf8mb4')
    tx.execute('create database if not exists `%s`default charset utf8mb4\
    default collate utf8mb4_general_ci;' % MySQLdb.escape_string(dbname).decode("utf8"))
    #要用斜引号不然报错
    #万恶的MySQLdb会自动加上单引号 结果导致错误
    db.select_db(dbname)
    tx.execute("create table if not exists comment(id BIGINT(12) UNSIGNED NOT NULL AUTO_INCREMENT,\
        author VARCHAR(30), facephoto VARCHAR(250), content TEXT, time DATETIME, post_id BIGINT(12), \
        PRIMARY KEY (id)) CHARSET=utf8mb4;")
    db.commit()
    db.close()