#----------------------------------------------------------------
# Settings takes care of handling the settings of the whole
# program.
# Code written by MattiaPeiretti (c). https>//mattiapeiretti.com
# Technical consultancy: Marco De Marco
#----------------------------------------------------------------

SETTINGS = {
    "MCD_BASELINK": "http://www-mars.lmd.jussieu.fr/mcd_python/cgi-bin/mcdcgi.py",
    "RECORDS_FILENAME_NUMBERS_PADDING": 3,
    #"RECORD_TYPE": "tsurfmn",
    "RECORD_TYPE": "tsurfmx",
    "SLON_STEP": 15,
    "LAT_STEP": 5.0,
    "LON_STEP": 10.0,
    "REQUEST_RETRY_WAITTIME": 10,
    "REQUEST_RETRY_AMOUNT": 5,
    "REQUEST_ERROR_CHARACTER": "0"
}

class SettingsHandler():
    __instance = None                                                                       # Instance shared varaible

    #Singleton
    def __new__(cls, *args, **kwargs):                                                      # Checking upon initialization that the class 
        if not SettingsHandler.__instance:                                                  # hasn't already been initialized
            SettingsHandler.__instance = object.__new__(cls)                                # if so returning the already
        return SettingsHandler.__instance                                                   # initialized instance..
    
    def __init__(self):
        self.settings = self.read_settings()

    def get_setting(self, setting):
        if self.settings[setting]:
            return self.settings[setting]
        else: 
            return False

    def read_settings(self):
        return SETTINGS