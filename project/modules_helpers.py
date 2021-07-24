import os
import multiprocessing
from tqdm import tqdm

# Custom Modules
import constants
import formulas
from dataHandler import dataHandler
from settingsHandler import SettingsHandler
from mcd_interface import MCDInterface

settings_handler = SettingsHandler()
mcd_interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))
data_hander = dataHandler(
    "../output/",
    settings_handler,
    mcd_interface,
    constants.LAT_MARGINS,
    constants.LON_MARGINS,
)


def load_dataset(dataset_dir):
    data = {}
    for filename in os.scandir(dataset_dir):
        if filename.is_file():
            current_file_data = []
            if filename.name.endswith(".csv"):
                file = str(dataset_dir + filename.name)
                for row in data_hander.read_matrix_from_csv(file):
                    current_file_data.append([row[0], row[1], row[2]])
            data[filename.name] = current_file_data
    print("Read ", len(data), "files.")

    return data


def execute_parallel(func, data_to_process, workers_amount=10):
    with multiprocessing.Pool(workers_amount) as p:
        print("Converting...")
        result = list(tqdm(p.imap(func, data_to_process), total=len(data_to_process)))
    return result


class workers:
    # This class contains all of the different workers needed for the parallel working.
    @staticmethod
    def worker_k2w_converter(data):
        lat = data[0]
        lon = data[1]
        k_value = data[2]
        w_data = formulas.convert_K2W(k_value)
        return (lat, lon, k_value, w_data)

    @staticmethod
    def worker_w_avg_calculator(data):
        w2_tsurfmn = data[4]
        w2_tsurfmx = data[5]
        return (w2_tsurfmx + w2_tsurfmn) / 2


def find_indexes(array, coord):
    for count, item in enumerate(array):
        if item[0] == coord[0]:
            if item[1] == coord[1]:
                return count
