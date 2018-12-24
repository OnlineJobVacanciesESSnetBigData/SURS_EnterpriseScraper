# Technical documentation for use of Python module job_spider_*number*

This document is a documentation file for the Python modules job_spider_*number*.py. We have created many such spiders for parallel use, trying to lessen the damage
if an error is encountered. Each module is comprised by a class definition of a crawler (JobSpider) with the names of "job_*number*" where *number* stand for the index
of each individual file. The class is used for crawling enterprise pages that and finding potential job advertisements. Each crawler crawls an enterprise domain to its
third level (determined by number of starting and additional slashes in the URL) and compares the addresses and tabs with a list of whitelisted words. If the words in 
the list are contained in the URL or a tab of a page, the page is labelled as a *potential job vacancy page*.

The spider loads the lists of whitelisted words for URLs and tabs and a list with all domains to be checked (*start_urls*). It uses 
manual settings for connections, specified in the attribute *custom_settings*.
It executes crawling using 4 specific methods defined according to the standard scrapy guidelines. The methods are:

* from_crawler: initiates the spider and starts the spider_startinfo before scraping and spider_endinfo after scraping.
* spider_startinfo: gives some basic info before scraping begins.
* scraper_endinfo: gives some basic info after finishing with scraping.
* parse: this method is the backbone of the scrapy structure and executes whatever need be done after the connection is established. In this case the URL and tabs are 
checked against whitelisted words. Some URLs are excluded (images, PDFs, videos, sound recordings, social network widgets and links, etc.). Relevant subpages' URLs 
are yielded for each domain. A .csv and log files of all yielded resutls is saved to the main project directory by using the command
```cmd
scrapy crawl jobs -o urls.csv -t csv --logfile log.txt
```

This module imports other modules and outside functions to work correctly:
* module **scrapy**
* function *signals* from **scrapy**
* fuction *Request* from **scrapy.http**
* class *JobItem* from **vacancies.items** ***(this is a project specific import)***
* functions *urlparse* and *urljoin* (from module **urllib.parse**)
* module **time**
* module **sys**
