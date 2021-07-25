# ----------------------------------------------------------------
# Settings takes care of handling the settings of the whole
# program.
# Code written by MattiaPeiretti (c). https>//mattiapeiretti.com
# Technical consultancy: Marco De Marco
# ----------------------------------------------------------------

import json
import constants


class SettingsHandler:
    __instance = None  # Instance shared varaible

    # Singleton
    def __new__(cls, *args, **kwargs):  # Checking upon initialization that the class
        if not SettingsHandler.__instance:  # hasn't already been initialized
            SettingsHandler.__instance = object.__new__(
                cls
            )  # if so returning the already
        return SettingsHandler.__instance  # initialized instance..

    def __init__(self):
        self.write_settings_to_file()

        self.settings = self.read_settings()

    def get_setting(self, setting):
        if setting in self.settings:
            return self.settings[setting]
        else:
            return False

    def read_settings(self):
        with open(constants.SETTINGS_FILE_PATH) as config_file:
            data = json.load(config_file)
        self.settings = data

    def update_setting(self, setting, value):
        self.settings[setting] = value
        self.write_settings_to_file()

    def write_settings_to_file(self):
        with open(constants.SETTINGS_FILE_PATH, "w") as config_file:
            json.dump(self.settings, config_file)
