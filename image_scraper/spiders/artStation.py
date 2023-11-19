import scrapy
from image_scraper.items import ImageScraperItem

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapy import Selector
import time

class artStation(scrapy.Spider):
    # This spider is blocked by the site and returned 403 status
    # all pieces are tested on shell and working OK. 
    # But when running as 'scrapy crawl artStation' it's blocked to run parse().
    name = 'artStation'
    allowed_domains = ['www.artstation.com']
    start_urls = ['https://www.artstation.com/search?sort_by=relevance&query=cyberpunk']
    
    def __init__(self):
        super().__init__()
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless") 
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)


    def parse(self, response):
        current_url = response.url
        print('DEV: before scroll down called.')
        selector = self.scroll_down(current_url, 20)
        print('DEV: after scroll down called.')
        source_pages = selector.css('a.gallery-grid-link::attr(href)').getall()
        for page in source_pages:
            yield response.follow(page, callback=self.extract_image)
            

    def extract_image(self, response):
        self.driver.get(response.url)
        time.sleep(1)
        selector = Selector(text=self.driver.page_source)
        item = ImageScraperItem()
        item['image_urls'] = selector.css('a.btn::attr(href)').re('^https(?:(?!dl=1).)+$')
        return item
    
    
    def scroll_down(self, url, scrolls):
        print('DEV: getting url...')
        self.driver.get(url)
        time.sleep(1)

        for i in range(scrolls):
#            sel_res_txt = self.driver.page_source
#            selector = Selector(text=sel_res_txt)

#            next_button = selector.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mui-isiaxn-button", " " ))]')
#            next_text = next_button.css("::text").get() 
#            next_page = next_button.css("::attr(href)").get()
           
            action = ActionChains(self.driver)
            action.scroll_by_amount(0, 2000)
            action.perform()
            time.sleep(3)
        sel_res_txt = self.driver.page_source
        selector = Selector(text=sel_res_txt)
        return selector
    