# Image Scraper

This image scraper was built on Oct, 2022, to scrape data (images) used to train the [Cyclegan Cyberpunk](https://github.com/pleix64/cyclegan-cyberpunk) deep learning network. 

The scraper is based on the [Scrapy](https://docs.scrapy.org/en/latest/index.html) framework, and using [Selenium](https://www.selenium.dev/documentation/) for automatically browsing some dynamic webpages that otherwise do not load sufficient content. 
## Installation
Download the code, 
```
git clone git@github.com:pleix64/image-scraper.git
```
Go to the project directory, 
```
cd image_scraper
```
Install the dependencies,
```
pipenv install
```
## Usage
In the project directory, activate the virtual environment, 
```
pipenv shell
```
To scrape images, run a spider:
```
scrapy crawl [spiderName]
```
Quit the virtual environment when you've done scraping, 
```
deactivate
```
