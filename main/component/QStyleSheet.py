styleSheet = '''
QWidget {
	color: #ddd;
	background: transparent;
}

QWidget:disabled {
	color: #232323;
	background-color: transparent;
}

QLineEdit {
	border-style: solid;
	border: 1px solid #232323;
	border-radius:4px;
}

QLineEdit:hover, QLineEdit:focus {
	border-style: solid;
	border: 1px solid #FFC132;
    selection-color: #232323;
	selection-background-color: #FFC132;
}

QCheckBox::indicator:checked:hover, QCheckBox::indicator:unchecked:hover {
	border: 2px solid #FFC132;
	border-radius: 8;
}
QCheckBox::indicator:checked {
	background: #ddd;
	border: 2px solid #232323;
	border-radius: 8;
}
QCheckBox::indicator:unchecked {
	background: #232323;
	border: 2px solid #232323;
	border-radius: 8;
}

QAbstractItemView {
	border: 1px solid #232323;
    selection-color: #232323;
	selection-background-color: #FFC132;
}

QHeaderView::section {
	Background-color:#282828;
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
	border-radius:4px;
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
	border-radius:4px;
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
	border-radius:4px;
	padding: 5px;
	padding-left: 5px;
	padding-right: 5px;
}
QPushButton:hover{
	color: #FFC132;
	border-color: #FFC132;
	background-color: #232323;
}
QPushButton:pressed {
	color: #232323;
	border-color: #FFC132;
	background-color: #FFC132;
}
'''