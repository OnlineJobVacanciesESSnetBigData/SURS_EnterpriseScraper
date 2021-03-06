# Technical documentation for use of Python module job_scraper

This document is a documentation file for the Python module **job_scraper.py**. The module is comprised by a class definition (*JobSpider*) with the name of "scraper". The class are used for scraping enterprise pages that were deemed potential job advertisements by the crawling process. The job of this spider is to collect the text contents on all sites and save it into a *.tab* file that is used for analysis and processing.

The spider has 5 specific methods defined according to the standard scrapy guidelines. The methods are:
* *from_crawler*: initiates the spider and starts the *spider_startinfo* before scraping and *spider_endinfo* after scraping.
* *spider_startinfo*: creates the return file which will be populated during the process and gives some basic info before scraping begins.
* *scraper_endinfo*: gives some basic info after finishing with scraping.
* *start_requests*: main method for running the scraper; feeds every page in list of potential vacancy pages to the spider.
* *parse*: this method is the backbone of the scrapy structure and executes whatever need actually be done after the connection is established.
           In this case the text on the page is collected and used for language detection and storage.

This module imports other modules and outside functions to work correctly:
* module **scrapy**
* function *signals* from **scrapy**
* function *Request* from **scrapy.http**
* function *BeautifulSoup* (from module **bs4**)
* functions *urlparse* and *urljoin* (from module **urllib.parse**)
* module **urllib.parse**
* function *detect* (from module **langdetect**)
* module **time**
* module **sys**
* module **datetime**

The output of the scraper is a .tab file in the scraping directory of the current period with 4 columns (delimited by the tab character) named Corpus_*year_month*.tab:
1. NumberJV (an empty/NA column that will be filled in the further process of estimation)
2. VacancySubpage
3. Date
4. Content

The second row holds information about the nature of the columns (c for class feature, i for feature to be ignored, m for the meta attribute, C for continuous-typed feature, D for discrete feature, S for string).
The third row specifies which columns are target and meta variables to be used in text mining. The microdata is written after 2 empty rows. This is a special file for use in the [Orange3 toolkit](https://orange.biolab.si/). 
