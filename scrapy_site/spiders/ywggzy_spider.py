# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy
from scrapy_site.items import SiteItem
from scrapy_site.utils import date


# 义务市公共资源交易中心
class YwggzySpider(scrapy.Spider):
    name = "ywggzy"
    allowed_domains = ["ggfw.ywjypt.yw.gov.cn"]
    start_urls = [
        "http://ggfw.ywjypt.yw.gov.cn/jyxx/070001/070001001/list3gc.html"
    ]

    # def __init__(self, name=None, **kwargs):
    #     self.iipage = 1
    #     super(YwggzySpider, self).__init__(name, **kwargs)

    def parse(self, response):
        detail = response.xpath('//ul[@class="ewb-nbd-items gclist"]//li')
        print("--------------begin -------------- yw")
        pubtime = ""
        for temp in detail:
            item = SiteItem()
            item['title'] = temp.xpath('a/text()').extract_first().strip()
            item['link'] = "http://ggfw.ywjypt.yw.gov.cn" + temp.xpath('a/@href').extract_first().strip()
            item['pubtime'] = temp.xpath('span[@class="ewb-date r"]/text()').extract_first().strip()
            pubtime = item['pubtime']
            yield item

        if pubtime == date.get_curdate():
            # 得到下一页
            print("-----------------翻页-----------------")
            page = response.xpath('//span[@id="index"]/text()').extract_first()
            cur_page_num = page.split('/')[0]
            total_page_num = page.split('/')[1]
            print("page , cur_page, totalNUm  " + page + ";" + cur_page_num + ";" + total_page_num )
            index = int(cur_page_num) + 1
            print("\n page num = " + str(index))
            # if int(self.iipage) <= int(total_pagenum):
            if int(index) <= int(total_page_num):
                next_page_href = "http://ggfw.ywjypt.yw.gov.cn" + "/jyxx/070001/070001001/" + str(index) + ".html"
                print("page link is " + next_page_href)
                yield scrapy.FormRequest(next_page_href, callback=self.parse)
