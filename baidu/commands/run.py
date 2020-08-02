#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @文件        :run.py
# @说明        :[]
# @时间        :2020/07/29 09:43:28
# @作者        :lei.wang
# @版本        :1.0

import scrapy.commands.crawl as crawl
from scrapy.exceptions import UsageError
from scrapy.commands import ScrapyCommand
import config
import filter


class Command(crawl.Command):
    def syntax(self):
        return "<question_name> <bind_id>"

    def short_desc(self):
        return "Crawl baidu"

    def long_desc(self):
        return "Crawl baidu knows data to a MySQL database."

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-p", "--pages", nargs=2, type="int", dest="pages", default=[],
                          help="set the range of pages you want to crawl")
        parser.add_option("-f", "--filter", type="str", dest="filter", default="",
                          help='set function name in "filter.py" to filter baidu knows')
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")

    def set_pages(self, pages):
        if len(pages) == 0:
            begin_page = 0
            end_page = 0
        else:
            begin_page = pages[0]
            end_page = pages[1]
            if begin_page <= 0:
                raise UsageError(
                    "The number of begin page must not be less than 1!")
            if begin_page > end_page:
                raise UsageError(
                    "The number of end page must not be less than that of begin page!")
        self.settings.set('BEGIN_PAGE', begin_page, priority='cmdline')
        self.settings.set('END_PAGE', end_page, priority='cmdline')

    def run(self, args, opts):
        self.set_pages(opts.pages)
        if opts.filter:
            try:
                opts.filter = eval('filter.' + opts.filter)
            except:
                raise UsageError("Invalid filter function name!")
        self.settings.set("FILTER", opts.filter)
        cfg = config.config()
        if len(args) >= 3:
            raise UsageError("Too many arguments!")
        for i in range(len(args)):
            if isinstance(args[i], bytes):
                args[i] = args[i].decode("utf8")

        if not 'MYSQL_PORT' in cfg.config.keys():
            cfg.config['MYSQL_PORT'] = 3306
        
        self.settings.set('MYSQL_HOST', cfg.config['MYSQL_HOST'])
        self.settings.set('MYSQL_USER', cfg.config['MYSQL_USER'])
        self.settings.set('MYSQL_PASSWD', cfg.config['MYSQL_PASSWD'])
        self.settings.set('MYSQL_PORT', cfg.config['MYSQL_PORT'])
        self.settings.set('QUESTION_TABLE', cfg.config['QUESTION_TABLE'])
        self.settings.set('QUESTION_INDEX_ID', cfg.config['QUESTION_INDEX_ID'])
        self.settings.set('QUESTION_FIND_FIELD_NAME', cfg.config['QUESTION_FIND_FIELD_NAME'])
        question_name = ''
        if len(args) >= 1:
            question_name = args[0]
            if question_name != 'all':
                if len(args) < 2:
                    raise UsageError("must bind id!")
        self.settings.set('QUESTION_NAME', question_name)
        index_id = 0
        if len(args) >= 2:
            index_id = args[1]
        self.settings.set('QUESTION_ID',index_id)
        
        dbname = cfg.config['MYSQL_DBNAME']
        if not dbname:
            raise UsageError("Please input database name!")

        self.settings.set('BAIDU_NAME', question_name, priority='cmdline')
        self.settings.set('MYSQL_DBNAME', dbname, priority='cmdline')
        config.init_database(cfg.config['MYSQL_HOST'], cfg.config['MYSQL_USER'],
                             cfg.config['MYSQL_PASSWD'], cfg.config['MYSQL_PORT'], dbname)
        log = config.log(question_name, dbname, self.settings['BEGIN_PAGE'])
        self.settings.set('SIMPLE_LOG', log)
        self.crawler_process.crawl('baidu', **opts.spargs)
        self.crawler_process.start()

        cfg.save()
