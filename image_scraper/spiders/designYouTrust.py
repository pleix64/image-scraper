import scrapy
from image_scraper.items import ImageScraperItem


class designYouTrust(scrapy.Spider):
    name = 'designYouTrust'
    allowed_domains = ['designyoutrust.com']
    start_urls = ['https://designyoutrust.com/2018/05/neon-dystopia-the-superb-cyberpunk-digital-art-by-jonathan-plesel/']
    

    def parse(self, response):
        item = ImageScraperItem()
        item['image_urls'] = response.css('img::attr(data-srcset)').re('(?<=990w, ).+(?= 650w)')
        yield item
        
            