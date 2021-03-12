try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    
import os

from component import IconLabel, RecentLabel, FileBrowser
from config import APP, ICON_PATH, PROJECT, get_recent, save_recent, get_settings, save_settings

if APP == "NUKE":
    from ..app.nuke import command
    extfilter = ['*.nk']

    def get_window():
        for w in QApplication.topLevelWidgets():
            if w.metaObject().className() == 'Foundry::UI::DockMainWindow':
                return w

elif APP == "MAYA":
    from ..app.maya import command
    extfilter = ['*.ma', '*.mb']

    def get_window():
        for w in QApplication.topLevelWidgets():
            if w.objectName() == 'MayaWindow':
                return w


class WelcomeScreen(QDialog):
    def __init__(self, parent=get_window()):
        super(WelcomeScreen, self).__init__(parent)
        
        self.settings = get_settings()
        
        self.mainOpacity = 0.0
        self.max_opacity = 0.6
        self.opening_animation = self.fade_animation(0.0, self.max_opacity, 250, self.animated)
        self.closing_animation = self.fade_animation(self.max_opacity, 0.0, 250, self.animated)
        
        self.state = "Opening"
        self.setup_ui()

    def setup_ui(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

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
        self.right_layout = QVBoxLayout()

        self.setup_recent_widget()
        # self.setup_filebrowser_widget()
        self.setup_settings_widget()
        self.setup_about_widget()

        self.show_recent()

        
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
        
        self.master_widget = QWidget()
        self.master_layout = QVBoxLayout(self.master_widget)
        self.master_layout.addSpacing(170)
        self.master_layout.addLayout(self.main_layout)
        self.master_layout.addSpacing(15)
        self.master_layout.addLayout(self.footer_layout)
        
        window_layout = QVBoxLayout(self)
        horizontal_layout = QHBoxLayout()
        window_layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(self.master_widget)

        # Signal
        self.connect(self.new_btn, SIGNAL('clicked()'), self.new_cmd)
        self.connect(self.open_btn, SIGNAL('clicked()'), self.show_browser)
        self.connect(self.recent_btn, SIGNAL('clicked()'), self.show_recent)
        self.connect(self.setting_btn, SIGNAL('clicked()'), self.show_setting)
        self.connect(self.about_btn, SIGNAL('clicked()'), self.show_about)

        self.show_on_startup.clicked.connect(self.update_startup_settings)
        self.close_btn.clicked.connect(self.close)
        self.change_widget_size()

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

        self.recent_page_prev = IconLabel(icon="previous", iconsize=20)
        self.recent_page_next = IconLabel(icon="next", iconsize=20)
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
        
        self.right_layout.addWidget(self.recent_widget)
        
    def setup_filebrowser_widget(self):
        self.filebrowser_widget = FileBrowser(filterExtension=extfilter)
        # self.filebrowser_widget.executed.connect(self.open_cmd)
        recent_files = get_recent()[PROJECT][APP]
        recent = [file for file in sorted(recent_files, key=lambda k : k['access_date'], reverse=True )]
        if recent:
            self.filebrowser_widget.set_root(os.path.dirname(recent[0]['path']))

        self.right_layout.addWidget(self.filebrowser_widget)

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

        self.right_layout.addWidget(self.settings_widget)

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

        self.right_layout.addWidget(self.about_widget)
        
    def init_settings(self):
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
        
        self.fullscreen = self.settings['full_screen']
        
    def setOpacity(self,value): self.mainOpacity = value
    def getOpacity(self): return self.mainOpacity
    opacity = Property(float, getOpacity, setOpacity)
    
    def animated(self, value):
        if value == QAbstractAnimation.State.Stopped:
            if self.state == "Opening":
                self.master_widget.show()
            elif self.state == "Closing":
                super(WelcomeScreen, self).close()
            elif self.state == "Resizing":
                self.state = "Resized"
                self.fullscreen = self.settings['full_screen']
                self.change_widget_size()
                self.opening_animation.start()
            elif self.state == "Resized":
                self.master_widget.show()
                
    def fade_animation(self, start_opacity, end_opacity, duration, finished_callback):
        ani = QPropertyAnimation(self,"opacity")
        ani.setStartValue(start_opacity)
        ani.setEndValue(end_opacity)
        ani.setDuration(duration)
        ani.valueChanged.connect(self.update)
        ani.stateChanged.connect(finished_callback)
        return ani
        
    def show(self):
        self.state = "Opening"
        super(WelcomeScreen, self).show()
        self.master_widget.hide()
        self.init_settings()
        self.opening_animation.start()
        
    def close(self):
        self.state = "Closing"
        self.master_widget.hide()
        self.closing_animation.start()
    
    def change_widget_size(self):
        frame = ( self.parent().frameGeometry().width()-self.parent().width() )/2
        appWindowPos = self.parent().pos()+QPoint( frame, self.parent().frameGeometry().height()-self.parent().height()-frame )
        if self.settings['full_screen']:
            self.shadow = min(self.parent().width(), self.parent().height())/3 if self.parent().width() > 800 and self.parent().height() > 600 else 0
            self.setFixedSize(
                self.parent().width(), 
                self.parent().height(), 
            )
            self.move(appWindowPos)
            
            size = (min(self.width(), self.height())-self.shadow/2)
            self.master_widget.setFixedSize(
                max(size, 800), 
                max((size/8*6), 600)
            )
        else:
            self.shadow = 20 if self.parent().width() > 800 and self.parent().height() > 600 else 0
            self.setFixedSize(
                min(self.parent().width(), 800 + self.shadow), 
                min(self.parent().height(), 600 + self.shadow) 
            )
            
            self.move(appWindowPos + QPoint(
                    (self.parent().frameGeometry().width()/2) - (self.width() / 2), 
                    (self.parent().frameGeometry().height()/2) - (self.height() / 2)
                )
            )
        
            self.master_widget.setFixedSize(
                max(self.width()-self.shadow, 800), 
                max(self.height()-self.shadow, 600)
            )
    
    def change_resolution(self):
        self.state = "Resizing"
        self.master_widget.hide()
        self.fullscreen = not self.settings['full_screen']
        self.closing_animation.start()

    def paintEvent(self, QPaintEvent):
        super(WelcomeScreen, self).paintEvent(QPaintEvent)
        
        # Coordinate
        x1 = (self.width()-self.master_widget.width())/2
        y1 = (self.height()-self.master_widget.height())/2
        x2 = self.master_widget.width()+x1
        y2 = self.master_widget.height()+y1
        
        # Drop Shadow
        painter = QPainter(self)
        brush = QBrush(QColor(0, 0, 0))
        painter.setBrush(brush)
        painter.setPen(QPen(Qt.transparent))
        if self.fullscreen:
            painter.setOpacity(self.opacity) 
            rect = QRect(0, 0, self.width(), self.height())   
            painter.drawRect(rect)
        else:
            for i in range(self.shadow):
                painter.setOpacity((self.opacity-(self.shadow-i)/float(self.shadow)*self.opacity)/2)
                rect = QRect(i, i, self.width()-(i*2), self.height()-(i*2))
                painter.drawRoundedRect(rect, self.shadow/3, self.shadow/3)
            
            # painter.setOpacity(self.opacity) 
            # rect = QRect(x1, y1, x2-x1, y2-y1)
            # painter.drawRect(rect)
        
        # Fill Window
        if not self.fullscreen:
            if self.opacity/self.max_opacity >= .5:
                brush = QBrush(QColor(50, 50, 50))
                painter.setBrush(brush)
                painter.setOpacity(self.opacity/self.max_opacity)
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
                line = QLine(QPoint(x1+180, y1+151), QPoint(x1+180, y2-51)) # Column divider
                painter.drawLine(line)

        # Logo
        painter.setOpacity(self.opacity) 
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 40))
        painter.drawText(QRect(x1+30, y1+35, x2-60, 105), Qt.AlignLeft, PROJECT)

    def new_cmd(self):
        self.post_open()
        command.new_scene(new_window=self.settings["new_window"])

    def open_cmd(self, filepath=""):
        self.post_open()
        command.open_file(filepath, new_window=self.settings["new_window"])

    def hide_widgets(self):
        if hasattr(self, 'recent_widget'):
            self.recent_widget.hide()
        if hasattr(self, 'filebrowser_widget'):
            self.filebrowser_widget.hide()
        if hasattr(self, 'settings_widget'):
            self.settings_widget.hide()
        if hasattr(self, 'about_widget'):
            self.about_widget.hide()

    def show_browser(self):
        self.hide_widgets()
        #self.filebrowser_widget.show()
        self.open_cmd()

    def show_recent(self):
        self.hide_widgets()
        self.recent_widget.show()

    def show_setting(self):
        self.hide_widgets()
        self.settings_widget.show()

    def show_about(self):
        self.hide_widgets()
        self.about_widget.show()

    def post_open(self):
        if self.settings['close_on_open']:
            self.close()
    
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
        self.recent_list = [RecentLabel() for i in range(self.max_list)]
        for i, w in enumerate(self.recent_list):
            w.update_file({"path":""})
            self.connect(w, SIGNAL('openScript()'), self.clicked)
            self.master_layout.addWidget(w)
            self.master_layout.addSpacing(15)
        self.master_layout.addStretch()
        self.initialized = True

    def update_list(self, searchStr, currentPage):
        self.recent = get_recent()
        recent_files = self.recent[PROJECT][APP]
        fileList = [file for file in sorted(recent_files, key=lambda k : k['access_date'], reverse=True )]
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