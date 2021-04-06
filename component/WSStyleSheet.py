WSStyleSheet = '''
QWidget {
	color: #ddd;
	background: transparent;
}

QWidget:disabled {
	color: #232323;
	background-color: transparent;
}

QLineEdit {
	border: 1px solid #232323;
	border-radius: 4px;
}

QToolTip {
	border: 1px solid #232323;
	background: #232323;
	color: #ddd;
}

QLineEdit:hover, QLineEdit:focus {
	border: 1px solid #FFC132;
    selection-color: #232323;
	selection-background-color: #FFC132;
}
QCheckBox::indicator {
	width : 12px;
	height : 12px;
	border-radius: 8px;
	border: 2px solid #232323;
}
QCheckBox::indicator:checked:hover, QCheckBox::indicator:unchecked:hover {
	border: 2px solid #FFC132;
}
QCheckBox::indicator:checked {
	background: #ddd;
}
QCheckBox::indicator:unchecked {
	background: #232323;
}

QAbstractItemView {
	border: 1px solid #232323;
    selection-color: #232323;
	selection-background-color: #FFC132;
}

QHeaderView::section {
	Background-color:#232323;
	padding:5px;
	border:0;
	font-weight: bold;
}

QScrollBar:vertical {
	background: transparent;
	width: 8px;
	border: 0;
}
QScrollBar::handle:vertical {
	background: #232323;
	min-height: 20px;
	border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
	background: #FFC132;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	border: none;
	background: none;
}
QScrollBar:horizontal {
	background: transparent;
	height: 8px;
	border: 1px solid #232323;
}
QScrollBar::handle:horizontal {
	background: #232323;
	min-width: 20px;
	border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
	background: #FFC132;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
	border: none;
	background: none;
}

QPushButton {
	background-color: #555;
	border: 2px solid #555;
	padding: 5px;
	border-radius: 4px;
	padding-left: 5px;
	padding-right: 5px;
}
QPushButton:hover{
	color: #FFC132;
	border-color: #FFC132;
}
QPushButton:pressed, QPushButton:checked {
	color: #232323;
	border-color: #FFC132;
	background-color: #FFC132;
}
QPushButton:checked{
	color: #FFC132;
	border-color: #FFC132;
	background-color: #232323;
	font-weight: bold;
}
'''