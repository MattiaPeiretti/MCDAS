from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import project.GUI.MCDAS_GUI_lib as GUI
from project.settingsHandler import SettingsHandler

settings_handler = SettingsHandler()


class HRangeSelector(QWidget):
    def __init__(self, title, *args, **kwargs):
        super(HRangeSelector, self).__init__()
        self.title = title
        self.build_widget()

    def build_widget(self):

        layout = QHBoxLayout()
        layout.addWidget(QLabel(self.title))
        self.begin_value_lineedit = QLineEdit(objectName="coordinates-lineedit")
        self.begin_value_lineedit.setValidator(QDoubleValidator(self))
        layout.addWidget(self.begin_value_lineedit)
        range_layout = QHBoxLayout()
        to_label = QLabel(" to ")
        range_layout.addWidget(to_label)
        self.end_value_lineedit = QLineEdit(objectName="coordinates-lineedit")
        self.end_value_lineedit.setValidator(QDoubleValidator(self))
        range_layout.setContentsMargins(0, 0, 0, 0)
        range_layout.addWidget(self.end_value_lineedit)
        range_layout_frame = QFrame()
        range_layout_frame.setLayout(range_layout)
        range_layout_frame.hide()
        layout.addWidget(range_layout_frame)

        def update_buttons_config():
            if range_layout_frame.isHidden():
                range_layout_frame.show()
                toggle_range_button.setText("Remove range value")
            else:
                range_layout_frame.hide()
                toggle_range_button.setText("Add range value")
                self.end_value_lineedit.setText("")

        toggle_range_button = QPushButton(
            "Add Range Value", clicked=update_buttons_config
        )

        layout.addWidget(toggle_range_button)
        layout.addStretch(1)

        self.setLayout(layout)

    def get_value(self):
        if not self.end_value_lineedit.text() == "":
            return [
                float(self.begin_value_lineedit.text()),
                float(self.end_value_lineedit.text()),
            ]
        if self.begin_value_lineedit.text() == "":
            return False

        return float(self.begin_value_lineedit.text())


class DownloadPage(GUI.CustomPage):
    def build(self):
        self.set_page_title("Download from MCD")

        coordinates_box = QGroupBox("Coordinates")
        coordinates_main_layout = QVBoxLayout()

        slon_range = HRangeSelector("Solar longitude (0° to 360°):")
        lat_range = HRangeSelector("Latitude (-90° to 90°) deg:")
        lon_range = HRangeSelector("Solar longitude (0° to 360°) deg:")

        coordinates_main_layout.addWidget(slon_range)
        coordinates_main_layout.addWidget(lat_range)
        coordinates_main_layout.addWidget(lon_range)

        def get_rages_value():
            print(slon_range.get_value(), lat_range.get_value(), lon_range.get_value())

        coordinates_main_layout.addWidget(
            QPushButton("Get Values", clicked=get_rages_value)
        )
        coordinates_box.setLayout(coordinates_main_layout)
        self.page_body.addWidget(coordinates_box)


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
