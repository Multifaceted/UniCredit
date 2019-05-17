# -*- coding: utf-8 -*-
import scrapy


class TedscrapeSpider(scrapy.Spider):
    name = 'TedScrape'
    allowed_domains = ['ted.com']
    start_urls = ['https://www.ted.com/talks?language=en&sort=newest']

    def parse(self, response):
        
        for element in response.xpath('//div[@class="m3"]'):
            talk_link = response.urljoin(element.xpath('.//h4[@class = "h12 talk-link__speaker"]/following-sibling::h4/a/@href').extract_first())
            title = element.xpath('.//h4[@class = "h12 talk-link__speaker"]/following-sibling::h4/a/text()').extract_first()
            date = element.xpath('.//span[@class = "meta__val"]/text()').extract_first()
            yield scrapy.Request(url = talk_link, callback = self.parse_talk, meta = {"title": title,
                                                                                      "date": date})
                                 
        next_page = response.xpath('//a[@class="pagination__next pagination__flipper pagination__link"]/@href').extract_first()
        
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url = next_page_link, callback = self.parse)
    
    def parse_talk(self, response):
        import time
        import re
        
        time.sleep(1)
        speaker = response.xpath('//meta[@name="author"]/@content').extract_first()
        talk_id = response.xpath('//div[@id="main-nav-slideouts"]/following::script[2]/text()').extract_first()
        talk_id = re.sub("[^0-9]", " ", talk_id.split(', ')[-1]).strip()
        tags = response.xpath('//meta[@property="og:video:tag"]/@content').extract()
        script_url = "https://www.ted.com/talks/" + talk_id + "/transcript.json"
        yield scrapy.Request(url = script_url, callback = self.parse_script, meta = {"speaker": speaker,
                                                                                     "title": response.meta["title"],
                                                                                     "date": response.meta["date"],
                                                                                     "talk_id": talk_id,
                                                                                     "tags": tags})
        
    def parse_script(self, response):
        yield {"speaker": response.meta["speaker"],
               "title": response.meta["title"],
               "date": response.meta["date"],
               "talk_id": response.meta["talk_id"],
               "tags": response.meta["tags"],
               "text": response.body}