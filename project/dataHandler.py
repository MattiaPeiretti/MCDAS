from mcd_interface import MCDInterface
from settingsHandler import SettingsHandler
import csv

class dataHandler():
    def __init__(self, dir_path, settings_handler):
        self.dir_path = dir_path
        self.setting_handler = settings_handler

    def write_database_slon_record(self, record_type, slon, db_dict):
        padded_slon = str(slon).rjust(self.setting_handler.get_setting("RECORDS_FILENAME_NUMBERS_PADDING"), "0")
        filename = f"MCDas_{record_type}_LS{padded_slon}"

        with open(self.dir_path + filename + '.csv', mode='w') as csv_file:
            fieldnames = ['lat', 'lon', 'min_temp']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for lat in db_dict:
                for lon in db_dict[lat]:
                    print(lat, lon, db_dict[lat][lon])
                    writer.writerow({'lat': lat, 'lon': lon, 'min_temp':db_dict[lat][lon]})

    



if __name__ == "__main__":
    
    print("Hello World!!")


    

    
            