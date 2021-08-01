from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial
import os
import glob

import project.GUI.custom_widgets as CustomWidgets


def parse_css_files(files=[]):
    styles = """"""
    for file in files:
        if not os.path.isfile(file):
            print(f"File: {file} does not exist.")
            continue
        with open(file, "r") as file_stream:
            styles += file_stream.read()
            print(f"Loaded {file}.")
    return styles


def load_font_files(dirs=[]):
    for dir_location in dirs:
        if not os.path.isdir(dir_location):
            print(f"File: {dir_location} does not exist.")
            continue
        for file in glob.glob(dir_location + "*.ttf"):
            QFontDatabase.addApplicationFont(file)
            print(f"Loaded {file} font file.")


class root(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mars Climate Database Augmented Software")

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("pageBody")

        self.header = QHBoxLayout()

        self.page_title_label = QLabel("Loading...")
        self.page_title_label.setObjectName("PageHeaderLabel")
        self.header.addWidget(self.page_title_label)
        self.header.addStretch(0)

        self.pages_register = {}
        self.navbar_buttons = []
        self.page_titles = {}

        css_files = [os.path.join(os.path.dirname(__file__), "default.css")]
        self.styles = parse_css_files(css_files)
        self.setStyleSheet(self.styles)

        fonts_dirs = [os.path.join(os.path.dirname(__file__), "fonts/roboto/")]
        load_font_files(fonts_dirs)

    def update_header(self, index):
        self.page_title_label.setText(self.page_titles[index])
        for count, button in enumerate(self.navbar_buttons):
            if not count == index:
                button.setStyleSheet("color: white;")
            else:
                button.setStyleSheet("color: #6495ED;")

    def insert_page(self, widget, name):
        index = len(self.pages_register)
        self.stacked_widget.insertWidget(index, widget)
        self.pages_register[index] = name
        if hasattr(widget, "name"):
            self.page_titles[index] = widget.name
        else:
            self.page_titles[index] = "Untitled Page"
        self.update_header(self.stacked_widget.currentIndex())

    def generate_navbar(self):
        for index, button_name in self.pages_register.items():
            button = QPushButton(button_name)
            button.setObjectName("NavbarButton")
            button.clicked.connect(partial(self.stacked_widget.setCurrentIndex, index))
            button.setCursor(QCursor(Qt.PointingHandCursor))
            self.navbar_buttons.append(button)
            self.header.addWidget(button)

    def initialize(self, displayDebugBorders=False):
        if displayDebugBorders:
            self.styles += "QWidget {border: 1px solid red!important;}"
            self.setStyleSheet(self.styles)

        self.body = QVBoxLayout()

        self.generate_navbar()
        self.body.addLayout(self.header)

        self.body.addWidget(self.stacked_widget)
        self.stacked_widget.currentChanged.connect(self.update_header)

        self.update_header(0)
        self.setLayout(self.body)


class CustomPage(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "Untitled Page"
        self.page_body = QVBoxLayout()
        self.page_body.setAlignment(Qt.AlignTop)

        self.build()

        self.page_body.addStretch()
        self.setLayout(self.page_body)

    def build(self):
        return

    def set_page_title(self, title):
        self.name = title
