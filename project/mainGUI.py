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
        # Initializing page
        self.set_page_title("Settings")

        self.active_settings_components = {}
        settings_data = settings_handler.get_settings_template_data()

        for section in settings_data:
            self.page_body.addWidget(
                QLabel(section["title"], objectName="settings-title")
            )

            for setting in section["settings"]:

                settings_component = None

                if setting["type"] == "number":
                    settings_component = QSpinBox()
                    settings_component.setValue(setting["default"])

                elif setting["type"] == "list":
                    settings_component = QComboBox()
                    settings_component.addItems(setting["items"])
                    settings_component.setCurrentIndex(setting["default"])

                elif setting["type"] == "checkbox":
                    settings_component = QCheckBox(setting["label"])
                    settings_component.setChecked(setting["default"])

                elif setting["type"] == "input":
                    settings_component = QLineEdit(setting["default"])

                settings_component.setObjectName("SettingsWidgets")

                self.active_settings_components[setting["id"]] = {
                    "component": settings_component,
                    "type": setting["type"],
                }
                layout = QGridLayout()

                layout.setObjectName("setting-container")
                layout.addWidget(QLabel(setting["name"]), 0, 0)
                layout.addWidget(settings_component, 0, 1)

                layout.addWidget(QLabel(setting["desc"]), 1, 0, 1, 2)

                layout.addWidget(
                    GUI.CustomWidgets.QHSeparator(objectName="separator"), 2, 0, 1, 2
                )

                self.page_body.addLayout(layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(QPushButton("Apply", clicked=self.apply_settings))
        self.page_body.addLayout(buttons_layout)

    def apply_settings(self):

        for setting, data in self.active_settings_components.items():
            component = data["component"]
            data_type = data["type"]

            if data_type == "number":
                print(setting, component.value())
                settings_handler.update_setting(setting, component.value())
            elif data_type == "list":
                print(setting, component.currentText())
                settings_handler.update_setting(setting, component.currentText())
            elif data_type == "checkbox":
                print(setting, component.isChecked())
                settings_handler.update_setting(setting, component.isChecked())
            elif data_type == "input":
                print(setting, component.text())
                settings_handler.update_setting(setting, str(component.text()))


if __name__ == "__main__":

    app = QApplication([])
    ex = GUI.root()
    ex.insert_page(DownloadPage(), "Download")
    ex.insert_page(SettingsPage(), "Settings")
    ex.initialize(displayDebugBorders=False)
    ex.resize(700, 500)
    ex.show()
    app.exec()
