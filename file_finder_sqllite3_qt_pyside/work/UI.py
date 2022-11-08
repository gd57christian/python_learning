from PySide import QtGui, QtCore

import config
import core

class FileFinder(QtGui.QMainWindow):
    """
    main UI class
    """
    # global class variables
    window_height = 470
    window_width = 810
    ui_blue_color = "#1BAAF2"

    def __init__(self):
        super(FileFinder, self).__init__()

        # initializing program variables
        self.file_list = []
        self.file_type = ""

        # configuring the main window
        self.config_window()

        #configuring the widgets
        self.create_widgets()

        # configuring the layout of the window
        self.create_layout()

        # configuring the connections
        self.create_connections()

    def config_window(self):
        """
        Function to set values to the windows
        """
        # set the title of the window
        self.setWindowTitle("File Finder")

        # set the size of the window
        self.setFixedSize(FileFinder.window_width, FileFinder.window_height)

    def create_widgets(self):
        """
        Creating all the widgets in the windows
        """
        # create label file type
        self.label_file_type = QtGui.QLabel("File Type")
        self.label_file_type.setAlignment(QtCore.Qt.AlignCenter)

        # create a combobox
        self.combobox_file_type = QtGui.QComboBox()
        self.combobox_file_type.setFixedSize(200, 25)
        self.combobox_file_type.addItems(config.SUPPORTED_FILE_TYPES)

        # create a search button
        self.pushbutton_search = QtGui.QPushButton("Search")
        self.pushbutton_search.setFixedSize(200, 35)
        self.pushbutton_search.setStyleSheet("background-color : %s" %FileFinder.ui_blue_color)

        # create a separator
        self.separator = QtGui.QFrame()
        self.separator.setFrameShape(QtGui.QFrame.HLine)
        self.separator.setFixedSize(500, 10)
        self.separator.setLineWidth(5)
        # todo separator aesthetic

        #create label found files
        self.label_found_files = QtGui.QLabel("Found Files")
        self.label_found_files.setAlignment(QtCore.Qt.AlignCenter)

        #create a listWidget
        self.list_found_files = QtGui.QListWidget()
        self.list_found_files.setFixedWidth(700)

        # create submit button
        self.pushbutton_submit = QtGui.QPushButton("Submit")
        self.pushbutton_submit.setFixedSize(200, 35)
        self.pushbutton_submit.setEnabled(False)

    def create_layout(self):
        """
        Setting the layout of the widgets
        """
        # initialize the central widget
        self.central_widget = QtGui.QWidget()
        self.setCentralWidget(self.central_widget)

        # set the main layout for the central widget
        self.main_layout = QtGui.QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.setSpacing(12)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        # set the file type label in the layout
        self.main_layout.addWidget(self.label_file_type)

        # set the combobox in the layout
        self.main_layout.addWidget(self.combobox_file_type)
        self.main_layout.setAlignment(self.combobox_file_type, QtCore.Qt.AlignHCenter)

        # set the search button in the layout
        self.main_layout.addWidget(self.pushbutton_search)
        self.main_layout.setAlignment(self.pushbutton_search, QtCore.Qt.AlignHCenter)

        #set the separator in the layout
        self.main_layout.addWidget(self.separator)
        self.main_layout.setAlignment(self.separator, QtCore.Qt.AlignHCenter)

        # set the found files label in the layout
        self.main_layout.addWidget(self.label_found_files)

        # set the list widget in the layout
        self.main_layout.addWidget(self.list_found_files)
        self.main_layout.setAlignment(self.list_found_files, QtCore.Qt.AlignHCenter)

        # set a sub layout to adjust the submit button in the window
        self.sub_layout = QtGui.QHBoxLayout()

        # set the submit button in the layout
        self.sub_layout.addWidget(self.pushbutton_submit)
        self.sub_layout.setAlignment(self.pushbutton_submit, QtCore.Qt.AlignRight)
        self.sub_layout.addSpacing(39)
        self.main_layout.addLayout(self.sub_layout)

    def create_connections(self):
        """
        Creating connections to the widgets
        """
        self.pushbutton_search.pressed.connect(self.search_pushbutton_pressed)
        self.pushbutton_submit.pressed.connect(self.submit_pushbutton_pressed)

    def search_pushbutton_pressed(self):
        """
        search button pressed:
            fill the list widget and enable submit button
        """
        self.file_type = self.combobox_file_type.currentText()
        self.file_list = core.search_file_type(config.SEARCH_DIRECTORY_ROOT,self.file_type)
        self.list_found_files.clear()
        if self.file_list:
            for item in self.file_list:
                file_item = QtGui.QListWidgetItem(item)
                self.list_found_files.addItem(file_item)
            self.pushbutton_submit.setEnabled(True)
            self.pushbutton_submit.setStyleSheet("background-color : %s" %FileFinder.ui_blue_color)
        else:
            self.pushbutton_submit.setEnabled(False)
            self.pushbutton_submit.setStyleSheet("background-color : gray")

    def submit_pushbutton_pressed(self):
        """
        submit pushbutton pressed:
            create a database file with the list_found_files and disable submit button
        """
        core.add_database(config.DATABASE_FILE, self.file_list, self.file_type)
        messagebox_confirm = QtGui.QMessageBox.information(self,
                                                           "Information Dialog",
                                                           "Success\nFile/s Entered into\nDatabase",
                                                           buttons=QtGui.QMessageBox.Ok,
                                                           defaultButton=QtGui.QMessageBox.Ok)