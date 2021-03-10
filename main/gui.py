try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *

from component import QCustomLabel, QRecentLabel
from config import APP, ICON_PATH, PROJECT, get_recent, save_recent, get_settings, save_settings

if APP == "NUKE":
    from ..app.nuke import command

    def get_window():
        for w in QApplication.topLevelWidgets():
            if w.metaObject().className() == 'Foundry::UI::DockMainWindow':
                return w

elif APP == "MAYA":
    from ..app.maya import command

    def get_window():
        for w in QApplication.topLevelWidgets():
            if w.objectName() == 'MayaWindow':
                return w


class WelcomeScreen(QDialog):
    def __init__(self, parent=get_window()):
        super(WelcomeScreen, self).__init__(parent)

        self.settings = get_settings()
        self.setup_ui()

    def show(self):
        super(WelcomeScreen, self).show()
        self.allPages = 1
        self.curentPage = 1
        
        if not self.recent_list.initialized:
            self.recent_list.initialize()
        self.update_recent_file_list()

        self.show_on_startup.setChecked(self.settings['startup_show'])
        self.settings_show_on_startup.setChecked(self.settings['startup_show'])
        self.settings_fullscreen.setChecked(self.settings['full_screen'])
        self.settings_close_on_open.setChecked(self.settings['close_on_open'])
        self.settings_open_new_window.setChecked(self.settings['new_window'])

    def setup_ui(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        # Left Side
        self.new_btn = QCustomLabel(name="New", icon="new")
        self.open_btn = QCustomLabel(name="Open", icon="open")
        self.recent_btn = QCustomLabel(name="Recent", icon="history")
        self.setting_btn = QCustomLabel(name="Setting", icon="setting")
        self.about_btn = QCustomLabel(name="About...", icon="about")

        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0,0,0,0)
        for w in (self.new_btn, self.open_btn, self.recent_btn, self.setting_btn, self.about_btn):
            self.left_layout.addWidget(w)
        self.left_layout.addStretch()

        # Right Side
        self.setup_recent_widget()
        self.setup_settings_widget()
        self.setup_about_widget()

        self.settings_widget.hide()
        self.about_widget.hide()

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.recent_widget)
        self.right_layout.addWidget(self.settings_widget)
        self.right_layout.addWidget(self.about_widget)
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.right_layout)

        # Footer
        self.show_on_startup = QCheckBox("Show Welcome Screen at Startup")
        self.show_on_startup.setStyleSheet("color:rgb(180, 180, 180); font-family:Arial")
        self.close_btn = QPushButton("Close")
        self.close_btn.setStyleSheet("color:rgb(50, 50, 50); background-color:rgb(135, 195, 240); font-family:Arial")

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0,0,0,0)
        self.footer_layout.addWidget(self.show_on_startup)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.close_btn)
        
        self.main_widget = QWidget()
        self.master_layout = QVBoxLayout(self.main_widget)
        self.master_layout.addSpacing(170)
        self.master_layout.addLayout(self.main_layout)
        self.master_layout.addSpacing(15)
        self.master_layout.addLayout(self.footer_layout)
        
        window_layout = QVBoxLayout(self)
        horizontal_layout = QHBoxLayout()
        window_layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(self.main_widget)

        # Signal
        self.connect(self.new_btn, SIGNAL('clicked()'), self.new_cmd)
        self.connect(self.open_btn, SIGNAL('clicked()'), self.open_cmd)
        self.connect(self.recent_btn, SIGNAL('clicked()'), self.show_recent)
        self.connect(self.setting_btn, SIGNAL('clicked()'), self.show_setting)
        self.connect(self.about_btn, SIGNAL('clicked()'), self.show_about)

        self.show_on_startup.clicked.connect(self.update_startup_settings)
        self.close_btn.clicked.connect(self.close)
        self.change_resolution()

    def setup_recent_widget(self):
        self.recent_widget = QWidget()
        self.recent_label = QLabel("Recent Files:")
        self.recent_label.setFont(QFont("Arial", 11))
        self.recent_label.setStyleSheet("color:rgb(180, 180, 180)")
        self.recent_search = QLineEdit()
        self.recent_search.setStyleSheet("""color:rgb(180, 180, 180); padding:4px 4px 4px 20px; 
                                            background-image:url(%s/search.png); 
                                            background-color:rgb(50, 50, 50); 
                                            background-position: left; 
                                            background-repeat:no-repeat""" % ICON_PATH)
        self.recent_search.setPlaceholderText("Search")
        self.recent_layout = QHBoxLayout()
        self.recent_layout.addWidget(self.recent_label)
        self.recent_layout.addSpacing(30)
        self.recent_layout.addWidget(self.recent_search)

        self.recent_list = QRecentWidget()

        self.recent_page_prev = QCustomLabel(icon="previous", iconsize=20)
        self.recent_page_next = QCustomLabel(icon="next", iconsize=20)
        self.recent_page_info = QLabel()
        self.recent_page_info.setText("0/0")
        self.recent_page_info.setFont(QFont("Arial", 10))
        self.recent_page_info.setAlignment(Qt.AlignCenter)
        self.recent_page_info.setStyleSheet("color:rgb(180, 180, 180)")

        self.recent_page_layout = QHBoxLayout()
        self.recent_page_layout.addWidget(self.recent_page_prev)
        self.recent_page_layout.addSpacing(10)
        self.recent_page_layout.addWidget(self.recent_page_info)
        self.recent_page_layout.addSpacing(10)
        self.recent_page_layout.addWidget(self.recent_page_next)
        
        self.recent_widget_layout = QVBoxLayout(self.recent_widget)
        self.recent_widget_layout.setSpacing(0)
        self.recent_widget_layout.addLayout(self.recent_layout)
        self.recent_widget_layout.addSpacing(7)
        self.recent_widget_layout.addWidget(self.recent_list)
        self.recent_widget_layout.addLayout(self.recent_page_layout)
        
        # Signal
        self.recent_search.textChanged.connect(self.search_recent)
        self.recent_list.file.connect(self.open_cmd)
        self.connect(self.recent_page_prev, SIGNAL('clicked()'), self.prev_page)
        self.connect(self.recent_page_next, SIGNAL('clicked()'), self.next_page)

        
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
        self.settings_layout.setSpacing(10)
        self.settings_layout.addLayout(self.settings_label_layout)
        self.settings_layout.addSpacing(7)
        for w in (self.settings_show_on_startup, self.settings_fullscreen, self.settings_open_new_window, self.settings_close_on_open):
            w.setFont(QFont("Arial", 10))
            self.settings_layout.addWidget(w)
            w.clicked.connect(self.update_settings)
        self.settings_fullscreen.clicked.connect(self.change_resolution)
        self.settings_layout.addStretch()
            

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
        

    def paintEvent(self, QPaintEvent):
        super(WelcomeScreen, self).paintEvent(QPaintEvent)

        painter = QPainter(self)

        # Drop Shadow
        brush = QBrush(QColor(0, 0, 0))
        painter.setBrush(brush)
        painter.setPen(QPen(Qt.transparent))
        if self.settings['full_screen']:
            max_opacity = .6
            painter.setOpacity(max_opacity)
            rect = QRect(0, 0, self.width(), self.height())   
            painter.drawRect(rect)
        else:
            max_opacity = .2
            painter.setOpacity(max_opacity)
            for i in range(self.shadow):
                painter.setOpacity(max_opacity-(self.shadow-i)/float(self.shadow)*max_opacity)
                rect = QRect(i, i, self.width()-(i*2), self.height()-(i*2))
                painter.drawRoundedRect(rect, max(self.shadow/3,10), min(self.shadow/3,10))
    
        # Fill Window
        x1 = (self.width()-self.main_widget.width())/2
        y1 = (self.height()-self.main_widget.height())/2
        x2 = self.main_widget.width()+x1
        y2 = self.main_widget.height()+y1
        
        brush = QBrush(QColor(50, 50, 50))
        painter.setBrush(brush)
        painter.setOpacity(1)
        rect = QRect(x1, y1, x2-x1, y2-y1)
        painter.drawRect(rect)
    
    
        # Border
        pen = QPen(QColor(35, 35, 35, 200))
        pen.setWidth(1)
        painter.setPen(pen)
        
        # Top Border
        line = QLine(QPoint(x1, y1), QPoint(x2, y1))
        painter.drawLine(line)
        
        # Left Border
        line = QLine(QPoint(x1, y1), QPoint(x1, y2))
        painter.drawLine(line)

        # Right Border
        line = QLine(QPoint(x2, y1), QPoint(x2, y2))
        painter.drawLine(line)

        # Bottom Border
        line = QLine(QPoint(x1, y2), QPoint(x2, y2))
        painter.drawLine(line)
        
        # Header Border
        line = QLine(QPoint(x1, y1+150), QPoint(x2, y1+150))
        painter.drawLine(line)
        
        # Footer
        line = QLine(QPoint(x1, y2-50), QPoint(x2, y2-50))
        painter.drawLine(line)
        
        # Divider
        line = QLine(QPoint(x1+180, y1+150), QPoint(x1+180, y2-50)) # Column divider
        painter.drawLine(line)

        # Logo
        brush = QBrush(QColor(151, 46, 60))
        pen = QPen(QColor(0, 0, 0, 0))
        painter.setPen(pen)
        painter.setBrush(brush)
        #self.rect = QRect(0, 0, self.customWidth, 150)
        #painter.drawRect(self.rect)

        # self.nukeIcon = QPixmap("%s/logo.png" % ICON_PATH).scaled(400, 200 , Qt.KeepAspectRatio)
        # painter.drawPixmap(QPoint(0, 0), self.nukeIcon)

        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 40))
        painter.drawText(QRect(x1+30, y1+35, x2-60, 105), Qt.AlignLeft, PROJECT)
        
    def on_top(self):
        self.raise_()

    def new_cmd(self):
        self.post_open()
        command.new_scene(new_window=self.settings["new_window"])

    def open_cmd(self, filepath=""):
        self.post_open()
        command.open_file(filepath, new_window=self.settings["new_window"])

    def show_recent(self):
        self.recent_widget.show()
        self.settings_widget.hide()
        self.about_widget.hide()

    def show_setting(self):
        self.recent_widget.hide()
        self.settings_widget.show()
        self.about_widget.hide()

    def show_about(self):
        self.recent_widget.hide()
        self.settings_widget.hide()
        self.about_widget.show()

    def post_open(self):
        if self.settings['close_on_open']:
            self.close()
    
    def change_resolution(self):
        frame = ( self.parent().frameGeometry().width()-self.parent().width() )/2
        appWindowPos = self.parent().pos()+QPoint( frame, self.parent().frameGeometry().height()-self.parent().height()-frame )
        if self.settings['full_screen']:
            self.shadow = max(self.parent().width(), self.parent().height())/3
            self.setFixedSize(
                max(self.parent().width(), 800+self.shadow), 
                max(self.parent().height(), 600+self.shadow), 
            )
            self.move(appWindowPos)
            
            self.main_widget.setFixedSize(
                max(min(self.width(), self.height())-self.shadow/2, 800), 
                max(min(self.width(), self.height())-self.shadow/2, 800)/8*6
            )
        else:
            self.shadow = 20
            self.setFixedSize(
                max(self.parent().width()/3, 800) + self.shadow, 
                max(self.parent().height()/3, 600) + self.shadow
            )
            
            self.move(appWindowPos + QPoint(
                    (self.parent().frameGeometry().width()/2) - (self.width() / 2), 
                    (self.parent().frameGeometry().height()/2) - (self.height() / 2)
                )
            )
        
            self.main_widget.setFixedSize(
                max(self.width()-self.shadow, 800), 
                max(self.height()-self.shadow, 600)
            )
            
    
    def update_settings(self):
        self.settings['startup_show'] = self.settings_show_on_startup.isChecked()
        self.settings['full_screen'] = self.settings_fullscreen.isChecked()
        self.settings['close_on_open'] = self.settings_close_on_open.isChecked()
        self.settings['new_window'] = self.settings_open_new_window.isChecked()
        self.show_on_startup.setChecked(self.settings['startup_show']) 
        save_settings(self.settings)


    def update_startup_settings(self):
        self.settings_show_on_startup.setChecked(self.show_on_startup.isChecked()) 
        self.update_settings()

    def search_recent(self):
        self.curentPage = 1
        self.update_recent_file_list()

    def update_recent_file_list(self):
        self.allPages = self.recent_list.update_list(self.recent_search.text(), self.curentPage)
        self.recent_page_info.setText("%s/%s" % (self.curentPage, self.allPages))
        self.update()

    def prev_page(self):
        if self.curentPage > 1:
            self.curentPage -=  1
        self.update_recent_file_list()

    def next_page(self):
        if self.curentPage < self.allPages:
            self.curentPage += 1
        self.update_recent_file_list()


