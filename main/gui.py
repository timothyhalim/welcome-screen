try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    
import os

from .component.IconLabel import IconLabel
from .component.FileBrowser import FileBrowser
from .component.RecentList import RecentList
from .component.SplashScreen import SplashScreen
from .config import APP, ICON_PATH, PROJECT, get_recent, save_recent, get_settings, save_settings

if APP == "NUKE":
    from ..app.nuke import command
    extfilter = ['*.nk']

elif APP == "MAYA":
    from ..app.maya import command
    extfilter = ['*.ma', '*.mb']

elif APP == "HOUDINI":
    from ..app.houdini import command
    extfilter = ['*.ma', '*.mb']

else:
    extfilter = []
    from app.other import command

class WelcomeScreen(SplashScreen):
    settings = get_settings()

    def __init__(self, parent=None):
        super(WelcomeScreen, self).__init__(parent, fullscreen=self.settings['full_screen'])
        self.setObjectName("WelcomeScreen")
        self.setup_ui()
        self.init_ui()

    def setup_ui(self):
        # Logo
        self.logo_height = 160
        self.logo = QLabel()
        self.logo.setMinimumHeight(self.logo_height)

        # Left Side
        self.new_btn = IconLabel(name="New", icon="new")
        self.open_btn = IconLabel(name="Open", icon="open")
        self.recent_btn = IconLabel(name="Recent", icon="history")
        self.setting_btn = IconLabel(name="Setting", icon="setting")
        self.about_btn = IconLabel(name="About...", icon="about")

        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0,0,0,0)
        for w in (self.new_btn, self.open_btn, self.recent_btn, self.setting_btn, self.about_btn):
            self.left_layout.addWidget(w)
        self.left_layout.addStretch()

        # Right Side
        self.content_widget = QStackedWidget()
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0,0,0,0)
        self.right_layout.addWidget(self.content_widget)

        self.setup_filebrowser_widget()
        self.setup_recent_widget()
        self.setup_settings_widget()
        self.setup_about_widget()

        # Signal
        self.connect(self.new_btn    , SIGNAL('clicked()'), self.new_cmd)
        self.connect(self.open_btn   , SIGNAL("clicked()"), lambda target=self.filebrowser_widget, sender=self.open_btn: self.switch_to(target, sender))
        self.connect(self.recent_btn , SIGNAL("clicked()"), lambda target=self.recent_widget, sender=self.recent_btn: self.switch_to(target, sender))
        self.connect(self.setting_btn, SIGNAL("clicked()"), lambda target=self.settings_widget, sender=self.setting_btn: self.switch_to(target, sender))
        self.connect(self.about_btn  , SIGNAL("clicked()"), lambda target=self.about_widget, sender=self.about_btn: self.switch_to(target, sender))
        
        # Add To Master Layout
        self.menu_layout = QHBoxLayout()
        self.menu_layout.setContentsMargins(0,0,0,0)
        self.menu_layout.addLayout(self.left_layout)
        self.menu_layout.addSpacing(15)
        self.menu_layout.addLayout(self.right_layout)
        
        self.master_layout = QVBoxLayout(self.master_widget)
        self.master_layout.setContentsMargins(0,0,0,15)
        self.master_layout.addWidget(self.logo)
        self.master_layout.addSpacing(10)
        self.master_layout.addLayout(self.menu_layout)

    def setup_filebrowser_widget(self):
        self.filebrowser_widget = FileBrowser(filterExtension=extfilter)
        self.filebrowser_widget.executed.connect(self.open_cmd)

        self.content_widget.addWidget(self.filebrowser_widget)

    def setup_recent_widget(self):
        self.recent_widget = QWidget()
        self.recent_search = QLineEdit()
        self.recent_search.setStyleSheet("""color:rgb(180, 180, 180); 
                                            padding:4px 4px 4px 20px; 
                                            background-image:url(%s/search.png); 
                                            background-color:rgb(50, 50, 50); 
                                            background-position: left; 
                                            background-repeat:no-repeat""" % ICON_PATH)
        self.recent_search.setPlaceholderText("Search Recent Files")

        self.recent_list = RecentList()

        self.recent_widget_layout = QVBoxLayout(self.recent_widget)
        self.recent_widget_layout.setContentsMargins(0,0,0,0)
        self.recent_widget_layout.addWidget(self.recent_search)
        self.recent_widget_layout.addWidget(self.recent_list)
        
        # Signal
        self.recent_search.textChanged.connect(self.update_recent_file_list)
        self.recent_list.fileClicked.connect(self.open_cmd)
        
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
            w.clicked.connect(self.update_settings)
        self.settings_fullscreen.clicked.connect(self.change_resolution)
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
        
    def init_ui(self):
        if hasattr(self, 'settings_widget'):
            self.settings_show_on_startup.setChecked(self.settings['startup_show'])
            self.settings_fullscreen.setChecked(self.settings['full_screen'])
            self.settings_close_on_open.setChecked(self.settings['close_on_open'])
            self.settings_open_new_window.setChecked(self.settings['new_window'])

        if hasattr(self, 'filebrowser_widget'):
            recent_files = get_recent()[PROJECT][APP]
            if recent_files:
                latest = max(recent_files, key=lambda k : k['access_date'] )
                self.filebrowser_widget.setRoot(os.path.dirname(latest['path']))
                self.filebrowser_widget.selectPath(latest['path'])

        if hasattr(self, 'recent_widget') and hasattr(self, 'recent_widget'):
            self.switch_to(self.recent_widget, self.recent_btn)
            self.update_recent_file_list()

    def paintEvent(self, QPaintEvent):
        super(WelcomeScreen, self).paintEvent(QPaintEvent)

        # Coordinate
        x1 = (self.width()-self.central_widget.width())/2
        y1 = (self.height()-self.central_widget.height())/2
        x2 = self.central_widget.width()+x1
        y2 = self.central_widget.height()+y1
        
        painter = QPainter(self)
        pen = QPen(QColor(35, 35, 35, 200))
        pen.setWidth(1)
        painter.setPen(pen)

        if not self.fullscreen:
            if self.opacity/self.max_opacity >= .5:
                # Header Border
                line = QLine(QPoint(x1, y1+self.logo_height+10), QPoint(x2, y1+self.logo_height+10))
                painter.drawLine(line)
                
                # Divider
                line = QLine(QPoint(x1+180, y1+self.logo_height+11), QPoint(x1+180, y2-self.footer_widget.height()-17)) # Column divider
                painter.drawLine(line)

        # Logo
        painter.setOpacity(self.opacity) 
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", self.logo_height/3))
        painter.drawText(QRect(x1+35, y1+35, x2-35, self.logo_height-35), Qt.AlignLeft, PROJECT)

    def new_cmd(self):
        self.post_open()
        command.new_scene(new_window=self.settings["new_window"])

    def open_cmd(self, filepath=""):
        self.post_open()
        command.open_file(filepath, new_window=self.settings["new_window"])

    def switch_to(self, target, sender):
        self.content_widget.setCurrentWidget(target)
        for button in [self.open_btn, self.recent_btn, self.setting_btn, self.about_btn]:
            button.boldToggle(False)
        if sender:
            sender.boldToggle(True)

    def post_open(self):
        if self.settings['close_on_open']:
            self.exit()
    
    def update_settings(self):
        self.settings['startup_show'] = self.settings_show_on_startup.isChecked()
        self.settings['full_screen'] = self.settings_fullscreen.isChecked()
        self.settings['close_on_open'] = self.settings_close_on_open.isChecked()
        self.settings['new_window'] = self.settings_open_new_window.isChecked()
        save_settings(self.settings)

    def update_recent_file_list(self):
        recent_files = get_recent()[PROJECT][APP]
        if self.recent_search.text():
            recent_files = [f for f in recent_files if self.recent_search.text().lower() in f['path'].lower()]
        self.recent_list.clear()
        self.recent_list.add_items(recent_files)
        self.update()

def start():
    ws = WelcomeScreen(parent=command.get_app_window())
    ws.start()