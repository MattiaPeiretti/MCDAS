# ----------------------------------------------------------------
# Interface that takes care of handling the requests to
# the MCD database.
# Code written by MattiaPeiretti (c). https>//mattiapeiretti.com
# Technical consultancy: Marco De Marco
# ----------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import re
import time

from project.settingsHandler import SettingsHandler


def find_number_in_string(string):
    numbers = []
    print(string)
    for word in string:
        if word.isdigit():
            numbers.append(int(word))
    return numbers


class MCDInterface:
    def __init__(self, base_link):
        self.base_link = base_link
        self.settings_handler = SettingsHandler()

    def do_query(self, slon, variable, coordinates):

        request_URI = self.get_query_URI(slon, variable, coordinates)
        return self.do_direct_query(request_URI)

    def do_direct_query(self, URI):
        try:
            response = requests.get(URI)
            if not response.status_code == 200:
                raise Exception()
        except:
            for try_nr in range(
                0, self.settings_handler.get_setting("REQUEST_RETRY_AMOUNT")
            ):
                print(
                    f"An error with the request occured. Trying again. Try {try_nr} out of {self.settings_handler.get_setting('REQUEST_RETRY_AMOUNT')}"
                )
                time.sleep(self.settings_handler.get_setting("REQUEST_RETRY_WAITTIME"))
                try:
                    response = requests.get(URI)
                    break
                except:
                    pass
            return self.settings_handler.get_setting("REQUEST_ERROR_CHARACTER")

        soup = BeautifulSoup(response.text, "html.parser")

        value = soup.find("li").text

        return float(re.findall("\d+\.\d+", value)[0])

    def get_query_URI(self, slon, variable, coordinates):
        lat = coordinates[0]
        lon = coordinates[1]
        alt = 0

        # FIX LATER!!
        # if not coordinates[2]:
        #     alt = 0
        # else:
        #     alt = coordinates[2]
        return f"{self.base_link}?ls={slon}&latitude={lat}&longitude={lon}&altitude={alt}&zkey=3&isfixedlt=on&dust=1&hrkey=1&zonmean=on&var1={variable}&var2=none&var3=none&var4=none&dpi=80&islog=off&colorm=jet&minval=&maxval=&proj=cyl&plat=&plon=&trans=&iswind=off&latpoint=&lonpoint="


if __name__ == "__main__":

    settings_handler = SettingsHandler()

    interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))

    print(interface.do_query(56, "tsurfmn", [45, 16]))
