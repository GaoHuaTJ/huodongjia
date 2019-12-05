import scrapy

from huodongjia.items import HuodongjiaItem
class HuodongjiaSpuder(scrapy.Spider):
    name = "huodongjia"
    start_urls=["https://www.huodongjia.com/business/17/overview/page-1"]
    base_url="https://www.huodongjia.com/business/17/overview/"
    offset=0
    def parse(self, response):
        item=HuodongjiaItem()
        item["meeting"]=response.xpath("//*[@id=\"event-infos-table\"]/tbody/tr/td[1]/a/text()").extract()
        item["date"]=response.xpath("//*[@id=\"event-infos-table\"]/tbody/tr/@time").extract()
        item["industry"]=response.xpath("//*[@id=\"event-infos-table\"]/tbody/tr/td[3]/text()").extract()
        item["place"]=response.xpath("//*[@id=\"event-infos-table\"]/tbody/tr/td[4]/text()").extract()
        yield item
        #假设有1000页
        if self.offset<1000:
            self.offset+=1
            url=self.base_url+"page-{0}".format(str(self.offset))
            print(url)
            yield scrapy.Request(url,callback=self.parse)




