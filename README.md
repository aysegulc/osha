
Osha Scraping Project
-------------------------

This scrapy project illustrates a recursive spider.

Starting with the first page, spider recursively requests the link in the page and save html body as a text file. Recursion depth is limited via 'DEPTH_LIMIT' parameter in the settings file.


```bash
# Scraped pages are saved as txt files into /texts directory
scrapy crawl osha
```
