#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=UTF-8  
import scrapy, time, sys
from scrapy import signals
from scrapy.http import Request
from urllib.parse import urlparse, urljoin
from vacancies.items import JobItem

# We need that in order to force Slovenian pages instead of English pages. It happened at "http://www.g-gmi.si/gmiweb/"
# that only English pages were found and no Slovenian.
from scrapy.conf import settings

# We run the program in the command line with this command:

#      scrapy crawl jobs -o urls.csv -t csv --logfile log.txt


# We get two output files
#  1) urls.csv
#  2) log.txt

# Url whitelist.
with open("PATH/TO/SOME/DIRECTORY/url_whitelist.txt", "r+", encoding="latin1") as kw:
    url_whitelist = kw.read().replace('\n', '').split(",")
url_whitelist = list(map(str.strip, url_whitelist))

# Tab whitelist.
# We need to replace character the same way as in detector.
with open("PATH/TO/SOME/DIRECTORY/tab_whitelist.txt", "r+", encoding="latin1") as kw:
    tab_whitelist = kw.read()
tab_whitelist = tab_whitelist.replace('Ŕ', 'č')
tab_whitelist = tab_whitelist.replace('╚', 'č')
tab_whitelist = tab_whitelist.replace('Ő', 'š')
tab_whitelist = tab_whitelist.replace('Ü', 'š')
tab_whitelist = tab_whitelist.replace('Ä', 'ž')
tab_whitelist = tab_whitelist.replace('×', 'ž')
tab_whitelist = tab_whitelist.replace('\n', '').split(",")
tab_whitelist = list(map(str.strip, tab_whitelist))

# Look for occupations in url.
"""with open("PATH/TO/SOME/DIRECTORY/occupations_url.txt", "r+", encoding="utf8") as occ_url:
    occupations_url = occ_url.read().replace('\n', '').split(",")
occupations_url = map(str.strip, occupations_url)"""

# Look for occupations in tab.
# We need to replace character the same way as in detector.
"""with open("PATH/TO/SOME/DIRECTORY/occupations_url.txt", "r+", encoding="utf8") as occ_url:
    occupations_tab = occ_tab.read()
occupations_tab = occupations_tab.replace('Ŕ', 'č')
occupations_tab = occupations_tab.replace('╚', 'č')
occupations_tab = occupations_tab.replace('Ő', 'š')
occupations_tab = occupations_tab.replace('Ü', 'š')
occupations_tab = occupations_tab.replace('Ä', 'ž')
occupations_tab = occupations_tab.replace('×', 'ž')
occupations_tab = occupations_tab.replace('\n', '').split(",")
occupations_tab = map(str.strip, occupations_tab"""

# Join url whitelist and occupations.
# url_whitelist_occupations = url_whitelist + occupations_url

# Join tab whitelist and occupations.
# tab_whitelist_occupations = tab_whitelist + occupations_tab


# base = open("G:/myVE/vacancies/bazni.txt", "w")
# non_base = open("G:/myVE/vacancies/ne_bazni.txt", "w")

