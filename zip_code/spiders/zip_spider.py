
import scrapy
import urllib

from zip_code.items import ZipCodeItem, CountyItem, StateItem

class ZipSpider(scrapy.Spider):
    name = "zip_code"
    allowed_domains = ["melissadata.com"]
    start_urls = ["https://www.melissadata.com/lookups/countyzip.asp"]

    def parse(self, response):
        for href in response.xpath('//option[@value]'):
            link = href.xpath('./@value').extract()[0]
            state = urllib.quote_plus(href.xpath('./text()').extract()[0])
            #state = urllib.quote_plus(href.extract())
            yield scrapy.Request('https://www.melissadata.com/lookups/countyzip.asp?state=' + link, callback=self.parse_counties)

    def parse_counties(self, response):
        for href in response.xpath('//option[@value]'):
            link = href.xpath('./@value').extract()[0]
            county = urllib.quote_plus(href.xpath('./text()').extract()[0])
            #fips = href.extract()
            yield scrapy.Request('https://www.melissadata.com/lookups/countyzip.asp?fips=' + link, callback=self.parse_zip_codes)

    def parse_zip_codes(self, response):
        # this function parses all zip codes for a given county
        table = response.xpath('//table[@class="Tableresultborder" and @width="650"]')
        rows = table.xpath('//*[@bgcolor]')
        for sel in rows:
            item = ZipCodeItem()
            item['zip_code'] = sel.xpath('td/a[contains(@href,"ZipCityPhone")]/text()').extract()[0]
            tds = sel.xpath('td[not(@align="center")]/text()').extract()
            item['city'] = tds[0].strip()
            item['zip_percent'] = float(tds[1])
            yield item