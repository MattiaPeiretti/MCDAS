from settingsHandler import SettingsHandler
from mcd_interface import MCDInterface
from dataHandler import dataHandler
import constants

import os
import numpy as np

if __name__ == "__main__":

    settings_handler = SettingsHandler()
    mcd_interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))
    data_hander = dataHandler()

    # ===== Downloading data ======

    record_type = settings_handler.get_setting("RECORD_TYPE")
    slon_step = settings_handler.get_setting("SLON_STEP")

    save_path = (
        settings_handler.get_setting("DATASET_DOWNLOAD_BASE_DIR")
        + settings_handler.get_setting("RECORD_TYPE")
        + "/"
    )

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for slon in np.arange(0, 360 + slon_step, slon_step):
        data = data_hander.collect_data(mcd_interface, slon, record_type)
        data_hander.write_database_slon_record(
            record_type,
            slon,
            data,
            save_path,
        )
