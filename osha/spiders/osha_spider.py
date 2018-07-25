# -*- coding: utf-8 -*-
import scrapy
import os


def make_directory(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


class OshaSpider(scrapy.Spider):
    name = 'osha'
    allowed_domains = ['osha.gov']
    # start_urls = ['https://www.osha.gov/pls/imis/sic_manual.html']

    def start_requests(self):
        make_directory('texts/')
        request = scrapy.Request("https://www.osha.gov/pls/imis/sic_manual.html", self.parse)
        request.meta['title'] = 'SIC_Division_Structure.txt'
        yield request

    def parse(self, response):
        title = response.meta['title']
        text_list = response.xpath('//*[@id="maincontain"]//text()').extract()

        with open('texts/' + title, 'w') as f:
            # f.write(''.join(text_list).strip().encode('utf-8'))
            f.write(''.join(text_list).strip().replace('\n', '\\n').replace('\r', '\\r').encode('utf-8'))

        for link in response.xpath('//a[contains(@href,"sic_manual.display")]'):
            href = link.xpath('./@href').extract_first(default='')
            # print(response.urljoin(href))
            request = scrapy.Request(response.urljoin(href), self.parse)
            sub_title = link.xpath('./@title').extract_first(default='').strip().replace(':', '').replace(',', '').replace(' ', '_')
            if not sub_title:
                sub_title = link.xpath('./text()').extract_first(default='').strip().replace(':', '').replace(',', '').replace(' ', '_')
            request.meta['title'] = sub_title + '.txt'
            yield request
