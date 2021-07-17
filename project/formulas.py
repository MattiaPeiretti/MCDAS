import constants

# Kelvin temp to Watt/m2
def convert_K2W(k_value):
    return constants.BOLTZMAN_CONSTANT * (k_value ** 4)


# Watt/m2 to kelvin temp
def convert_W2K(w_value):
    return (w_value / constants.BOLTZMAN_CONSTANT) ** (1 / 4)
