#----------------------------------------------------------------
# Interface that takes care of handling the requests to 
# the MCD database.
# Code written by MattiaPeiretti (c). https>//mattiapeiretti.com
# Technical consultancy: Marco De Marco
#----------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import re

def find_number_in_string(string):
    numbers = []
    print(string)
    for word in string:
        if word.isdigit():
            numbers.append(int(word))
    return numbers

class MCDInterface():
    def __init__(self, base_link):
        self.base_link = base_link

    def do_query(self, slon, variable, coordinates):
        lat = coordinates[0]
        lon = coordinates[1]
        alt = 0

        # FIX LATER!!
        # if not coordinates[2]:
        #     alt = 0
        # else:
        #     alt = coordinates[2]


        raw_html = requests.get(f"{self.base_link}?ls={slon}&latitude={lat}&longitude={lon}&altitude={alt}&zkey=3&isfixedlt=on&dust=1&hrkey=1&zonmean=on&var1={variable}&var2=none&var3=none&var4=none&dpi=80&islog=off&colorm=jet&minval=&maxval=&proj=cyl&plat=&plon=&trans=&iswind=off&latpoint=&lonpoint=")
        soup = BeautifulSoup(raw_html.text, "html.parser")
        
        value = soup.find("li").text

        return float(re.findall("\d+\.\d+", value)[0])


if __name__ == "__main__":
    
    interface = MCDInterface("http://www-mars.lmd.jussieu.fr/mcd_python/cgi-bin/mcdcgi.py")

    print(interface.do_query(56, "tsurfmn",[45, 16]))
