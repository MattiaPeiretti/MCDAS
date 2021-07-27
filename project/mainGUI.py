from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import project.GUI.MCDAS_GUI_lib as GUI
from project.settingsHandler import SettingsHandler

settings_handler = SettingsHandler()


class DownloadPage(GUI.CustomPage):
    def build(self):
        self.set_page_title("Download from MCD")
        self.page_body.addWidget(QLabel("This is a custom label."))


class SettingsPage(GUI.CustomPage):
    def build(self):
        self.set_page_title("Settings")
        self.page_body.addWidget(QLabel("This is a custom label."))
        settings_data = settings_handler.get_settings_template_data()
        for section in settings_data:
            print(section)
            self.page_body.addWidget(QLabel(section["title"]))


if __name__ == "__main__":

    app = QApplication([])
    ex = GUI.root()
    ex.insert_page(DownloadPage(), "Download")
    ex.insert_page(SettingsPage(), "Settings")
    ex.initialize(displayDebugBorders=False)
    ex.resize(700, 500)
    ex.show()
    app.exec()
