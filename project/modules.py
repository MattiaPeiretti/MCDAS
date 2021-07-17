from dataHandler import dataHandler
import formulas
import dataHandler
from settingsHandler import SettingsHandler
from mcd_interface import MCDInterface
import os
import numpy as np
from tqdm import tqdm
import multiprocessing


LAT_MARGINS = [-90, 90]
LON_MARGINS = [0, 360]

settings_handler = SettingsHandler()
mcd_interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))
data_hander = dataHandler.dataHandler(
    "../output/", settings_handler, mcd_interface, LAT_MARGINS, LON_MARGINS
)

TSURFMX_DIR = "../data/tsurfmx/"


def convert_W2K_module():

    pass


def worker(data):
    lat, lon, k_value = data
    w_data = formulas.convert_K2W(k_value)
    return (lat, lon, k_value, w_data)


def convert_K2W_module():
    data_to_process = []
    processed_matrix = []
    for filename in os.listdir(TSURFMX_DIR):
        if filename.endswith(".csv"):
            file = str(TSURFMX_DIR + filename)
            for row in data_hander.read_matrix_from_csv(file):
                data_to_process.append((row[0], row[1], row[2]))
        print("Processing", len(data_to_process), "rows.")
        break

    with multiprocessing.Pool(30) as p:
        print("Converting...")
        result = list(
            tqdm(p.imap(worker, data_to_process[1:]), total=len(data_to_process))
        )
    print("Creating Matrix")
    for count, item in enumerate(result):
        lat, lon, k_value, w_value = item
        processed_matrix.append([lat, lon, k_value, w_value])
    print("Saving")
    data_hander.write_matrix_to_csv(
        TSURFMX_DIR + "processed/",
        "test.csv",
        processed_matrix,
        ["Latitude", "Longitude", "Tsurfmx", "Watt/m2"],
    )
