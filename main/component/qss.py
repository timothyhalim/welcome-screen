styleSheet = """
#Ready {
	background-color: #008C00;
	color: white;
}
#NotReady {
	background-color: #FF8C00;
	color: white;
}
#Error {
	background-color: #8B0000;
	color: white;
}

#Container {
	border-radius: 4;
	border: 1px solid #555;
}

QWidget {
	color: #ddd;
	background: #333;
}

QWidget:disabled {
	color: #555;
	background-color: #333;
}

QDialog {
	background-color: #333;
}

QLabel{
	background: transparent;
}

QGroupBox::title {
	subcontrol-origin: margin;
	left: 7px;
	padding: 0px 5px 0px 5px;
}

QGroupBox {
	background-color: transparent;
	border: 1px solid #555;
	border-radius: 4;
	padding-top: 0;
	margin-top: 2.5ex;
}

QComboBox {
	border: 1px solid #555;
	border-radius: 4;
	padding: 3px;
	min-width: 6em;
	selection-background-color: #f7931e;
}


QAbstractItemView {
	border: none;
	selection-background-color: #f7931e;
}

QListWidget {
	border: 1px solid #555;
	border-radius: 4;
}

QPlainTextEdit, QLineEdit, QLineEdit {
	border-style: solid;
	border: 1px solid #555;
	border-radius: 4;
}

QPlainTextEdit, QLineEdit:hover, QLineEdit:focus {
	border-style: solid;
	border: 1px solid #f7931e;
	border-radius: 4;
	selection-background-color: #f7931e;
}

QCheckBox::indicator:checked:hover, QCheckBox::indicator:unchecked:hover {
	border: 2px solid #f7931e;
}
QCheckBox::indicator:checked {
	background: #ddd;
	border: 2px solid #333;
	border-radius: 6px;
}
QCheckBox::indicator:unchecked {
	background: #333;
	border: 2px solid #333;
	border-radius: 6px;
}

QAbstractScrollArea #scrollAreaWidgetContents {
	background-color: black;
}

QScrollBar:vertical {
	background: transparent;
	width: 8px;
	border: 1px solid #333;
}
QScrollBar::handle:vertical {
	background: #555;
	min-height: 20px;
	border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
	background: #f7931e;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	border: none;
	background: none;
}
QScrollBar:horizontal {
	background: transparent;
	height: 8px;
	border: 1px solid #333;
}
QScrollBar::handle:horizontal {
	background: #555;
	min-width: 20px;
	border-radius: 3px;
}
QScrollBar::handle:horizontal:hover {
	background: #f7931e;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
	border: none;
	background: none;
}
QSlider {
	min-height: 20px;
}
QSlider::groove:horizontal {
	border: None;
	height: 5px; 
	background: #333;
	border-radius: 2px;
}
QSlider::handle:horizontal {
	background: #555;
	width: 16px;
	padding: -2px;
	margin: -6px 0;
	border: 2px solid #333;
	border-radius: 8px;
}
QSlider::handle:horizontal:hover {
	border: 2px solid #f7931e;
}
QSlider::add-page:qlineargradient {
	background: 333;
}
QSlider::sub-page:qlineargradient {
	background: #f7931e;
	border: 2px solid #333;
	border-radius: 2px;
}
QPushButton {
	background-color: #555;
	border-width: 2;
	border-color: #555;
	border-style: solid;
	border-radius: 6;
	padding: 3px;
	padding-left: 5px;
	padding-right: 5px;
}
QPushButton:hover{
	color: #333;
	border-color: #f7931e;
	background-color: #f7931e;
}
QPushButton:pressed {
	color: #f7931e;
	border-color: #f7931e;
	background-color: #555;
}

QProgressBar{text-align: center; background-color: transparent}
QProgressBar::chunk{background-color: #555;border:None;}

QTabWidget::pane {border-top: 1px solid #333; bottom:2px;}
QTabWidget::tab-bar {left: 0px;}
QTabWidget::tab-bar:top {top: 1px;}
QTabWidget::tab-bar:bottom {bottom: 1px;}
QTabWidget::tab-bar:left {right: 1px;}
QTabWidget::tab-bar:right {left: 1px;}
QTabBar{background:transparent;}
QTabBar::tab {background:transparent; font-weight: bold; width:55px}
QTabBar::tab:!selected {background: #282828; color: #999}
QTabBar::tab:!selected:hover {color: #BBB; border-top: 2px solid #f7931e}
QTabBar::tab:top:!selected {margin-top: 3px;}
QTabBar::tab:bottom:!selected {margin-bottom: 3px;}
QTabBar::tab:left:!selected {margin-right: 3px;}
QTabBar::tab:right:!selected {margin-left: 3px;}
QTabBar::tab:top:selected {border-bottom-color: none;}
QTabBar::tab:bottom:selected {border-top-color: none;}
QTabBar::tab:left:selected {border-left-color: none;}
QTabBar::tab:right:selected {border-right-color: none;}
QTabBar::tab:top, QTabBar::tab:bottom {min-width: 8ex;margin-right: -1px;padding: 5px 10px 5px 10px;}
QTabBar::tab:top:last, QTabBar::tab:bottom:last,QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {margin-right: 0;}
QTabBar::tab:left:last, QTabBar::tab:right:last,QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {margin-bottom: 0;}
QTabBar::tab:left, QTabBar::tab:right {min-height: 8ex;margin-bottom: -1px;padding: 10px 5px 10px 5px;}

QTableWidget {
	border: 1px solid #282828;
	selection-background-color: #f7931e; 
	selection-color: #BBB; 
	background-color:#333333; 
	alternate-background-color: #292929;
}
QTableWidget::item { 
	margin: 0 5px 0 5px 
}

QHeaderView::section {
	Background-color:#282828;
	padding:5px;
	border:1px solid #333;
	font-weight: bold;
}

QListView {
	show-decoration-selected: 1; /* make the selection span the entire width of the view */
}

QListView::item:alternate {
	background: #EEEEEE;
}

QListView::item:selected {
	color: #f7931e;
	border-color: #f7931e;
	background-color: #555;
}

QListView::item:selected:!active {
	color: #f7931e;
	border-color: #f7931e;
	background-color: #555;
}

QListView::item:selected:active {
	color: #f7931e;
	border-color: #f7931e;
	background-color: #555;
}

QListView::item:hover {
	color: #333;
	border-color: #f7931e;
	background-color: #f7931e;
}
"""