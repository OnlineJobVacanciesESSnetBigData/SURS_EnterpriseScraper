leto_mesec = "2018_november"

#Programme that read all .csv files in the map and puts it together to .txt .
from os import listdir

#Define the function to read all csv.
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

#Call the function.
filenames = find_csv_filenames("/home/STATISTIKA/grahonja/WinFolders/Q/Big_Data/Spletne_strani_podjetij/Strganje"
                               "/%s/%s_Crt_ubuntu" % (leto_mesec, leto_mesec[5:]))

#Open txt file to where write all urls.
f = open("/home/STATISTIKA/grahonja/WinFolders/Q/Big_Data/Spletne_strani_podjetij/Strganje"
         "/%s/vsi_najdeni_url.txt" % leto_mesec, "w")
f.write("najdeni_url\n")

#Read all csv files one by one and write them into the txt file.
for name in filenames:
    print name
    g = open("/home/STATISTIKA/grahonja/WinFolders/Q/Big_Data/Spletne_strani_podjetij/Strganje"
             "/%s/%s_Crt_ubuntu/%s" % (leto_mesec, leto_mesec[5:], str(name)), "r+")
	
    urls = g.readlines()
    for url in urls:
        #remove EOL
        url = url.strip()
        #if url == "keyword_url_tab,url,keyword_tab,keyword_url":
        if url == "url":
            continue
        #some urls begin and end with quotation mark ", because they contain double comma ,,  this is Scrapy output
        elif url[0] == "\"" and url[len(url)-1] == "\"":
            #write only url without quotation mark at the end and at the beginning
		    f.write(url[1:(len(url)-1)]+"\n")
        else:
            f.write(url+"\n")
	
f.close()
	

#avgust.
print "Number of .csv files: " + str(len(filenames))
