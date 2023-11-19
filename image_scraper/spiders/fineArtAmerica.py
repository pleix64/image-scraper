import scrapy
from image_scraper.items import ImageScraperItem


class fineArtAmerica(scrapy.Spider):
    name = 'fineArtAmerica'
    allowed_domains = ['fineartamerica.com']
    start_urls = ['https://fineartamerica.com/art/digital+art/cyberpunk']
    

    def parse(self, response):
        item = ImageScraperItem()
        item['image_urls'] = response.css('a img.flowImage::attr(data-src)').getall()
        yield item
        
        next_page = response.css('a.buttonbottomnext::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            