# scraping_EnterprisePages
Programs and documentation regarding scraping of Enterprise Pages. This project runs in Python 3.6 or more. It is **not** supported in Python 2.7. It uses the library *scrapy* for connecting and extracing information from pages.

Scrapy projects run in a predefined architecture with predefined Python scripts, which can be edited for specific uses. The structure builds
itself when running **scrapy startproject *name_of_project*** in the desired directory. The structure is:
<pre>
DIRECTORY
   |
   *name_of_project*
          |
          scrapy.cfg - configuration file for scrapy
          *name_of_project*
                 |
                 _init_.py - an (usually) empty file that tells Python that this is a module
                 items.py - a file for in-depth customization of scraped items
                 middlewares.py - a file with customizable options and methods for each Spider
                 pipelines.py - a file for customizable definitions of pipelines
                 settings.py - a file for connection settings for scrapy
                 spiders
                    |
                     _init_.py - an (usually) empty file that tells Python that this is a module
                     Spider_1.py
                     Spider_2.py
                     .
                     .
                     .
</pre>

The connections are done in parallel. The user can adjust options throught the dictionaries of options in the **settings.py** script. The
settings cover a wide range of possibilities, from number of concurent connections to time between each connection, allowed languages, etc.
Furthermore, individual options can be adjusted in the definitions of Spiders themselves editing the dictionary with the reserved name
"custom_settings".

All Spiders have a predetermined structure:
the attributes must include a unique *name*, the method *parse* and either a list of starting URLs named *start_urls* or a method which determines
starting URLs names *start_requests*. Other methods can be added following the correct guidelines. For more information check the 
[scrapy project websites](https://doc.scrapy.org/en/latest/).




###### *Keep in mind that all internet domains, paths to directories and files, file names and HTML tags are examples and should be changed before use.*

### List of all imported modules in Python:

(working with **scrapy**)
* module **scrapy**
* function *signals* from **scrapy**
* function *Request* from **scrapy.http**
* function *settings* from **scrapy.conf**
* class *JobItem* from **vacancies.items** ***(this is a project specific import)***

(parsing text and internet links)
* function *BeautifulSoup* (from module **bs4**)
* functions *urlparse* and *urljoin* (from module **urllib.parse**)
* module **urllib.parse**

(detecting text language)
* function *detect* (from module **langdetect**)

(formating date and time, calculating with time)
* module **time**
* module **datetime**

(system-specific parameters and functions)
* module **sys**
*module sys
