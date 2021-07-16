#----------------------------------------------------------------
# Interface that takes care of handling the requests to 
# the MCD database.
# Code written by MattiaPeiretti (c). https>//mattiapeiretti.com
# Technical consultancy: Marco De Marco
#----------------------------------------------------------------

from sys import excepthook
import requests
from bs4 import BeautifulSoup
import re
import time

from settingsHandler import SettingsHandler
import consoleGUI

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
        self.settings_handler = SettingsHandler()
        self.gui = consoleGUI.GUI("Error")

    def do_query(self, slon, variable, coordinates):
        lat = coordinates[0]
        lon = coordinates[1]
        alt = 0

        # FIX LATER!!
        # if not coordinates[2]:
        #     alt = 0
        # else:
        #     alt = coordinates[2]
        request_URI = f"{self.base_link}?ls={slon}&latitude={lat}&longitude={lon}&altitude={alt}&zkey=3&isfixedlt=on&dust=1&hrkey=1&zonmean=on&var1={variable}&var2=none&var3=none&var4=none&dpi=80&islog=off&colorm=jet&minval=&maxval=&proj=cyl&plat=&plon=&trans=&iswind=off&latpoint=&lonpoint="
        
        try:
            response = requests.get(request_URI)
            if not response.status_code == 200:
                raise Exception()
        except:
            for try_nr in range(0, self.settings_handler.get_setting("REQUEST_RETRY_AMOUNT")):
                self.gui.display_error("Request Error Occured", f"Trying to connect again: try {try_nr} of {self.settings_handler.get_setting('REQUEST_RETRY_AMOUNT')}")
                time.sleep(self.settings_handler.get_setting("REQUEST_RETRY_WAITTIME"))
                try:
                    response = requests.get(request_URI)
                    break
                except:
                    pass
            return self.settings_handler.get_setting("REQUEST_ERROR_CHARACTER")

        soup = BeautifulSoup(response.text, "html.parser")
        
        value = soup.find("li").text

        return float(re.findall("\d+\.\d+", value)[0])


if __name__ == "__main__":
    
    settings_handler = SettingsHandler()

    interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))

    print(interface.do_query(56, "tsurfmn",[45, 16]))
