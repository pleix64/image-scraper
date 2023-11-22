# Image Scraper

This image scraper was built on Oct, 2022, to scrape data (images) used to train the [Cyclegan Cyberpunk](https://github.com/pleix64/cyclegan-cyberpunk) deep learning network. 

The scraper is based on the Scrapy framework, and using Selenium for automatically browsing some dynamic webpages that otherwise do not load sufficient content. 
## Installation
(to be added later)
## Usage
Change directory to the Image Scraper project root directory, 
```
cd /path/to/image_scraper
```
Create new directory for storing images if you haven't done so, 
```
mkdir data
```
or name it as whatever you like, but you have to change the value of variable `IMAGES_STORE` in `image_scraper/settings.py` accordingly. 
Activate the virtual environment, 
```
pipenv shell
```
To scrape images, run a spider:
```
scrapy crawl [spiderName]
```
