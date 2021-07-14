import requests
from bs4 import BeautifulSoup
import time

import os

FILES_DIR = "../output/"

FILE_EXTENTION = ".txt"

solar_longitude_range = 360
solar_longitude_start = 0
solar_longitude_step = 15

latitude_range = 90
latitude_start = -90
latitude_step = 5

mcd_site_baselink = "http://www-mars.lmd.jussieu.fr/mcd_python/"

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_database_query(slon, lat):
    return f"http://www-mars.lmd.jussieu.fr/mcd_python/cgi-bin/mcdcgi.py?ls={slon}&latitude={lat}&longitude=all&altitude=0&zkey=3&isfixedlt=on&dust=1&hrkey=1&zonmean=on&var1=tsurfmn&var2=none&var3=none&var4=none&dpi=80&islog=off&colorm=jet&minval=&maxval=&proj=cyl&plat=&plon=&trans=&iswind=off&latpoint=&lonpoint="

def find_ASCII_data(link):
    global AG
    global AGT
    # getting the data of the first page with the graph
    AG = time.time()
    req = requests.get(link)
    AGT = time.time()
    soup = BeautifulSoup(req.text, "html.parser")

    # finding the link of the ASCII data
    ascii_table_URL = mcd_site_baselink + soup.find("a")['href'][3:]
    vb = requests.get(ascii_table_URL).text
    return vb

def write_txt_file(ASCII_data, slon, lat):
    # Saving the data to a file...
    file_name = f"MCD_ls{slon}_lat{lat}"

    with open(FILES_DIR + file_name+FILE_EXTENTION, "w") as file_entity:
        file_entity.write(ASCII_data)

def main():
    global AG
    global AGT
    atime1 = time.time()
    graph_query = generate_database_query(15, 5)
    atime2 = time.time()
    

    ASCII_data = find_ASCII_data(graph_query)

    ctime1 = time.time()
    write_txt_file(ASCII_data, 15, 5)
    ctime2 = time.time()


    print(f"it takes: {atime2 - atime1} to request data")
    print(f"it takes: {AGT - AG} to process data")
    print(f"it takes: {ctime2 - ctime1} to write data")

if __name__ == "__main__":
    main()

