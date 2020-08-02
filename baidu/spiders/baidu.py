import scrapy
from baidu.items import BaiduItem
from . import helper
import datetime


class BaiduSpider(scrapy.Spider):
    name = "baidu"

    def parse(self, response):  # forum parser
        print("Crawling page %d..." % self.cur_page)
        #print(response.xpath('//dt[contains(@alog-alias, "result-title-")]//a/@href').extract())
        for sel in response.xpath('//dt[contains(@alog-alias, "result-title-")]//a/@href'):
            url = sel.extract()
            bind_id = 0
            if not self.settings['QUESTION_ID']:
                # get all question

                pass
            else:
                bind_id = self.settings['QUESTION_ID']

            meta = {'bind_id': bind_id}
            yield scrapy.Request(url, callback=self.parse_comment,meta=meta)
            if self.cur_page == 0:
                break

        if self.cur_page >= 1:
            next_page = response.xpath('//a[@class="pager-next"]/@href')
            self.cur_page += 1
            if next_page:
                if self.cur_page <= self.end_page:
                    next_page = response.urljoin(next_page.extract_first())
                    print(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)

    def parse_comment(self, response):
        #print(response.url)

        meta = response.meta
        for sel in  response.xpath('//div[@id = "wgt-answers" or @id = "wgt-best"]//div[(contains(@id, "answer-") and contains(@class, "bd answer")) or (contains(@id, "best-answer-") and contains(@class, "wgt-best"))]'):
            username = sel.xpath('div[contains(@id,"wgt-replyer-all-")]//span[contains(@class,"wgt-replyer-all-uname")]/text()').extract_first()
            facephoto = sel.xpath('div[contains(@id,"wgt-replyer-all-")]//img[@class = "wgt-replyer-all-avatar"]/@src').extract_first()
            time = sel.xpath('div[contains(@id,"wgt-replyer-all-")]//span[@class = "wgt-replyer-all-time"]/text()').extract_first()
            content = sel.xpath('div[@class="line content-wrapper" or @class="bd answer"]/div[@class="line content"]/div[@accuse = "aContent"][last()]').extract_first()
            if time:
                time = time.replace('推荐于','')
                time = helper.strip_r_n(time)
                if helper.is_valid_date(time):
                    pass
                else:
                    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if content:
                #print(helper.parse_content(content))
                pass
            item = BaiduItem()
            item['facephoto'] = facephoto
            item['username'] = helper.strip_r_n(username)
            item['time'] = time
            item['content'] = helper.parse_content(content)
            item['post_id'] = meta['bind_id']
            if content:
                yield item  
                pass     
