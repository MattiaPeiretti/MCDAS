import project.constants as constants
import project.settingsHandler as settingsHandler

from tqdm import tqdm
import csv
import os
import numpy as np
import multiprocessing


def print_data(GUI, slon, lat, lon, current_value):
    GUI.update(slon, lat, lon, current_value)


def cls():
    os.system("cls" if os.name == "nt" else "clear")


class dataHandler:
    def __init__(self):
        self.settings_handler = settingsHandler.SettingsHandler()
        self.data = {}

    def __add_value_to_dict(self, lat, lon, value):
        if not lat in self.data.keys():
            self.data[lat] = {}
            self.data[lat] = {lon: value}
        else:
            self.data[lat][lon] = value

    def __prepare_data(self, slon, record_type):
        # Geneates all of the URI from which all the data needs to be downloaded.

        requests = []

        lat_step = self.settings_handler.get_setting("LAT_STEP")
        lon_step = self.settings_handler.get_setting("LON_STEP")

        for lat in np.arange(
            constants.LAT_MARGINS[0], constants.LAT_MARGINS[1] + lat_step, lat_step
        ):

            # If currently checking the poles, we will assign the data of one point to the whole scale.
            if lat == constants.LAT_MARGINS[0] or lat == constants.LAT_MARGINS[1]:

                requests.append(
                    (
                        lat,
                        180,
                        self.mcd_interface.get_query_URI(slon, record_type, [lat, 180]),
                    )
                )
                continue

            for lon in np.arange(
                constants.LON_MARGINS[0], constants.LON_MARGINS[1] + lon_step, lon_step
            ):
                requests.append(
                    (
                        lat,
                        lon,
                        self.mcd_interface.get_query_URI(slon, record_type, [lat, lon]),
                    )
                )

        return requests

    def download_worker(self, data):
        lat, lon, uri = data
        current_value = self.mcd_interface.do_direct_query(uri)
        return (lat, lon, current_value)

    def collect_data(self, mcd_interface, slon, record_type):
        # Downloads all of the needed data from the database, making requests for every generated URI.
        self.mcd_interface = mcd_interface
        requests = self.__prepare_data(slon, record_type)

        with multiprocessing.Pool() as p:
            print(f"Current Solar Longitude: {slon} - Total work: {100*(slon/360)}%\n")
            result = list(
                tqdm(p.imap(self.download_worker, requests), total=len(requests))
            )

        for item in result:
            lat, lon, value = item
            if abs(lat) == 90:
                for step in np.arange(
                    constants.LON_MARGINS[0],
                    constants.LON_MARGINS[1]
                    + self.settings_handler.get_setting("LON_STEP"),
                    self.settings_handler.get_setting("LON_STEP"),
                ):
                    self.__add_value_to_dict(lat, step, value)
            self.__add_value_to_dict(lat, lon, value)

        return self.data

    def write_database_slon_record(self, record_type, slon, db_dict, dir_path):
        padded_slon = str(slon).rjust(
            self.settings_handler.get_setting("RECORDS_FILENAME_NUMBERS_PADDING"), "0"
        )
        filename = f"MCDas_{record_type}_LS{padded_slon}"

        with open(dir_path + filename + ".csv", mode="w", newline="") as csv_file:
            fieldnames = [
                "lat",
                "lon",
                self.settings_handler.get_setting("RECORD_TYPE"),
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for lat in db_dict:
                for lon in db_dict[lat]:
                    writer.writerow(
                        {
                            "lat": lat,
                            "lon": lon,
                            self.settings_handler.get_setting("RECORD_TYPE"): db_dict[
                                lat
                            ][lon],
                        }
                    )

    def write_matrix_to_csv(self, dir, filename, matrix, header):
        with open(dir + filename, mode="w", newline="") as csv_file:
            fieldnames = header
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for row in matrix:
                current_row_dict = {}

                for count in range(len(header)):
                    if not len(row) == count:
                        row.append("")
                    current_row_dict[header[count]] = row[count]
                writer.writerow(current_row_dict)

    def read_matrix_from_csv(self, csv_file, has_header=True):
        if has_header:
            return np.genfromtxt(csv_file, delimiter=",")[
                1:
            ]  # [1:] to remove the header, otherwise the header would be interpreted as nan
        return np.genfromtxt(csv_file, delimiter=",")
