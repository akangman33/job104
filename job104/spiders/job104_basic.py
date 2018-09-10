# -*- coding: utf-8 -*-
import scrapy
import time


class Job104BasicSpider(scrapy.Spider):
    name = 'job104_basic'
    allowed_domains = ['104.com.tw']
    # start_urls = ['https://www.104.com.tw/']

    def __init__(self):
        self.keyword = ["python", "java", "javascript", "R", "C#"]
        self.page = 1
        self.url = "https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&area=6001001000&order=11&asc=0&page={}&mode=s&jobsource=2018indexpoc"
        self.count = 0

    def start_requests(self):
        for keyword in self.keyword:
            url = self.url.format(keyword, self.page)
            yield scrapy.Request(url=url, callback=self.parse, meta={'key': keyword, 'no': self.page}, dont_filter=True)

    def parse(self, response):
        detail_urls = response.xpath('.//div[@class="b-block__left"]/h2[@class="b-tit"]/a/@href').extract()
        # print(len(detail_urls), '******************************'*10)
        if len(detail_urls) > 0:
            for detail_url in detail_urls:
                detail_url = 'https:' + detail_url
                # print(detail_url)
                yield scrapy.Request(url=detail_url, callback=self.parse_info, dont_filter=True)
            # print(detail_url, '******************************')
            key = response.meta.get('key')
            no = response.meta.get('no')
            url = self.url.format(key, str(no+1))
            yield scrapy.Request(url=url, callback=self.parse, meta={'key': key, 'no': no+1}, dont_filter=True)
        else:
            pass

    def parse_info(self, response):
        self.count = self.count+1
        i = {}
        i['id'] = self.count
        i['job_name'] = response.xpath('.//div[@class="center"]/h1/text()').extract_first().replace('\r\n', '').replace(' ', '')
        i['company'] = response.xpath('.//div[@class="center"]/h1/span/a/text()').extract_first()
        i['salary'] = response.xpath('.//div[@class="content"]/dl/dd[2]/text()').extract_first()
        i['address'] = response.xpath('.//div[@class="content"]/dl/dd[4]/text()').extract_first().replace('\r\n\t', '').replace(' ', '')
        i['job_url'] = response.url
        # print(i)
        return i