class QRecentWidget(QWidget):
    file = Signal(object)

    def __init__(self):
        super(QRecentWidget, self).__init__()
        self.master_layout = QVBoxLayout(self)
        self.master_layout.setSpacing(0)
        self.initialized = False

    def initialize(self):
        self.max_list = int(self.height()/19)
        self.recent_list = [QRecentLabel() for i in range(self.max_list)]
        for i, w in enumerate(self.recent_list):
            w.update_file({"path":""})
            self.connect(w, SIGNAL('openScript()'), self.clicked)
            self.master_layout.addWidget(w)
            self.master_layout.addSpacing(15)
        self.master_layout.addStretch()
        self.initialized = True

    def update_list(self, searchStr, currentPage):
        self.recent = get_recent()
        nuke_recent = self.recent[PROJECT][APP]
        fileList = [file for file in sorted(nuke_recent, key=lambda k : k['access_date'], reverse=True )]
        if searchStr:
            fileList = [f for f in fileList if searchStr.lower() in f['path'].lower()]
        
        recent_file = fileList[self.max_list * (currentPage-1) : self.max_list * currentPage]
        for i, w in enumerate(self.recent_list):
            path = recent_file[i] if i < len(recent_file) else {"path":""}
            w.update_file(path)
            
        q, r = divmod(len(fileList)/float(self.max_list), 1)
        page_count = int(q) + bool(r)
        return max(page_count, 1)

    def clicked(self):
        self.file.emit(self.sender().filePath)

def show():
    ws = WelcomeScreen()
    ws.show()