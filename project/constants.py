
# ==== PHYSICS CONSTANTS ====

# BOLTZMAN
BOLTZMAN_CONSTANT = 5.6704 * (10 ** -8)

# KELVIN
DELTA_KELVIN = 273.15


# ==== SOFTWARE RELATED ====

LAT_MARGINS = [-90, 90]
LON_MARGINS = [0, 360]
LON_STEPS_PER_LAT = 145

TABLE_HEADER = [
    "Latitude",
    "Longitude",
    "Tsurfmx",
    "Tsurfmn",
    "Tsurfmx_Watt/m2",
    "Tsurfmn_Watt/m2",
    "AVG_Watt/m2",
    "Lat_AVG_Tsurfmx_Watt/m2",
    "Lat_AVG_Tsurfmn_Watt/m2",
    "Lat_AVG_Watt/m2",
    "Lat_Max_Tsurfmx_Watt/m2",
    "Lat_Min_Tsurfmn_Watt/m2",
]

TSURFMX_DIR = "../data/tsurfmx/"
TSURFMN_DIR = "../data/tsurfmn/"