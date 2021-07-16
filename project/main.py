from settingsHandler import SettingsHandler
from mcd_interface import MCDInterface
from dataHandler import dataHandler
import numpy as np
import sys

if __name__ == "__main__":

    try:
        if not sys.argv[1] and not sys.argv[2]:
            LAT_MARGINS = [-90, 90] 
        if not sys.argv[3] and not sys.argv[4]:
            LON_MARGINS = [0, 360]
    except ValueError:
        pass
    else:
        LAT_MARGINS = [float(sys.argv[1]), float(sys.argv[2])] 
        LON_MARGINS = [float(sys.argv[3]), float(sys.argv[4])] 

    settings_handler = SettingsHandler()
    mcd_interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))
    data_hander = dataHandler("../output/", settings_handler, mcd_interface, LAT_MARGINS, LON_MARGINS)

    # ===== Downloading data ======

    record_type = settings_handler.get_setting("RECORD_TYPE")
    slon_step = settings_handler.get_setting("SLON_STEP")


    for slon in np.arange(0, 360 + slon_step, slon_step):
        data = data_hander.collect_data(slon, record_type)
        data_hander.write_database_slon_record(record_type, slon, data)