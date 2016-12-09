# -*- coding:gb2312 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from soufang.items import SoufangItem
from scrapy.http import Request
import threading


class SoufangSpider(CrawlSpider):

    name = 'soufang'
    allowed_domains = ['fang.com']
    #start_urls = ["http://newhouse.fang.com/house/s/"]
    start_urls = ["http://newhouse.fang.com/house/s/b92/"]
    q = threading.Lock()
    page_file_name_lock = threading.Lock()
    page_file_name = 0
    page_num = 0
    #rules = [Rule(LinkExtractor(allow='http://[a-z]+\.fang\.com/?ctm=1'), 'parse_bj', follow=True)]


    def parse(self, response):
        sel = Selector(response)
        """
        filename = "body"
        with open(filename, "wb") as f:
            f.write(response.body)
        """
        urls = sel.xpath('//li/div/div/a/@href').extract()
        print "urls", urls, len(urls)


        for url in urls:
            print url
            try:
                request = Request(url, callback=self.parse_detail)
                self.q.acquire()
                self.page_num += 1
                request.meta['num'] = page_num
                self.q.release()
                yield request
            except Exception as e:
                log_text = "ERROR:" + url

        try:
            url = sel.xpath('//div[@class="page"]/ul/li[@class="fr"]/a/@href').extract()
            print "$" * 30
            print url
            print "$" * 30

            """
            request = Request(url, callback=self.parse)
            yield request
            """
        except Exception as e:
            log_text = "ERROR:" + url



    def is_uchar(self, uchar):
        """判断一个unicode是否是中文"""
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        """判断一个unicode是否是数字"""
        if uchar >= u'\u0030' and uchar <= u'\u0039':
            return True
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
            return True

        return False


    def parse_detail(self, response):

        sel = Selector(response)
        soufang = SoufangItem()
        page_num = response.meta['num']
        filename = "./page/peking" + str(page_num)

        soufang["url"] = response.url
        print "#" * 30
        print response.url
        print page_num
        print "#" * 30

       # print response.body
       # print "$" * 30

        title = sel.xpath('//div[@id="daohang"]/div/dl/dd/div/h1/a/text()').extract()
        final_title = ''
        if len(title) == 0:
            title = sel.xpath('//title/text()').extract()[0]
            title = title.strip().split("-")
            if len(title) != 0:
                try:
                    #print title[0].strip()
                    title = title[0].strip()
                    tmp = []
                    for word in title:
                        if self.is_uchar(word) == True:
                            tmp.append(word)
                        else:
                            tmp.append('-')

                    title = ''.join(tmp)
                    final_title = title
                except Exception as e:
                    print e

        else:
            try:
                #print title[0].strip()
                title = title[0].strip()
                tmp = []
                for word in title:
                    if self.is_uchar(word) == True:
                        tmp.append(word)
                    else:
                        tmp.append('-')

                title = ''.join(tmp)
                final_title = title
            except Exception as e:
                print e

        soufang['residence'] = final_title
        print final_title
        """
        with open(filename, "wb") as f:
            f.write(response.body)
        """

    def parse_bj(self, response):

        soufang = SoufangItem()
        soufang["url"] = response.url
        """
        soufang["url"] = response.url.split("/").split(".")[0]

        filename = response.url
        with open(filename, 'wb') as f:
            f.write(response.body)
        """
        """
        for item in response.xpath("//div[@class='nlc_details']"):

            soufang['position'] =
            soufang['avg_money'] =
            soufang['residence'] =

            soufang['residence'] = item.xpath("a/text()")
        """

        return soufang