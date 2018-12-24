# This is a program that creates a launch file for spiders in the relevant map. It generates scrapy programs (from a
# template program) and the code of the launch bat file that starts all of them. The program works in Python 2.7.

# Path variables:
leto, mesec = "2018", "november"
scraping_map = r"Q:\Big_Data\Spletne_strani_podjetij\Strganje\%s_%s" % (leto, mesec)
subfolder = "%s_Crt" % mesec
# Initial parameter to determine number of spiders. Each spider crawls 60 urls. E.g, if there are 6057 urls, we set it
# to 101 spiders, so that the last subset will be 6000 to 6060. There is also the initial spider, that crawls webpages
# 1 to 59, so there will actually be 101 spiders.
with open(r"Q:\Big_Data\Spletne_strani_podjetij\IKT\urls_leto_2018.txt", "rb") as urls:
    j = int(round((len([url for url in urls.readlines()]) + 30) / 60))

# Prepare SPIDERS and BAT FILE with commands, that will throw all spiders at the same time to the network.
# echo %1 #this is example of .bat file with parameters
# echo %2
# echo %3
# scrapy crawl jobs -o urls.csv -t csv --logfile log.txt %1 %2 %3

# Creates a commands.bat file with instructions for scrapy launches on Windows.
'''
bat1 = open(scraping_map + "/" + subfolder + "1/commands.bat", "w")

# Our scrapy module (and Python 2.7) is installed on the F: directory. Also take notice, that we scrape webpages in
# Slovenian only, you need to change that in the second row.
bat1.write("::commands.bat\ntitle cmdPython27\nSET PYTHONHOME=F:\python\python27\nSET PYTHONPATH=F:\Python\Python27;F:\Python\Python27\Lib;F:\Python\Python27\DLLs\n")
bat1.write("SET ORACLE_HOME=F:\ORACLE\ORA11\nSET MSHELP_TOOLS=%ORACLE_HOME%\MSHELP\nSET NLS_LANG=SLOVENIAN_SLOVENIA.EE8MSWIN1250\nSET NLS_DATE_FORMAT=DD.MM.YYYY\nSET TNS_ADMIN=%ORACLE_HOME%\\network\\admin\n")
bat1.write("SET PATH=%PYTHONHOME%;%PYTHONHOME%\Scripts;%ORACLE_HOME%\BIN;%ORACLE_HOME%\jdk\jre\\bin;%ORACLE_HOME%\jdk\jre\\bin\client;%PATH%\ncd \"Q:....\nstart ...\nstart ...\n")

# Specify where should the scraped results be written:
bat1.write("cd \"" + scraping_map + "\\" + subfolder +"1\"\n")


bat1.write("setlocal\nfor /f \"tokens=4-5 delims=. \" %%%%i in ('ver') do set VERSION=%%%%i.%%%%j\necho Windows
%%version%%>\"%s\\%s1\\THIS_MACHINE_IS_ONLINE.txt\nendlocal\n" % (scraping_map, subfolder))
# The first scrapy launch order with the name of the results (enterprises_0_10_url.csv)
# and logfile (enterprises_0_10_log.txt):
bat1.write("start F:\Python\Python27\Scripts\scrapy crawl jobs_0 -o enterprises_url_0.csv -t csv
--logfile enterprises_log_0.txt\n")
'''

# Creates a term.sh file with instuctions for scrapy launchers on Ubuntu
term = open(scraping_map + "/" + subfolder + "_ubuntu/term.sh", "wb")
term.write(b"ulimit -n 4096\nSTART=0\n")
term.write(b"source /home/STATISTIKA/grahonja/.local/share/virtualenvs/ubuntu_proj-qDvrCgzC/bin/activate\n")
term.write(b"cd /home/STATISTIKA/grahonja/WinFolders/%s/%s_ubuntu\n\n"
           % (scraping_map.replace(":", "").replace("\\", "/").encode(), subfolder.encode()))
term.write(b"END=%s\n\nfor (( c=$START; c<=$END; c++ ))\ndo\nsleep 0.25\n\n" % str(j-1).encode())
term.write(b"export http_proxy=proxy.gov.si:80\nexport https_proxy=proxy.gov.si:80\n\n")
term.write(b"/usr/bin/terminator --title seja$c --geometry=1710x782 -e \"/bin/bash -c "
           b"'/home/STATISTIKA/grahonja/.local/share/virtualenvs/ubuntu_proj-qDvrCgzC/bin/./scrapy crawl job_$c -o "
           b"enterprises_url_$c.csv -t csv --logfile enterprises_log_$c.txt ' \" & \n\n")
term.write(b"done\n\n")
term.write(b"/usr/bin/printf -n \"\n\nClick ENTER to read and merge all csv...\"\nread\n")
term.write(b"python2 /home/STATISTIKA/grahonja/WinFolders/Q/Big_Data"
           b"/Spletne_strani_podjetij/Python/programi_2018/read_all_csv.py ")
term.write(b"/home/STATISTIKA/grahonja/.local/share/virtualenvs/ubuntu_proj-qDvrCgzC/bin/./scrapy crawl scraper "
           b"--logfile enterprises_scraper.txt\n")
term.write(b"/usr/bin/printf -n \"\n\nClick ENTER to scrape relevant URLs...\"\nread\n")
term.write(b"/home/STATISTIKA/grahonja/.local/share/virtualenvs/ubuntu_proj-qDvrCgzC/bin/./scrapy crawl scraper "
           b"--logfile scrape_log.txt\n")
term.write(b"deactivate\n\n")
term.close()

# Loop that generates spiders from initial spider_0_10.
for i in range(1, j):
    subfolder_n = subfolder + "_ubuntu"
    # Open the template (and first) scrapy file:
    with open(scraping_map + "\\" + subfolder_n + "\\vacancies\\spiders\\job_spider_0.py", "r+b") as prgm:
        program = prgm.read().decode("utf8")
    
    # Create new spiders with names 10_20 and so on, that scrape sections of the list of urls.
    program = program.replace("_0", "_%d" % i)
    program = program.replace("1:60", "%d:%d" % (i * 60, (i + 1) * 60))
    # Generate new spider.
    with open(scraping_map + "\\" + subfolder_n + "\\vacancies\\spiders\\job_spider_%d.py" % i, "wb") as dest:
        dest.write(program.encode("utf8"))
    '''
    # At the same time write the command into bat file.
    bat1.write("start F:\Python\Python27\Scripts\scrapy crawl jobs_" + str((i + 1) * 10) + "_" + str((i + 1) * 10 + 10)
              + " -o enterprises_" + str((i + 1) * 10) + "_"+str((i + 1) * 10 + 10)
              + "_url.csv -t csv --logfile enterprises_" + str((i + 1) * 10) + "_" + str((i + 1) * 10 + 10)
              + "_log.txt\n")
    '''
'''
bat1.close()
'''
