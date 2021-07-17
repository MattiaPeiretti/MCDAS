from mcd_interface import MCDInterface
from settingsHandler import SettingsHandler
import consoleGUI
from tqdm import tqdm

import re
import csv
import os
import numpy as np
import time
import multiprocessing


def print_data(GUI, slon, lat, lon, current_value):
    #print(f"Solar Longitude: {slon} Total Work: {100*(slon/360)}%, Latitude: {lat} Total Work: {100*((lat+90)/(lat_margins[1]+90))}%, Longitude: {lon} Total Work: {100*(lon/lon_margins[1])}%, Current Value: {value}",  end='\r')
    GUI.update(slon, lat, lon, current_value)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

class dataHandler():
    def __init__(self, dir_path, settings_handler, mcd_interface, lat_margins, lon_margins):
        self.dir_path = dir_path
        self.settings_handler = settings_handler
        self.mcd_interface = mcd_interface
        self.lat_margins = lat_margins
        self.lon_margins = lon_margins
        self.data = {}
        

        self.gui = consoleGUI.GUI("Mars Climate Database Augmented Software:", lat_margins, lon_margins)

    def prepare_data(self, slon, record_type):
        requests = []

        lat_step = self.settings_handler.get_setting("LAT_STEP")
        lon_step = self.settings_handler.get_setting("LON_STEP")

        for lat in np.arange(self.lat_margins[0], self.lat_margins[1] + lat_step, lat_step):

            # If currently checking the poles, we will assign the data of one point to the whole scale.
            if lat == self.lat_margins[0] or lat == self.lat_margins[1]:
                
                requests.append((lat, 180, self.mcd_interface.get_query_URI(slon, record_type, [lat, 180])))
                continue

            for lon in np.arange(self.lon_margins[0], self.lon_margins[1] + lon_step, lon_step):
                requests.append((lat, lon, self.mcd_interface.get_query_URI(slon, record_type, [lat, lon])))
                self.gui.display_error("preparing strings", len(requests))

        return requests

    def collect_data(self, slon, record_type):
        
        requests = self.prepare_data(slon, record_type)
        #Creating mp pool
        # pool = multiprocessing.Pool()
        # result = pool.map(self.download_worker, requests)
        
        with multiprocessing.Pool() as p:
            print(f"Current Solar Longitude: {slon} - Total work: {100*(slon/360)}%\n")
            result = list(tqdm(p.imap(self.download_worker, requests), total=len(requests)))
            consoleGUI.cls()

        for item in result:
            lat, lon, value = item
            if abs(lat) == 90:
                for step in np.arange(self.lon_margins[0], self.lon_margins[1]+self.settings_handler.get_setting("LON_STEP"), self.settings_handler.get_setting("LON_STEP")):
                    self.add_value_to_dict(lat, step, value)
            self.add_value_to_dict(lat, lon, value)
            

        return self.data

        #data = add_value_to_dict(data, lat, lon, current_value)

    def add_value_to_dict(self, lat, lon, value):
        if not lat in self.data.keys():
            self.data[lat] = {}
            self.data[lat] = {lon: value}
        else:
            self.data[lat][lon] = value

    def download_worker(self, data):
        lat, lon, uri = data
        current_value = self.mcd_interface.do_direct_query(uri)
        return (lat, lon, current_value)

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


    

    
            