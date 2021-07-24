from consolemenu import *
from consolemenu.items import *
import modules


class Modules:
    def __init__(self):
        self.modules = {}
        self.menu = ConsoleMenu("Modules", "Run code on the db data.")

    def register_module(self, module_name, module_func):
        self.modules[module_name] = module_func

    def run_module(self, module_name):
        self.modules[module_name]()

    def print_menu(self):
        self.menu = SelectionMenu(self.modules.keys(), "Run Module:")

        self.menu.show()
        self.menu.join()
        selection = list(self.modules.keys())[self.menu.selected_option]
        self.run_module(selection)


if __name__ == "__main__":
    modulesHandler = Modules()
    modulesHandler.register_module("Convert Watt to Kelvin", modules.convert_W2K_module)
    modulesHandler.register_module("Convert Kelvin to Watt", modules.convert_K2W_module)
    modulesHandler.register_module(
        "Check for faulty values in the dataset",
        modules.check_for_faulty_values_in_dataset,
    )
    modulesHandler.print_menu()
