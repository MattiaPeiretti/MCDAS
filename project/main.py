from settingsHandler import SettingsHandler
from mcd_interface import MCDInterface
from dataHandler import dataHandler
import numpy as np


LAT_MARGINS = [-90, 90] 
LON_MARGINS = [0, 360] 


if __name__ == "__main__":

    settings_handler = SettingsHandler()
    mcd_interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))
    data_hander = dataHandler("../output/", settings_handler, mcd_interface)

    # ===== Downloading data ======

    record_type = settings_handler.get_setting("RECORD_TYPE")
    slon_step = settings_handler.get_setting("SLON_STEP")


    for slon in np.arange(0, 360 + slon_step, slon_step):
        data = data_hander.collect_data(slon, LAT_MARGINS, LON_MARGINS, record_type)
        data_hander.write_database_slon_record(record_type, slon, data)