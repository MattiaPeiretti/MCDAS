from dataHandler import dataHandler
from settingsHandler import SettingsHandler
from mcd_interface import MCDInterface
import dataHandler
import constants
import modules_helpers


from tqdm import tqdm
import os
from tkinter import *
import tkinter.filedialog


settings_handler = SettingsHandler()
mcd_interface = MCDInterface(settings_handler.get_setting("MCD_BASELINK"))
data_hander = dataHandler.dataHandler()


def convert_W2K_module():
    pass


def convert_K2W_module():
    tsurfmx_to_process = []
    tsurfmn_to_process = []

    # Loading datasets from folders
    tsurfmx_to_process = modules_helpers.load_dataset(constants.TSURFMN_DIR)[:1]
    tsurfmn_to_process = modules_helpers.load_dataset(constants.TSURFMX_DIR)[:1]

    # Starting the conversions

    print("K to W/m2 conversion of tsuftmn")
    tsurfmn = modules_helpers.execute_parallel(
        modules_helpers.workers.worker_k2w_converter, tsurfmx_to_process, 18
    )

    print("K to W/m2 conversion of tsuftmx")
    tsurfmx = modules_helpers.execute_parallel(
        modules_helpers.workers.worker_k2w_converter, tsurfmn_to_process, 18
    )

    # Creating a matrix with all of the data loaded from the datasets in the form of a bi-dimentional table.

    print("Creating Matrix.")

    full_matrix = []

    for count, row in enumerate(tsurfmn):
        full_matrix.append(
            [row[0], row[1], row[2], tsurfmx[count][2], row[3], tsurfmx[count][3]]
        )

    # Proceeding to calculate averages...

    print("Calculating W/m2 temp average.")

    WTemp_average = modules_helpers.execute_parallel(
        modules_helpers.workers.worker_w_avg_calculator, full_matrix, 18
    )

    print("Adding AVG values to Matrix.")

    for count in range(len(full_matrix)):
        full_matrix[count].append(WTemp_average[count])

    print("Creating latitude average and excursions and adding it to the matrix.")
    AVG_full_matrix = []

    AVG_sum = 0
    max_lat = 0
    min_lat = 1000
    AVG_sum_max = 0
    AVG_sum_min = 0

    for count, row in enumerate(tqdm(full_matrix)):
        if not row[1] == 360:
            AVG_sum += row[6]
            AVG_sum_max += row[4]
            AVG_sum_min += row[5]
            if max_lat < row[4]:
                max_lat = row[4]
            if min_lat > row[5]:
                min_lat = row[5]
        else:
            # Adding the calculated data to the needed matrices.

            full_matrix[count].append(AVG_sum_max / (constants.LON_STEPS_PER_LAT - 1))
            full_matrix[count].append(AVG_sum_min / (constants.LON_STEPS_PER_LAT - 1))
            full_matrix[count].append(AVG_sum / (constants.LON_STEPS_PER_LAT - 1))
            full_matrix[count].append(max_lat)
            full_matrix[count].append(min_lat)

            AVG_full_matrix.append(full_matrix[count])

            # Resetting variables
            AVG_sum = 0
            AVG_sum_max = 0
            AVG_sum_min = 0
            max_lat = 0
            min_lat = 1000

    # Writing the calculated data to two different files.
    # The data is divided in two different tables, the first table contains all of the calculated data,
    # plus the data that was already in the dataset, and the second table contains the summed up data of
    # all of the calculated averages.

    print("Wriring extensive table file.")

    data_hander.write_matrix_to_csv(
        "../data/processed/", "full_lon.csv", full_matrix, constants.TABLE_HEADER
    )

    print("Wriring average summary table file.")

    data_hander.write_matrix_to_csv(
        "../data/processed/", "LAT_AVGs.csv", AVG_full_matrix, constants.TABLE_HEADER
    )


def check_for_faulty_values_in_dataset():
    Tk().withdraw()

    record_type = input(
        "Please insert the record type(MCD Variable, E.G. tsurfmn) that you would like to check: "
    )

    if not record_type in constants.VALID_RECORD_TYPES:
        print("That record type is not valid!")
        return -1

    print(
        "Please insert the path to the desired record type(MCD Variable, E.G. tsurfmn) that you would like to check: "
    )
    record_type_dir_path = tkinter.filedialog.askdirectory() + "/"

    if not os.path.exists(record_type_dir_path):
        print("Such path does not exist! Please try again.")
        return

    values_to_correct = []

    dataset = modules_helpers.load_dataset(record_type_dir_path)
    for key, record in tqdm(dataset.items()):
        for count, row in enumerate(record):
            if row[2] == 0:
                values_to_correct.append((key, row[0], row[1]))
    print(f"{len(values_to_correct)} faulty values have been found. \nCorrecting...")

    new_values = []

    for value in tqdm(values_to_correct):
        filename, lat, lon = value

        # Retrieving Solar Longitude from filename
        SL_position = filename.find("LS")
        slon = int(filename[SL_position + 2 : SL_position + 5])

        new_values.append(
            [
                filename,
                lat,
                lon,
                mcd_interface.do_direct_query(
                    mcd_interface.get_query_URI(
                        slon,
                        record_type,
                        [lat, lon],
                    )
                ),
            ]
        )
        # print(slon, lat, lon, new_value)
    corrected_lines = []
    for value in new_values:
        current_slon = dataset[value[0]]

        row_nr = modules_helpers.find_indexes(current_slon, [value[1], value[2]])
        corrected_lines.append((value[0], row_nr))

        dataset[value[0]][row_nr] = [value[1], value[2], value[3]]

    table_header = ["lat", "lon", record_type]

    print("Writing corrected files.")

    for filename, array in tqdm(dataset.items()):

        data_hander.write_matrix_to_csv(
            record_type_dir_path, filename, array, table_header
        )

    print("Corrected the following rows:")
    for row in corrected_lines:
        filename, row_rn_curr = row
        print(filename, row_rn_curr)
    # current_slon[current_slon.index(value[1])][
    #     current_slon.index(value[2])
    # ] = value[3]
