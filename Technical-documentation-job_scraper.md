# Technical documentation for use of Python module job_scraper

This document is a documentation file for the Python module **job_scraper.py**. The module is comprised by a class definition (*JobSpider*) with the name of "scraper". 
The functions are used for scraping enterprise pages that were deemed potential job advertisements by the crawling process. The job of this spider is to collect the 
text contents on all sites and save it into a *.tab* file that is used for analysis and processing.

The spider has 5 specific methods defined according to the standard scrapy guidelines. The methods are:
*	*from_crawler*: initiates the spider and starts the *spider_startinfo* before scraping and *spider_endinfo* after scraping.
*	*spider_startinfo*: creates the return file which will be populated during the process and gives some basic info before scraping begins.
*	*scraper_endinfo*: gives some basic info after finishing with scraping.
* *start_requests*: main method for running the scraper; feeds every page in list of potential vacancy pages to the spider.
* *parse*: this method is the backbone of the scrapy structure and executes whatever need actually be done after the connection is established.
           In this case the text on the page is collected and used for language detection and storage.

Scrapers run in multithread mode on 3 threads. This is because we have an agreement with job portals to only use three agents at once. A working log is written at the same time.
This module imports other modules and outside functions to work correctly:
* module **scrapy**
* function *signals* from **scrapy**
* function *Request* from **scrapy.http*
*	function *BeautifulSoup* (from module **bs4**)
*	functions *urlparse* and *urljoin* (from module **urllib.parse**)
* module **urllib.parse**
* function *detect* (from module **langdetect**)
*	module **time**
*	module **sys**
* module **datetime**