class JobSpider(scrapy.Spider):
    # Name of spider
    name = "job_0"

    # Custom settings that this spider uses
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'sl', },
        'DOWNLOADER_MIDDLEWARES': {
            'vacancies.middlewares.VacanciesCrawlerMiddleware': 543
        }
    }

    # List of all domains to be checked; a sublist with 60 domains is created.
    with open("PATH/TO/SOME/DIRECTORY/urls_year_2018.txt", "r+") \
            as urls_file:
        start_urls = [row.strip() for row in urls_file.readlines()][1:60]
    start_urls += [url + "/" if not url.endswith("/") else url[:-1] for url in start_urls]

    # Initiates the Spider and runs spider_startinfo and spider_endinfo at approriate times.
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(JobSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_startinfo, signals.spider_opened)
        crawler.signals.connect(spider.spider_endinfo, signals.spider_closed)
        return spider

    # Gives some basic info before scraping begins.
    def spider_startinfo(self, spider):
        print("Starting search of relevant pages...\n")
        print("Domains:\n%s\n\n" % str(spider.start_urls))
        spider.start_time = time.time()

    # Gives some basic info after finishing with scraping.
    def spider_endinfo(self, spider):
        end_time = round(time.time() - spider.start_time)
        if str(len(spider.jobs_urls)).endswith("01") or len(spider.jobs_urls) == 1:
            print("\n\nSearch finished, found %d relevant page." % len(spider.jobs_urls))
        else:
            print("\n\nSearch finished, found %d relevant pages." % len(spider.jobs_urls))
        print("Time elapsed for crawling: %02d:%02d:%02d.\n\n" % (end_time//3600, end_time//60 - (end_time//3600)*60,
                                                        end_time - (end_time // 60) * 60))
        spider.logger.info("Time elapsed for crawling: %02d:%02d:%02d" % (end_time//3600,
                                                                          end_time//60 - (end_time//3600)*60,
                                                                          end_time - (end_time // 60) * 60))

    # Result of the program is this list of job vacancies webpages.
    jobs_urls = []

    # What is actually done after the connection is established. The URL and tabs are checked against whitelisted words.
    # Some URLs are excluded (images, PDFs, videos, sound recordings, social network widgets and links, etc.).
    # Relevant subpages' URLs are yielded for each domain. By using the
    #
    # scrapy crawl jobs -o urls.csv -t csv --logfile log.txt
    #
    # command, a csv of all yielded resutls is saved to the main project directory.
    def parse(self, response):
        print("%*s" % (210, ""), end="\r")
        print("Spider %s now working...Connected to %s" % (self.name, response.url[:160]), end="\r")
        try:
            response.selector.remove_namespaces()
        # print "response url" , str(response.url)
        except Exception as e:
            self.logger.info(e)
            response = scrapy.http.HtmlResponse(response.url)
            response.selector.remove_namespaces()

        # Take url of response, because we would like to stay on the same domain.
        parsed = urlparse(response.url)

        # Base url.
        # base_url = get_base_url(response).strip()
        base_url = parsed.scheme + '://' + parsed.netloc
        # print "base url" , str(base_url)
        # If the urls grows from seeds, it's ok, otherwise not.
        if base_url in self.start_urls:
            # print "base url je v start"
            # base.write(response.url+"\n")



            # net1 = parsed.netloc

            # Take all urls, they are marked by "href" or "data-link". These are either webpages on our website either new websites.
            urls = response.xpath('//@href').extract() + response.xpath('//@data-link').extract()
            # print "povezave na tej strani ", urls



            # Loop through all urls on the webpage.
            for url in urls:
                # Test all new urls. NE DELA

                # print "url ", str(url)

                # If url doesn't start with "http", it is relative url, and we add base url to get absolute url.
                if not (url.startswith("http")):
                    # Povežem delni url z baznim url.
                    url = urljoin(base_url, url).strip()

                # print "new url ", str(url)

                new_parsed = urlparse(url)
                new_base_url = new_parsed.scheme + '://' + new_parsed.netloc
                # print "new base url ", str(new_base_url)

                if new_base_url in self.start_urls:
                    # print "yes"

                    url = url.replace("\r", "")
                    url = url.replace("\n", "")
                    url = url.replace("\t", "")
                    url = url.replace("\\", "/")
                    url = url.replace("\"", "'")
                    url = url.strip()

                    # Remove anchors '#', that point to a section on the same webpage, because this is the same webpage.
                    # But we keep question marks '?', which mean, that different content is pulled from database.
                    if '#' in url:
                        index = url.find('#')
                        url = url[:index]
                        if url in self.jobs_urls:
                            continue

                    # Ignore ftp and sftp.
                    if url.startswith("ftp") or url.startswith("sftp"):
                        continue





                        # Compare each url on the webpage with original url, so that spider doesn't wander away on the net.
                        # net2 = urlparse(url).netloc
                        # test.write("lokacija novega url "+ str(net2)+"\n")

                        # if net2 != net1:
                        #    continue
                        # test.write("ni ista lokacija, nadaljujemo\n")

                    # If the last character is slash /, I remove it to avoid duplicates.
                    if url[len(url) - 1] == '/':
                        url = url[:(len(url) - 1)]

                    # If url includes characters like %, ~ ... it is LIKELY NOT to be the one I are looking for and I ignore it.
                    # However in this case I exclude good urls like http://www.mdm.si/company#employment
                    if any(x in url for x in ['%', '~',

                                              # slike
                                              '.jpg', '.jpeg', '.png', '.gif', '.eps', '.ico', '.svg', '.tif', '.tiff',
                                              '.JPG', '.JPEG', '.PNG', '.GIF', '.EPS', '.ICO', '.SVG', '.TIF', '.TIFF',

                                              # dokumenti
                                              '.xls', '.ppt', '.doc', '.xlsx', '.pptx', '.docx', '.txt', '.csv', '.pdf',
                                              '.pd',
                                              '.XLS', '.PPT', '.DOC', '.XLSX', '.PPTX', '.DOCX', '.TXT', '.CSV', '.PDF',
                                              '.PD',

                                              # glasba in video
                                              '.mp3', '.mp4', '.mpg', '.ai', '.avi', '.swf',
                                              '.MP3', '.MP4', '.MPG', '.AI', '.AVI', '.SWF',

                                              # stiskanje in drugo
                                              '.zip', '.rar', '.css', '.flv', '.xml'
                                                                              '.ZIP', '.RAR', '.CSS', '.FLV', '.XML'

                                              # Twitter, Facebook, Youtube
                                              '://twitter.com',
                                              '://mobile.twitter.com', 'www.twitter.com',
                                              'www.facebook.com', 'www.youtube.com'

                                              # Feeds, RSS, arhiv
                                              '/feed', '=feed', '&feed', 'rss.xml', 'arhiv'

                                              ]):
                        continue

                    # We need to save original url for xpath, in case we change it later (join it with base_url)
                    # url_xpath = url


                    # We don't want to go to other websites. We want to stay on our website, so we keep only urls with domain (netloc) of the company we are investigating.
                    # if (urlparse(url).netloc == urlparse(base_url).netloc):



                    # The main part. We look for webpages, whose urls include one of the employment words as strings.
                    # We will check the tab of the url as well. This is additional filter, suggested by Dan Wu, to improve accuracy.
                    # tabs = response.xpath('//a[@href="%s"]/text()' % url_xpath).extract()
                    tabs = response.xpath('//a[@href="%s"]/text()' % url).extract()
                    # tabs = response.xpath('.//title/text()').extract()

                    # Sometimes tabs can be just empty spaces like '\t' and '\n' so in this case we replace it with [].
                    # That was the case when the spider didn't find this employment url: http://www.terme-krka.com/si/sl/o-termah-krka/o-podjetju-in-skupini-krka/zaposlitev/

                    # tabs = [tab.encode('utf-8') for tab in tabs]
                    tabs = [tab.replace('\t', '') for tab in tabs]
                    tabs = [tab.replace('\n', '') for tab in tabs]
                    tab_empty = True
                    for tab in tabs:
                        if tab != '':
                            tab_empty = False
                    if tab_empty == True:
                        tabs = []

                    # -- Instruction.
                    # -- Users in other languages, please insert employment words in your own language,
                    #    like jobs, vacancies, career, employment ... --
                    # Starting keyword_url is zero, then we add keywords as we find them in url.
                    keyword_url = ''
                    for keyword in url_whitelist:

                        if keyword in url:
                            keyword_url = keyword_url + keyword + ' '
                    # a) If we find at least one keyword in url, we continue.
                    if keyword_url != '':

                        # 1. Tabs are empty.
                        if tabs == []:

                            # We found url that includes one of the magic words and also the text includes a magic word.
                            # We check url, if we have found it before. If it is new, we add it to the list "jobs_urls".
                            if url not in self.jobs_urls:
                                self.jobs_urls.append(url)
                                item = JobItem()
                                item["url"] = url
                                # item["keyword_url"] = keyword_url
                                # item["keyword_url_tab"] = ' '
                                # item["keyword_tab"] = ' '
                                print("Vacancy Subpage ", url)

                                # We return the item.
                                yield item



                        # 2. There are texts in tabs, one or more.
                        else:

                            # For the same partial url several texts are possible.
                            for tab in tabs:

                                # We search for keywords in tabs.
                                keyword_url_tab = ''
                                for key in tab_whitelist:

                                    if key in tab:
                                        keyword_url_tab = keyword_url_tab + key + ' '

                                # If we find some keywords in tabs, then we have found keywords in both url and tab and we can save the url.
                                if keyword_url_tab != '':

                                    # keyword_url_tab starts with keyword_url from before, because we want to remember
                                    # keywords from both url and tab. So we add initial keyword_url.
                                    keyword_url_tab = 'URL ' + keyword_url + ' TAB ' + keyword_url_tab

                                    # We found url that includes one of the magic words and also the tab includes a
                                    # magic word. We check url, if we have found it before. If it is new, we add it to
                                    # the list "jobs_urls".
                                    if url not in self.jobs_urls:
                                        self.jobs_urls.append(url)
                                        item = JobItem()
                                        item["url"] = url
                                        # item["keyword_url"] = ' '
                                        # item["keyword_url_tab"] = keyword_url_tab
                                        # item["keyword_tab"] = ' '
                                        print("Vacancy Subpage ", url)

                                        # We return the item.
                                        yield item

                                # We haven't found any keywords in tabs, but url is still good, because it contains some
                                #  keywords, so we save it.
                                else:

                                    if url not in self.jobs_urls:
                                        self.jobs_urls.append(url)
                                        item = JobItem()
                                        item["url"] = url
                                        # item["keyword_url"] = keyword_url
                                        # item["keyword_url_tab"] = ' '
                                        # item["keyword_tab"] = ' '
                                        print("Vacancy Subpage ", url)

                                        # We return the item.
                                        yield item

                    # b) If keyword_url = empty, there are no keywords in url, but perhaps there are
                    #  keywords in tabs. So we check tabs.
                    else:
                        for tab in tabs:

                            keyword_tab = ''
                            # for key in tab_whitelist:
                            for key in tab_whitelist:

                                if key in tab:
                                    keyword_tab = keyword_tab + key + ' '
                            if keyword_tab != '':

                                if url not in self.jobs_urls:
                                    self.jobs_urls.append(url)
                                    item = JobItem()
                                    item["url"] = url
                                    # item["keyword_url"] = ' '
                                    # item["keyword_url_tab"] = ' '
                                    # item["keyword_tab"] = keyword_tab
                                    print("Vacancy Subpage ", url)

                                    # We return the item.
                                    yield item

                    # We don't put "else" sentence because we want to further explore the employment webpage to find
                    # possible new employment webpages. We keep looking for employment webpages, until we reach the
                    # DEPTH set in settings.py.
                    yield Request(url, callback=self.parse)

                    # else:
                    # non_base.write(response.url+"\n")
