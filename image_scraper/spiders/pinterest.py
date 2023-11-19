import scrapy
from image_scraper.items import ImageScraperItem

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapy import Selector
from urllib.parse import urlparse
import time

class pinterest(scrapy.Spider):
    name = 'pinterest'
    allowed_domains = ['www.pinterest.com',
                       'www.pinterest.ca',
                       'i.pinimg.com']
    start_urls = ['https://www.pinterest.com/ArtTLG/sci-fi-art-cyberpunk-world/']
    
    def __init__(self):
        super().__init__()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") 
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)


    def parse(self, response):
        current_url = response.url
        #selector = self.scroll_down(current_url, 20)
        #source_pages = selector.css('a.Wk9.xQ4.CCY.czT::attr(href)').re('^/pin/[0-9]+/$')
        source_pages = self.scroll_down(current_url, 20)
        source_pages = list(set(source_pages))
        print('DEV: got {} source pages'.format(len(source_pages)))
        for page in source_pages:
            orig = urlparse(current_url)
            dest = urlparse(page)
            page = orig._replace(path=dest.path).geturl()
            yield response.follow(page, callback=self.extract_image)
            

    def extract_image(self, response):
        item = ImageScraperItem()
        item['image_urls'] = response.css('img.hCL::attr(src)').re('^https.+original.+')
        return item
    
    
    def scroll_down(self, url, scrolls):
        self.driver.get(url)
        time.sleep(3)
        
        source_pages = []
        for i in range(scrolls):           
            action = ActionChains(self.driver)
            action.scroll_by_amount(0, 2000)
            action.perform()
            time.sleep(3)
            sel_res_txt = self.driver.page_source
            selector = Selector(text=sel_res_txt)
            source_pages += selector.css('a.Wk9.xQ4.CCY.czT::attr(href)').re('^/pin/[0-9]+/$')
        
        return source_pages
    