#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @文件        :pipelines.py
# @说明        :[更新通道]
# @时间        :2020/07/29 14:40:28
# @作者        :lei.wang
# @版本        :1.0

from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from six.moves.urllib.parse import quote
from baidu.items import BaiduItem


class BaiduPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        dbname = settings['MYSQL_DBNAME']
        question_name = settings['QUESTION_NAME']
        if not dbname.strip():
            raise ValueError("No database name!")
        if not question_name.strip():
            raise ValueError("No question name!")

        self.settings = settings
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host=settings['MYSQL_HOST'],
                                            db=settings['MYSQL_DBNAME'],
                                            user=settings['MYSQL_USER'],
                                            passwd=settings['MYSQL_PASSWD'],
                                            port=settings['MYSQL_PORT'],
                                            charset='utf8mb4',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            init_command='set foreign_key_checks=0'  # 异步容易冲突
                                            )

    def open_spider(self, spider):
        spider.cur_page = begin_page = self.settings['BEGIN_PAGE']
        spider.end_page = self.settings['END_PAGE']
        pn = 0
        if begin_page != 0:
            pn = 10 * (begin_page - 1)
        spider.filter = self.settings['FILTER']
        question_name = self.settings['QUESTION_NAME']
        if not isinstance(question_name, bytes):
            question_name = question_name.encode('utf8')
        base_url = "http://zhidao.baidu.com/search?word=%s&pn=%d&c=1"
        if question_name == 'all':
            pass
        else:
            spider.start_urls = [base_url % (quote(question_name), pn)]

    def close_spider(self, spider):
        self.settings['SIMPLE_LOG'].log(spider.cur_page - 1)

    def process_item(self, item, spider):
        _conditional_insert = {
            'comment': self.insert_comment
        }
        query = self.dbpool.runInteraction(
            _conditional_insert[item.name], item)
        query.addErrback(self._handle_error, item, spider)
        return item

    def insert_comment(self, tx, item):
        tx.execute('set names utf8mb4')
        sql = "replace into comment (`author`,`facephoto`,`content`,`time`,`post_id`) values (%s, %s, %s, %s, %s)"
        params = (item["username"], item['facephoto'], item['content'],
                  item['time'], item['post_id'])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, fail, item, spider):
        spider.logger.error('Insert to database error: %s \
        when dealing with item: %s' % (fail, item))
