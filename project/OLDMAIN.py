import requests
from bs4 import BeautifulSoup

import os

FILES_DIR = "outputMin/"

FILE_EXTENTION = ".txt"

solar_longitude_range = 360
solar_longitude_start = 240
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
    # getting the data of the first page with the graph
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "html.parser")

    # finding the link of the ASCII data
    ascii_table_URL = mcd_site_baselink + soup.find("a")['href'][3:]
    return requests.get(ascii_table_URL).text

def write_txt_file(ASCII_data, slon, lat):
    # Saving the data to a file...
    file_name = f"MCD_ls{slon}_lat{lat}"

    with open(FILES_DIR + file_name+FILE_EXTENTION, "w") as file_entity:
        file_entity.write(ASCII_data)

def main():
    for slon in range(solar_longitude_start, solar_longitude_range, solar_longitude_step):
        cls()
        if not solar_longitude_range == 0:
            print('Progess is: ', 100*(slon/solar_longitude_range), "%")
        else:
            print('Progess is: 0%')
        print(f"Current Solar Longitude {slon}")
        for lat in range(latitude_start, latitude_range, latitude_step):
            print(f"Current Latitude {lat}")
            
            graph_query = generate_database_query(slon, lat)
            ASCII_data = find_ASCII_data(graph_query)
            write_txt_file(ASCII_data, slon, lat)


if __name__ == "__main__":
    main()

