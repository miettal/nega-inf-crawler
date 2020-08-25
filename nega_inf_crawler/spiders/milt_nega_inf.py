# -*- coding: utf-8 -*-
import scrapy


class MiltNegaInfSpider(scrapy.Spider):
    name = 'milt-nega-inf'
    allowed_domains = ['www.mlit.go.jp']
    start_urls = ['https://www.mlit.go.jp/nega-inf/']

    def parse(self, response):  # index
        for jigyoubunya in response.css('a::attr("href")').re('\\./cgi-bin/searchmenu\\.cgi\\?jigyoubunya=(.+)'):
            url = 'https://www.mlit.go.jp/nega-inf/cgi-bin/fsearch.cgi'
            yield scrapy.http.FormRequest(
                url=url,
                formdata={'jigyoubunya': jigyoubunya},
                callback=self.parse_list,
            )

    def parse_list(self, response):
        table = response.css('table')[1]
        for (i, tr) in enumerate(table.css('tr')):
            if i == 0:
                continue
            date = tr.css('td::text').extract()[0]
            jigyousya = tr.css('td::text').extract()[1]
            syobunsyurui = tr.css('td::text').extract()[2]
            try:
                summary_link = tr.css('td')[4].css('input::attr("onclick")').re('window\\.open\\(\'([^\']+)\'.+\\)')[0]
                summary_link = response.urljoin(summary_link)
            except IndexError:
                summary_link = None
            try:
                detail_link = tr.css('td')[5].css('input::attr("onclick")').re('window\\.open\\(\'([^\']+)\'.+\\)')[0]
                detail_link = response.urljoin(detail_link)
            except IndexError:
                detail_link = None
            yield {
                'date': date,
                'jigyousya': jigyousya,
                'syobunsyurui': syobunsyurui,
                'summary_link': summary_link,
                'detail_link': detail_link,
            }
