# ==== PHYSICS CONSTANTS ====

# BOLTZMAN
BOLTZMAN_CONSTANT = 5.6704 * (10 ** -8)

# KELVIN
DELTA_KELVIN = 273.15


# ==== SOFTWARE RELATED ====

SETTINGS_FILE_PATH = "settings.json"
SETTINGS_TEMPLATE_FILE_PATH = "settingsTemplate.json"

# ==== BASE SCI CONSTANTS ====

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

VALID_RECORD_TYPES = [
    "t",
    "p",
    "rho",
    "wind",
    "w",
    "u",
    "v",
    "tsurf",
    "ps",
    "tau",
    "qdust",
    "rdust",
    "sdust",
    "mtot",
    "icetot",
    "h2ovap",
    "h2oice",
    "rice",
    "co2ice",
    "groundice",
    "pbl",
    "stress",
    "updraft",
    "downdraft",
    "pblwvar",
    "pblhvar",
    "ps_ddv",
    "p_ddv",
    "t_ddv",
    "u_ddv",
    "v_ddv",
    "w_ddv",
    "rho_ddv",
    "tau_ddv",
    "tsurfmx",
    "tsurfmn",
    "lwdown",
    "swdown",
    "lwup",
    "swup",
    "co2col",
    "arcol",
    "n2col",
    "cocol",
    "o3col",
    "co2",
    "ar",
    "n2",
    "co",
    "o3",
    "o",
    "o2",
    "hydro",
    "hydro2",
    "e",
    "ecol",
    "hecol",
    "he",
    "cp",
    "visc",
]


RECORD_TYPES_TABLE = {
    "t": "selected=" ">Temperature (K)",
    "p": "Pressure (Pa)",
    "rho": "Density (kg/m3)",
    "wind": "Horizontal wind (m/s)",
    "w": "Vertical wind (m/s, pos. when downward)",
    "u": "W-E wind component (m/s)",
    "v": "S-N wind component (m/s)",
    "tsurf": "Surface temperature (K)",
    "ps": "Surface pressure (Pa)",
    "tau": "Dust column vis opt depth above surf",
    "qdust": "Dust mass mixing ratio (kg/kg)",
    "rdust": "Dust effective radius (m)",
    "sdust": "Dust deposition on flat surface (kg/m2/s)",
    "mtot": "Water vapor column (kg/m2)",
    "icetot": "Water cloud ice column (kg/m2)",
    "h2ovap": "Water vapor vol. mixing ratio (mol/mol)",
    "h2oice": "Water ice mixing ratio (mol/mol)",
    "rice": "Water ice effective radius (m)",
    "co2ice": "surface CO2 ice layer (kg/m2)",
    "groundice": "surface H2O ice layer (kg/m2, 0.5: perennial)",
    "pbl": "Convective PBL height (m)",
    "stress": "Surf. wind stress (Kg/m/s2)",
    "updraft": "Max PBL updraft wind (m/s)",
    "downdraft": "Max PBL downdraft wind (m/s)",
    "pblwvar": "PBL vert wind variance (m2/s2)",
    "pblhvar": "PBL eddy vert heat flux (m/s/K)",
    "ps_ddv": "Surf. pres. day to day variability (Pa)",
    "p_ddv": "Pressure day to day variability (Pa)",
    "t_ddv": "Temperature day to day variability (K)",
    "u_ddv": "zonal wind day to day variability (m/s)",
    "v_ddv": "merid. wind day to day variability (m/s)",
    "w_ddv": "vert. wind day to day variability (m/s)",
    "rho_ddv": "density day to day variability (kg/m^3)",
    "tau_ddv": "Dust column day to day variability",
    "tsurfmx": "daily max mean surf temperature (K)",
    "tsurfmn": "daily min mean surf temperature (K)",
    "lwdown": "thermal IR flux to surface (W/m2)",
    "swdown": "solar flux to surface (W/m2)",
    "lwup": "thermal IR flux to space (W/m2)",
    "swup": "solar flux reflected to space (W/m2)",
    "co2col": "CO2 column (kg/m2)",
    "arcol": "Ar column (kg/m2)",
    "n2col": "N2 column (kg/m2)",
    "cocol": "CO column (kg/m2)",
    "o3col": "O3 column (kg/m2)",
    "co2": "[CO2] vol. mixing ratio (mol/mol)",
    "ar": "[Ar] vol. mixing ratio (mol/mol)",
    "n2": "[N2] vol. mixing ratio (mol/mol)",
    "co": "[CO] vol. mixing ratio (mol/mol)",
    "o3": "[O3] ozone vol. mixing ratio (mol/mol)",
    "o": "[O] vol. mixing ratio (mol/mol)",
    "o2": "[O2] vol. mixing ratio (mol/mol)",
    "hydro": "[H] vol. mixing ratio (mol/mol)",
    "hydro2": "[H2] vol. mixing ratio (mol/mol)",
    "e": "electron number density (cm-3)",
    "ecol": "Total Electronic Content (TEC) (m-2)",
    "hecol": "He column (kg/m2)",
    "he": "[He] vol. mixing ratio (mol/mol)",
    "cp": "Air heat capacity Cp (J kg-1 K-1)",
    "visc": "Air viscosity estimation (N s m-2)",
}
