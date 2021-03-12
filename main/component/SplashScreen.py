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
    def __init__(self, parent=None, fullscreen=False):
        super(SplashScreen, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.fullscreen = fullscreen
        self.state = "Opening"
        self.mainOpacity = 0.0
        self.max_opacity = 0.6
        self.opening_animation = self.fade_animation(0.0, self.max_opacity, 250, self.animated)
        self.closing_animation = self.fade_animation(self.max_opacity, 0.0, 250, self.animated)
        
        self.layout = QHBoxLayout()

        # Footer
        self.close_btn = QPushButton("Close")
        self.close_btn.setStyleSheet("color:rgb(50, 50, 50); background-color:rgb(135, 195, 240); font-family:Arial")

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(0,0,0,0)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.close_btn)

        # Master Widget
        self.master_widget = QWidget()
        self.master_layout = QVBoxLayout(self.master_widget)
        self.master_layout.addSpacing(170)
        self.master_layout.addLayout(self.layout)
        self.master_layout.addSpacing(15)
        self.master_layout.addLayout(self.footer_layout)

        window_layout = QVBoxLayout(self)
        horizontal_layout = QHBoxLayout()
        window_layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(self.master_widget)

        # Signal
        self.close_btn.clicked.connect(self.exit)
        
        self.change_widget_size()

    def setOpacity(self,value): self.mainOpacity = value
    def getOpacity(self): return self.mainOpacity
    opacity = Property(float, getOpacity, setOpacity)

    def animated(self, value):
        if value == QAbstractAnimation.State.Stopped:
            if self.state == "Opening":
                self.master_widget.show()
            elif self.state == "Closing":
                self.close()
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
        
    def start(self):
        self.state = "Opening"
        self.show()
        self.master_widget.hide()
        self.opening_animation.start()
        
    def exit(self):
        self.state = "Closing"
        self.master_widget.hide()
        self.closing_animation.start()
    
    def center_to_parent(self):
        if self.parent():
            frame = ( self.parent().frameGeometry().width()-self.parent().width() )/2
            appWindowPos = self.parent().pos()+QPoint( frame, self.parent().frameGeometry().height()-self.parent().height()-frame )
                
            self.move(appWindowPos + QPoint(
                    (self.parent().frameGeometry().width()/2) - (self.width() / 2), 
                    (self.parent().frameGeometry().height()/2) - (self.height() / 2)
                )
            )

    def change_widget_size(self):
        self.shadow = 20 
        self.setFixedSize(
            800 + self.shadow, 
            600 + self.shadow
        )
        self.master_widget.setFixedSize(
            max(self.width()-self.shadow, 800), 
            max(self.height()-self.shadow, 600)
        )
    
    def change_resolution(self):
        self.state = "Resizing"
        self.master_widget.hide()
        self.fullscreen = not self.fullscreen
        self.closing_animation.start()

    def paintEvent(self, QPaintEvent):
        super(SplashScreen, self).paintEvent(QPaintEvent)

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
        # painter.setOpacity(self.opacity) 
        # painter.setPen(QPen(QColor(255, 255, 255)))
        # painter.setFont(QFont("Arial", 40))
        # painter.drawText(QRect(x1+30, y1+35, x2-60, 105), Qt.AlignLeft, PROJECT)