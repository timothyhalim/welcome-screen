execfile(r"C:\Users\timothy.septianjaya\Documents\Timo\Scripts\DCC\WelcomeScreen\main\component\SplashScreen.py")
execfile(r"C:\Users\timothy.septianjaya\Documents\Timo\Scripts\DCC\WelcomeScreen\main\component\FileBrowser.py")
execfile(r"C:\Users\timothy.septianjaya\Documents\Timo\Scripts\DCC\WelcomeScreen\main\component\RecentList.py")

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
    qttype = "PySide2"
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    qttype = "PySide"

class WS(SplashScreen):
    def __init__(self, parent=None):
        super(WS, self).__init__(parent)
        self.setObjectName("WS")
        self.setup_ui()

    def setup_ui(self):
        self.master_layout = QVBoxLayout(self.master_widget)
        self.master_layout.setContentsMargins(0,0,0,15)
        self.content_widget = QStackedWidget()
        self.master_layout.addWidget(self.content_widget)

        self.setup_filebrowser_widget()
        self.setup_recent_widget()
        self.setup_settings_widget()
        self.setup_about_widget()
        
    def setup_filebrowser_widget(self):
        self.filebrowser_widget = FileBrowser()
        # self.filebrowser_widget.executed.connect(self.open_cmd)

        self.content_widget.addWidget(self.filebrowser_widget)

    def setup_recent_widget(self):
        self.recent_widget = QWidget()
        self.recent_search = QLineEdit()
        self.recent_search.setStyleSheet("""color:rgb(180, 180, 180); 
                                            padding:4px 4px 4px 20px; 
                                            background-image:url(search.png); 
                                            background-color:rgb(50, 50, 50); 
                                            background-position: left; 
                                            background-repeat:no-repeat""")
        self.recent_search.setPlaceholderText("Search Recent Files")

        self.recent_list = RecentList()

        self.recent_widget_layout = QVBoxLayout(self.recent_widget)
        self.recent_widget_layout.setContentsMargins(0,0,0,0)
        self.recent_widget_layout.addWidget(self.recent_search)
        self.recent_widget_layout.addWidget(self.recent_list)
        
        # Signal
        # self.recent_search.textChanged.connect(self.update_recent_file_list)
        # self.recent_list.fileClicked.connect(self.open_cmd)
        
        self.content_widget.addWidget(self.recent_widget)

    def setup_settings_widget(self):
        self.settings_widget = QWidget()
        self.settings_label = QLabel("Settings:")
        self.settings_label.setFont(QFont("Arial", 11))
        self.settings_label.setStyleSheet("color:rgb(180, 180, 180)")
        self.settings_label_layout = QHBoxLayout()
        self.settings_label_layout.addWidget(self.settings_label)
        self.settings_label_layout.addStretch()
        
        self.settings_show_on_startup = QCheckBox("Show Welcome Screen at Startup")
        self.settings_fullscreen = QCheckBox("Full Screen Welcome Screen")
        self.settings_open_new_window = QCheckBox("Open file in New Window")
        self.settings_close_on_open = QCheckBox("Close Welcome Screen after Opening file")

        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.settings_layout.setContentsMargins(0,0,0,0)
        self.settings_layout.setSpacing(10)
        self.settings_layout.addLayout(self.settings_label_layout)
        self.settings_layout.addSpacing(7)
        for w in (self.settings_show_on_startup, self.settings_fullscreen, self.settings_open_new_window, self.settings_close_on_open):
            w.setFont(QFont("Arial", 10))
            self.settings_layout.addWidget(w)
            # w.clicked.connect(self.update_settings)
        # self.settings_fullscreen.clicked.connect(self.change_resolution)
        self.settings_layout.addStretch() 

        self.content_widget.addWidget(self.settings_widget)

    def setup_about_widget(self):
        self.about_widget = QWidget()
        self.about_label_layout = QHBoxLayout()
        self.about_label_layout.addStretch()
        
        self.about_welcome_screen = QLabel("Welcome Screen v1.0")
        self.about_welcome_screen.setFont(QFont("Arial", 20))
        self.about_author = QLabel("Timothy Halim Septianjaya")
        self.about_author.setFont(QFont("Arial", 11))
        self.about_web = QLabel()
        self.about_web.setText('''<a href="http://timo.ink" style="color:#FFC132;text-decoration: none;">Home Page</a>''')
        self.about_web.setOpenExternalLinks(True)
        self.about_web.setFont(QFont("Arial", 11))
        
        self.about_layout = QVBoxLayout(self.about_widget)
        self.about_layout.setSpacing(10)
        self.about_layout.addLayout(self.about_label_layout)
        self.about_layout.addStretch()
        for w in (self.about_welcome_screen, self.about_author, self.about_web):
            w.setAlignment(Qt.AlignCenter)
            self.about_layout.addWidget(w)
        self.about_layout.addStretch()

        self.content_widget.addWidget(self.about_widget)
        

w = WS()
w.start()