import time, os, shutil, re


def adjust_programs_to_new_period(con=False, newyear="", newmonth=""):
    path = r"Q:\Big_Data\Spletne_strani_podjetij\Strganje"
    year = "2018"
    if not newyear:
        newyear = input("What is the current year(current year: %s)? " % year)
    if not newyear or str(newyear)[0] == "y":
        newyear = year
    month = "november"
    if not newmonth:
        newmonth = input("What is the current month (current month: %s)? " % month)
    if not newmonth or newmonth[0] == "y":
        newmonth = month
    time.sleep(1)

    if not os.path.exists(path + "\\%s_%s" % (newyear, newmonth)):
        os.makedirs(path + r"\%s_%s\posnetki" % (newyear, newmonth))

        os.makedirs(path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders" % (newyear, newmonth, newmonth))

        shutil.copy(path + r"\%s_%s\%s_Crt_ubuntu\scrapy.cfg" % (year, month, month),
                    path + r"\%s_%s\%s_Crt_ubuntu" % (newyear, newmonth, newmonth))

        for file in os.listdir(path + "\\%s_%s\\%s_Crt_ubuntu\\vacancies" % (year, month, month)):
            if file not in ["spiders", "__pycache__"]:
                shutil.copy(path + "\\%s_%s\\%s_Crt_ubuntu\\vacancies\\%s" % (year, month, month, file),
                            path + "\\%s_%s\\%s_Crt_ubuntu\\vacancies\\%s" % (newyear, newmonth, newmonth, file))
        shutil.copy(path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders\job_spider_0.py" % (year, month, month),
                        path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders\job_spider_0.py" % (newyear, newmonth, newmonth))
        shutil.copy(path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders\job_scraper.py" % (year, month, month),
                    path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders\job_scraper.py" % (newyear, newmonth, newmonth))

    if not (con or year != newyear or month != newmonth):
        to_con = input("This directory already exists. Are you sure you want to continue?")
        if not to_con or to_con.startswith("y"):
            return adjust_programs_to_new_period(True, "y", "y")
        else:
            print("\n\nCancelling...")
            return 0
    else:
        print("\n\n")
        print("\nFiles will be written to the directory: Q:\Big_Data\Spletne_strani_podjetij\Strganje\%s_%s"
              % (newyear, newmonth))
        time.sleep(1)
        for s in range(4):
            print("\rYou have %s seconds to interrupt this process!" % (5-s), end="")
            time.sleep(1)
        print("\rYou have 1 second to interrupt this process! ", end="")
        time.sleep(1)
        print("\rYou have 0 seconds to interrupt this process!", end="")
        print("\r                                             ", end="")
        print("\n")

        # Poprava na novo obdobje v prvem pajku
        with open(path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders\job_spider_0.py" % (newyear, newmonth, newmonth),
                  "r+b") as spdr1:
            spider1 = spdr1.read().decode()
        with open(r"Q:\Big_Data\Spletne_strani_podjetij\IKT\urls_leto_%s.txt" % year, "r") as urlist:
            spidernum = round(len(urlist.readlines()) / 60)
        try:
            urlist = open(r"Q:\Big_Data\Spletne_strani_podjetij\IKT\urls_leto_%s.txt" % newyear, "r")
            newspidernum = round(len(urlist.readlines()) / 60)
            urlist.close()
        except FileNotFoundError:
            print("The file \'urls_leto_%s.txt\' was not found, therefore the"
                  " number of spiders to create was not updated." % newyear)
            newspidernum = spidernum
        spider1 = re.sub("IKT\\\\urls_leto_%s.txt" % year, "IKT\\urls_leto_%s.txt" % newyear, spider1)
        with open(path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders\job_spider_0.py" % (newyear, newmonth, newmonth),
                  "wb") as spdr1:
            spdr1.write(spider1.encode())

        # Poprava na novo obdobje v strgalniku strani
        with open(path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders\job_scraper.py" % (newyear, newmonth, newmonth), "r+b")\
                as scr_prgm:
            scr_program = scr_prgm.read().decode()
        scr_program = re.sub("leto_mesec = \"%s_%s\"" % (year, month), "leto_mesec = \"%s_%s\"" % (newyear, newmonth),
                             scr_program)
        with open(path + r"\%s_%s\%s_Crt_ubuntu\vacancies\spiders\job_scraper.py" % (newyear, newmonth, newmonth), "wb")\
                as scr_prgm:
            scr_prgm.write(scr_program.encode())

        # Poprava na novo obdobje v programu 'pripravi_pajke.py'
        with open(r"Q:\Big_Data\Spletne_strani_podjetij\Python\programi_2018\pripravi_pajke.py", "r+") as prgm:
            program = prgm.read()
        program = re.sub("leto, mesec = \"%s\", \"%s\"" % (year, month),
                         "leto, mesec = \"%s\", \"%s\"" % (newyear, newmonth), program)
        program = re.sub("IKT\\\\urls_leto_%s.txt" % year, "IKT\\\\urls_leto_%s.txt" % newyear, program)
        with open(r"Q:\Big_Data\Spletne_strani_podjetij\Python\programi_2018\pripravi_pajke.py", "w") as prgm:
            prgm.write(program)

        # Poprava na novo obdobje v programu 'read_all_csv.py'
        with open(r"Q:\Big_Data\Spletne_strani_podjetij\Python\programi_2018\read_all_csv.py", "r+b") as prgm:
            program = prgm.read().decode()
        program = re.sub("leto_mesec = \"%s_%s\"" % (year, month), "leto_mesec = \"%s_%s\"" % (newyear, newmonth),
                         program)
        with open(r"Q:\Big_Data\Spletne_strani_podjetij\Python\programi_2018\read_all_csv.py", "wb") as prgm:
            prgm.write(program.encode())

        # Poprava na novo obdobje v TEM programu
        with open(r"Q:\Big_Data\Spletne_strani_podjetij\Python\programi_2018\MASTER_posodobi_obdobje.py", "r+b") as prgm:
            program = prgm.read().decode()
        program = re.sub("year = \"%s\"" % year, "year = \"%s\"" % newyear, program)
        program = re.sub("month = \"%s\"" % month, "month = \"%s\"" % newmonth, program)
        with open(r"Q:\Big_Data\Spletne_strani_podjetij\Python\programi_2018\MASTER_posodobi_obdobje.py", "wb") as prgm:
            prgm.write(program.encode())
        return 1


adjust_programs_to_new_period()
