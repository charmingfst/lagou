# -*- coding: utf-8 -*-
# coding=utf-8
import json

import scrapy


class PositionSpider(scrapy.Spider):
    name = "position"
    # allowed_domains = ["lagou.com/zhaopin/"]
    start_urls = [
        'https://www.lagou.com/jobs/positionAjax.json']

    totalPageCount = 0
    curpage = 1

    city = u'杭州'

    district = u'西湖区'

    url = 'https://www.lagou.com/jobs/positionAjax.json'

    # 设置下载延时
    # download_delay = 10

    def start_requests(self):
        # for num in xrange(1, 3):
        #     form_data = {'pn': str(num), 'city': self.city, 'district': self.district}
        #     headers = {
        #         'Host': 'www.jycinema.com',
        #         'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        #     }
        #     yield scrapy.FormRequest(self.url, formdata=form_data, callback=self.parse)
        # requests = []
        # for num in xrange(1, 5):
        #     requests.append(scrapy.FormRequest(self.url, method='post', formdata={'pn': str(num), 'city': self.city,'district':self.district},  callback=self.parse))
        # return requests
        return [scrapy.FormRequest(self.url,formdata={'pn': str(self.curpage), 'city': self.city,'district':self.district},
                                   callback=self.parse)]

    def parse(self, response):
        # print response.body
        print response.body.decode('utf-8')
        print str(self.curpage) + "page"

        jdict = json.loads(response.body)
        jcontent = jdict['content']
        jposresult = jcontent["positionResult"]
        pageSize = jcontent["pageSize"]
        jresult = jposresult["result"]
        self.totalPageCount = jposresult['totalCount'] / pageSize + 1;
        for each in jresult:
            print each['city']
            print each['companyFullName']
            print each['companySize']
            print each['positionName']
            print each['secondType']
            print each['salary']
            print ''

        if self.curpage <= self.totalPageCount:
            self.curpage += 1
            yield scrapy.http.FormRequest(self.url, formdata={'pn': str(self.curpage), 'city': self.city,'district': self.district},
                                          callback=self.parse)
