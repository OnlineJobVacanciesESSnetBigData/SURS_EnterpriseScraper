#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=UTF-8  
import scrapy
from scrapy import signals
import urllib.parse
import time
import sys
from scrapy.http import Request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from langdetect import detect
import datetime

# We need that in order to force Slovenian pages instead of English pages.
# It happened at "http://www.g-gmi.si/gmiweb/" that only English pages were found and no Slovenian.
# from scrapy.conf import settings
# Settings.set(name, value, priority='cmdline')
# settings.overrides['DEFAULT_REQUEST_HEADERS'] = {'Accept':'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
#                                                  'Accept-Language':'sl','en':q=0.8,}

#######################################################################################################################
# We run the programme in the command line with this command:

#      scrapy crawl scraper --logfile scraper_log.txt


# We get three output files
#  1) .html files in foldier 'posnetki'
#  2) log.txt
#  3) a record in the Corpus_YEAR_MONTH.tab file

class JobSpider(scrapy.Spider):
    # Name of spider
    name = "scraper"

    # Manual middlewares
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {
        'vacancies.middlewares.VacanciesDownloaderMiddleware': 543}
    }
    # Counters
    slovenian = 0
    unsuccessful_loading = 0
    other = 0
    all = 0
    start_time = None
    # Year and month for directory names; this will become a map in the main scraping directory, where new files will be
    # created during the process of scraping.
    year_month = "YEAR_MONTH"
    # path za datoteke
    path = "PATH/TO/MAIN/SCRAPING/DIRECTORY/" + year_month

    # Reads the file of potential job ad pages. Since scrapy loads every method and attribute of every Spider object
    # before running them, this file does not yet exist before running the crawlers. This is why the list is defined
    # as empty if the file does not exist.
    try:
        with open(path + "/all_found_urls.txt", "r", encoding="utf8") as f:
            urllist = [url.strip() for url in f.readlines()][1:]
    except FileNotFoundError:
        urllist = []

    # Initiates the Spider and runs spider_startinfo and spider_endinfo at approriate times.
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(JobSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_startinfo, signals.spider_opened)
        crawler.signals.connect(spider.spider_endinfo, signals.spider_closed)
        return spider

    # Creates the return file which will be populated during the process and
    # gives some basic info before scraping begins.
    def spider_startinfo(self, spider):
        # Orange corpus.
        # If corpus does not yet exist, it is created, otherwise new rows are appended.
        try:
            with open(spider.path + "/Corpus_" + spider.year_month + ".tab", "rb") as ocorpus:
                ocorpus.read()
        except IOError:
            with open(spider.path + "/Corpus_" + spider.year_month + ".tab", "wb") as ocorpus:
                ocorpus.write(
                    b"NumberJV\tVacancySubpage\tDate\tContent\nc\ts\ts\ts\nclass\t\t\tinclude=True\n\n")
        print("Info about number of vacancy pages:\n\t-number of possible pages    %d\n"
              "\t-number of saved slovenian   %d\n\t-number of found other       %d\n"
              "\t-number of unsuccessful    %d\n\n"
              % (len(spider.urllist), spider.slovenian, spider.other, spider.unsuccessful_loading))
        # If the function start_requests has a 'yield Request' order and no parameter
        # 'meta={"dont_redirect": True}', the redirections are enabled.
        print("Redirections are ENABLED, number of checked pages might be higher than number of pages in list!\n\n")
        # If the function start_requests has a 'yield Request' order and no parameter
        # 'meta={"dont_redirect": True}', the redirections are enabled. For better clarity uncomment the below row.
        # print(""Redirections are DISABLED, number of saved pages might be lower than expected!\n\n")
        print(" Saved/Conn. Lang. Sum             URL")
        spider.start_time = time.time()

    # Gives some basic info after finishing with scraping.
    def spider_endinfo(self, spider):
        end_time = round(time.time() - spider.start_time)
        print("\nTime needed for scraping %dm:%ds" % (end_time//60, end_time - (end_time // 60) * 60))
        print("\nNumber of possible job vacancy pages    %d" % len(spider.urllist))
        print("Number of saved slovenian pages   %d" % spider.slovenian)
        print("Number of saved other pages       %d" % spider.other)
        print("Number of unsuccessful pages      %d" % spider.unsuccessful_loading)
        print("------------------------------------------------")
        print("Number of all traversed pages     %d" % (spider.slovenian + spider.other + spider.unsuccessful_loading))

    # Main method for running the scraper
    def start_requests(self):
        for url in self.urllist:
            self.all += 1
            try:
                yield scrapy.Request(url=url, callback=self.parse)
            except Exception as e:
                print("\tERROR when saving text " + url + ": " + str(e))
                with open(self.path+"/unsuccessful_loading.txt", "a+b") as neuspelo_nalaganje:
                    neuspelo_nalaganje.write(b"With code CON: " + url.encode("utf8") + b"\n")
                self.unsuccessful_loading += 1
                self.logger.info(e)
                continue

    # What is actually done after the connection is established. The text on the page is collected and used for
    # language detection and storage.
    def parse(self, response):
        orange_corpus = open(self.path + "/Corpus_" + self.year_month + ".tab", "a+b")
        # Control file for texts in other languages.
        other_langs = open(self.path + "/other_langs.txt", "a+b")

        soup = BeautifulSoup(response.body, "html.parser")
        # Rips out the text. This part was copied from the internet.
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # for line in lines:
        #    print line, "\n"
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        # drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Slovenian alphabet has characters that are not readable in all codecs, we change the most common ones to the
        # correct form
        text = text.replace('Ă„Ĺ¤', 'č')
        text = text.replace('ÄŤ', 'č')
        text = text.replace('ÄŚ', 'Č')

        text = text.replace('ÄąÄľ', 'ž')
        text = text.replace('Ĺľ', 'ž')
        text = text.replace('ÄąËť', 'Ž')
        text = text.replace('Ĺ˝', 'Ž')

        text = text.replace('Ĺˇ', 'š')
        text = text.replace('ÄąË‡', 'š')
        text = text.replace('Ĺ ', 'Š')

        text = text.replace('Â', '')
        text = text.replace('â€“', '')
        text = text.replace('â€™', '\'')
        text = text.replace('â', '')
        text = text.replace('™', '')
        text = text.replace('Ã', '')
        text = text.replace('¼', '')
        text = text.replace('Ã', '')
        text = text.replace('©', '')
        text = text.replace(':', ': ')
        text = text.replace('"', '')
        text = text.replace('»', ' ')
        text = text.replace('«', ' ')
        text = text.replace('    ', ' ')
        text = text.replace('   ', ' ')
        text = text.replace('  ', ' ')
        text = text.lower()
        text = text.replace('Ž', 'ž')
        text = text.replace('Š', 'š')
        text = text.replace('Č', 'č')

        # Our output file needs to have all tabulator spaces removed with normal spaces.
        text = text.replace('\t', ' ')

        # Detects lanugage.
        lang = ''
        if text != '':
            print("Detecting language on url %s...\r" % response.url[:160], end="")
            try:
                lang = detect(text)
                # lang_prob = detect_langs(text.decode('utf-8'))
            except Exception as e:
                print("Error when detecting lanugage on " + response.url + ": " + str(e))
                lang = 'language not detected due to error'
                # lang_prob = ['language not detected due to error']
            print(" " * 200, end="\r")

        # Saves slovenian pages to .tab file.
        if lang == 'sl':
            self.slovenian += 1
            orange_corpus.write(("?\t" + response.url + "\t" + datetime.datetime.now().strftime("%d.%m.%Y")
                                 + "\t" + text + "\n").encode("utf8"))
            print("Page %-*s %s   %-*d%s" % (len(str(len(self.urllist))) * 2 + 2,
                                              "%d/%d:" % (self.slovenian + self.other, self.all),
                                              lang, len(str(len(self.urllist))) + 3, self.slovenian, response.url))

        else:
            self.other += 1
            other_langs.write((response.url + "\n" + text + "\n\n\n").encode("utf8"))
            print("Page %-*s %s   %-*d%s" % (len(str(len(self.urllist))) * 2 + 2,
                                              "%d/%d:" % (self.slovenian + self.other, self.all),
                                              lang, len(str(len(self.urllist))) + 3, self.other, response.url))

        # Saves a record of the current HTML for later analysis and checks of content.
        url_record = response.url.replace(':', '-')
        url_record = url_record.replace('?', '-')
        url_record = url_record.replace('&', '-')
        url_record = url_record.replace('=', '-')
        url_record = url_record.replace('/', '-')
        if len(url_record) > 160:
            url_record = url_record[:160]
        with open("%s/records/%d  %s  %s.html" % (self.path, self.slovenian + self.other, lang, url_record), "wb")\
                as f:
            f.write(response.body)

        orange_corpus.close()
        other_langs.close()
        return
