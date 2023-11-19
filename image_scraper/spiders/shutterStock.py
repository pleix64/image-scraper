import scrapy
from image_scraper.items import ImageScraperItem

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapy import Selector
from urllib.parse import urlparse
import time

class shutterStock(scrapy.Spider):
    name = 'shutterStock'
    allowed_domains = ['shutterstock.com']
    #start_urls = ['https://www.shutterstock.com/search/japanese-street-view?image_type=photo']
    start_urls = ['https://www.shutterstock.com/search/living-room-bedroom?image_type=photo']
    
    def __init__(self):
        super().__init__()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") 
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.counter = 0


    def parse(self, response):
        current_url = response.url
        response, next_page = self.scroll_to_bottom(current_url)
        source_pages = response.css('div a::attr(href)').getall()
        source_pages = [x for x in source_pages if 'image-photo' in x]
        for page in source_pages:
            orig = urlparse(current_url)
            dest = urlparse(page)
            page = orig._replace(path=dest.path, query='').geturl()
            yield response.follow(page, callback=self.extract_image)
        
        if next_page is not None and self.counter < 21:
            orig = urlparse(current_url)
            dest = urlparse(next_page)
            next_page = orig._replace(query=dest.query).geturl()
            yield scrapy.Request(next_page, callback=self.parse)
            

    def extract_image(self, response):
        targets = response.css('picture source::attr(srcset)').getall()
        targets = [x for x in targets if '600w' in x]
        
        item = ImageScraperItem()
        item['image_urls'] = []
        item['image_urls'].append(targets[0])
        return item
    
    
    def scroll_to_bottom(self, url):
        self.driver.get(url)
        selector = None
        next_button = None
        next_page = None

        while True: 
            sel_res_txt = self.driver.page_source
            selector = Selector(text=sel_res_txt)
            next_button = selector.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mui-isiaxn-button", " " ))]')
            next_text = next_button.css("::text").get() 
            next_page = next_button.css("::attr(href)").get()
            if next_text == 'Next':
                break
            action = ActionChains(self.driver)
            action.scroll_by_amount(0, 2000)
            action.perform()
            time.sleep(3)
        print("DEV: found next page path: {}".format(next_page))
        
        self.counter += 1
        return selector.response, next_page
    