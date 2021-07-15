from mcd_interface import MCDInterface
from settingsHandler import SettingsHandler
import csv
import os
import numpy as np

def add_value_to_dict(dict, lat, lon, value):
    if lat in dict.keys():
        dictdata = dict[lat]
        dictdata[lon] = value
        dict[lat] = dictdata
    else:
        dict[lat] = {lon:  value}
    return dict

def print_data(slon, lat, lon, value, lat_margins, lon_margins):
    print(f"Solar Longitude: {slon} Total Work: {100*(slon/360)}%, Latitude: {lat} Total Work: {100*((lat+90)/(lat_margins[1]+90))}%, Longitude: {lon} Total Work: {100*(lon/lon_margins[1])}%, Current Value: {value}",  end='\r')
        

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

class dataHandler():
    def __init__(self, dir_path, settings_handler, mcd_interface):
        self.dir_path = dir_path
        self.settings_handler = settings_handler
        self.mcd_interface = mcd_interface

    def collect_data(self, slon, lat_margins, lon_margins, record_type):

        data = {}

        lat_step = self.settings_handler.get_setting("LAT_STEP")
        lon_step = self.settings_handler.get_setting("LON_STEP")

        for lat in np.arange(lat_margins[0], lat_margins[1] + lat_step, lat_step):

            # If currently checking the poles, we will assign the data of one point to the whole scale.
            if lat == lat_margins[0] or lat == lat_margins[1]:

                current_value = self.mcd_interface.do_query(slon, record_type, [lat, 180])

                for lon in np.arange(lon_margins[0], lon_margins[1] + lon_step, lon_step):
                    data = add_value_to_dict(data, lat, lon, current_value)

                  
                    print_data(slon, lat, lon, current_value, lat_margins, lon_margins)
                continue

            for lon in np.arange(lon_margins[0], lon_margins[1] + lon_step, lon_step):
                current_value = self.mcd_interface.do_query(slon, record_type, [lat, lon])

                data = add_value_to_dict(data, lat, lon, current_value)
                print_data(slon, lat, lon, current_value, lat_margins, lon_margins)
                
        return data


    def write_database_slon_record(self, record_type, slon, db_dict):
        padded_slon = str(slon).rjust(self.settings_handler.get_setting("RECORDS_FILENAME_NUMBERS_PADDING"), "0")
        filename = f"MCDas_{record_type}_LS{padded_slon}"

        with open(self.dir_path + filename + '.csv', mode='w', newline='') as csv_file:
            fieldnames = ['lat', 'lon', 'min_temp']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for lat in db_dict:
                for lon in db_dict[lat]:
                    writer.writerow({'lat': lat, 'lon': lon, 'min_temp':db_dict[lat][lon]})

    



if __name__ == "__main__":
    
    print("Hello World!!")


    

    
            