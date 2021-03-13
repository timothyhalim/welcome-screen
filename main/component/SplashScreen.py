try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui     import *
    from PySide2.QtCore    import *
    qttype = "PySide2"
except:
    from PySide.QtGui  import *
    from PySide.QtCore import *
    qttype = "PySide"

class SplashScreen(QDialog):
    def __init__(self, parent=None, fullscreen=False, minwidth=800, minheight=600):
        super(SplashScreen, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.fullscreen = fullscreen
        self.minWidth = minwidth
        self.minHeight = minheight
        self.state = "Opening"
        self.mainOpacity = 0.0
        self.max_opacity = 0.6
        self.opening_animation = self.fade_animation(0.0, self.max_opacity, 250, self.animated)
        self.closing_animation = self.fade_animation(self.max_opacity, 0.0, 250, self.animated)
        
        # Content Widget
        self.master_widget = QWidget()

        # Footer
        self.footer_widget = QWidget()
        self.footer_widget.setMaximumHeight(30)
        self.footer_layout = QHBoxLayout(self.footer_widget)
        self.footer_layout.setContentsMargins(0,0,0,0)
        self.close_btn = QPushButton("Close")
        # self.close_btn.setStyleSheet("color:rgb(50, 50, 50); background-color:rgb(135, 195, 240); font-family:Arial")

        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.close_btn)

        # Central Widget
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.master_widget)
        self.central_layout.addWidget(self.footer_widget)

        window_layout = QVBoxLayout(self)
        horizontal_layout = QHBoxLayout()
        window_layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(self.central_widget)

        # Signal
        self.close_btn.clicked.connect(self.exit)
        
        self.change_widget_size(self.fullscreen)

    def setOpacity(self,value): self.mainOpacity = value
    def getOpacity(self): return self.mainOpacity
    opacity = Property(float, getOpacity, setOpacity)

    def animated(self, value):
        if value == QAbstractAnimation.State.Stopped:
            if self.state == "Opening":
                self.central_widget.show()
            elif self.state == "Closing":
                self.close()
            elif self.state == "Resizing":
                self.state = "Resized"
                self.change_widget_size(not self.fullscreen)
                self.opening_animation.start()
            elif self.state == "Resized":
                self.central_widget.show()

    def fade_animation(self, start_opacity, end_opacity, duration, finished_callback):
        ani = QPropertyAnimation(self,"opacity")
        ani.setStartValue(start_opacity)
        ani.setEndValue(end_opacity)
        ani.setDuration(duration)
        ani.setEasingCurve(QEasingCurve.InOutCirc)
        ani.valueChanged.connect(self.update)
        ani.stateChanged.connect(finished_callback)
        return ani
        
    def start(self):
        self.state = "Opening"
        self.show()
        self.central_widget.hide()
        self.opening_animation.start()
        
    def exit(self):
        self.state = "Closing"
        self.central_widget.hide()
        self.closing_animation.start()
    
    def center_widget(self):
        if self.parent():
            windowframe = ( self.parent().frameGeometry().width()-self.parent().width() )/2
            topFrame = self.parent().frameGeometry().height()-self.parent().height()-windowframe
            appWindowPos = self.parent().pos() + QPoint(windowframe, topFrame)
                
            self.move(appWindowPos + QPoint(
                    (self.parent().frameGeometry().width()/2) - (self.width() / 2), 
                    (self.parent().frameGeometry().height()/2) - (self.height() / 2)
                )
            )
        else:
            self.screenresolution = QDesktopWidget().screenGeometry()
            self.move( 
                QPoint(self.screenresolution.width() / 2, self.screenresolution.height() / 2) - 
                QPoint((self.width() / 2), (self.height() / 2))
            )
        

    def change_widget_size(self, fullscreen=False):
        if fullscreen:
            if self.parent():
                self.shadow = min(self.parent().width(), self.parent().height())/3 if self.parent().width() > self.minWidth and self.parent().height() > self.minHeight else 0
                self.setFixedSize(
                    self.parent().width(), 
                    self.parent().height(), 
                )
                
                size = (min(self.width(), self.height())-self.shadow/2)
                self.central_widget.setFixedSize(
                    max(size, self.minWidth), 
                    max((size/8*6), self.minHeight)
                )
            else:
                self.screenresolution = QDesktopWidget().screenGeometry()
                self.shadow = min(self.screenresolution.width(), self.screenresolution.height())/3 if self.screenresolution.width() > self.minWidth and self.screenresolution.height() > self.minHeight else 0

                self.setFixedSize(
                    self.screenresolution.width(), 
                    self.screenresolution.height()
                )

                size = (min(self.width(), self.height())-self.shadow/2)
                self.central_widget.setFixedSize(
                    max(size, self.minWidth), 
                    max((size/8*6), self.minHeight)
                )
        else:
            self.shadow = 20 
            self.setFixedSize(
                self.minWidth + self.shadow, 
                self.minHeight + self.shadow
            )
            self.central_widget.setFixedSize(
                max(self.width()-self.shadow, self.minWidth), 
                max(self.height()-self.shadow, self.minHeight)
            )
        self.fullscreen = fullscreen
        self.center_widget()
    
    def change_resolution(self):
        self.state = "Resizing"
        self.central_widget.hide()
        self.closing_animation.start()

    def paintEvent(self, QPaintEvent):
        super(SplashScreen, self).paintEvent(QPaintEvent)

        # Coordinate
        x1 = (self.width()-self.central_widget.width())/2
        y1 = (self.height()-self.central_widget.height())/2
        x2 = self.central_widget.width()+x1
        y2 = self.central_widget.height()+y1
        
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
        
        self.setWindowOpacity(self.opacity/self.max_opacity)
        
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
                
                # Footer
                line = QLine(QPoint(x1, y2-self.footer_widget.height()-17), QPoint(x2, y2-self.footer_widget.height()-17))
                painter.drawLine(line)