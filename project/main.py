from settingsHandler import SettingsHandler
from mcd_interface import MCDInterface
from dataHandler import dataHandler

LAT_MARGINS = [-90, 90] 
LON_MARGINS = [0, 360] 

data = {}

def add_value_to_dict(dict, lat, lon, value):
    if lat in dict.keys():
        dictdata = dict[lat]
        dictdata[lon] = value
        dict[lat] = dictdata
    else:
        dict[lat] = {lon:  current_value}
    return dict

if __name__ == "__main__":

    settings_handler = SettingsHandler()
    mcd_interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))
    data_hander = dataHandler("../output/", settings_handler)

    # ===== Downloading data ======
    
    slon = 56

    lat_step = settings_handler.get_setting("LAT_STEP")
    lon_step = settings_handler.get_setting("LON_STEP")
    record_type = settings_handler.get_setting("RECORD_TYPE")

    for lat in range(LAT_MARGINS[0], LAT_MARGINS[1] + lat_step, lat_step):

        # If currently checking the poles, we will assign the data of one point to the whole scale.
        if lat == LAT_MARGINS[0] or lat == LAT_MARGINS[1]:

            current_value = mcd_interface.do_query(slon, record_type, [lat, 180])

            for lon in range(LON_MARGINS[0], LON_MARGINS[1] + lon_step, lon_step):
                data = add_value_to_dict(data, lat, lon, current_value)

                print(lat, lon, current_value)
            continue

        for lon in range(LON_MARGINS[0], LON_MARGINS[1] + lon_step, lon_step):
            current_value = mcd_interface.do_query(slon, record_type, [lat, lon])

            data = add_value_to_dict(data, lat, lon, current_value)

            print(lat, lon, current_value)
    
    data_hander.write_database_slon_record(record_type, slon, data)