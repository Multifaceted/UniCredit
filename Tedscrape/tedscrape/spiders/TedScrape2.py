# -*- coding: utf-8 -*-
import scrapy


class TedscrapeSpider(scrapy.Spider):
    allowed_domains = ['ted.com']
    start_urls = ['https://www.ted.com/talks?language=en&sort=newest']

    def parse(self, response):
        for element in response.xpath('//div[@class="m3"]'):
            yield {
                    "speaker": element.xpath('.//h4[@class = "h12 talk-link__speaker"]/text()').extract_first(),
                    "title": element.xpath('.//h4[@class = "h12 talk-link__speaker"]/following-sibling::h4/a/text()').extract_first(),
                    "link": response.urljoin(element.xpath('.//h4[@class = "h12 talk-link__speaker"]/following-sibling::h4/a/@href').extract_first()),
                    "date": element.xpath('.//span[@class = "meta__val"]/text()').extract_first()
                    
                    }
            
        next_page = response.xpath('//a[@class="pagination__next pagination__flipper pagination__link"]/@href').extract_first()
        
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url = next_page_link, callback = self.parse)
    
#    def parse_speech(self, response):