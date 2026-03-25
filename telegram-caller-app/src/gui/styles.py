# -*- coding: utf-8 -*-
"""
Стили для тёмной темы приложения (синий/фиолетовый Modern UI)
"""

DARK_STYLE = """
QWidget {
    background-color: #1a1a2e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: #16213e;
}

QPushButton {
    background-color: #0f3460;
    color: #ffffff;
    border: 1px solid #533483;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #1a4870;
    border: 1px solid #7b2cbf;
}

QPushButton:pressed {
    background-color: #0a2647;
}

QPushButton:disabled {
    background-color: #2d2d44;
    color: #6b6b6b;
    border: 1px solid #3d3d5c;
}

QPushButton#CallButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #7b2cbf, stop:1 #533483);
    font-size: 16px;
    font-weight: bold;
}

QPushButton#CallButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #9d4edd, stop:1 #7b2cbf);
}

QPushButton#EndCallButton {
    background-color: #c0392b;
    color: white;
}

QPushButton#EndCallButton:hover {
    background-color: #e74c3c;
}

QLineEdit {
    background-color: #0f0f23;
    color: #e0e0e0;
    border: 1px solid #533483;
    border-radius: 6px;
    padding: 8px 12px;
    selection-background-color: #7b2cbf;
}

QLineEdit:focus {
    border: 2px solid #7b2cbf;
}

QListWidget {
    background-color: #0f0f23;
    border: 1px solid #533483;
    border-radius: 6px;
    outline: none;
}

QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #2d2d44;
}

QListWidget::item:selected {
    background-color: #7b2cbf;
    color: white;
}

QListWidget::item:hover {
    background-color: #1a1a3e;
}

QTabWidget::pane {
    border: 1px solid #533483;
    border-radius: 6px;
    background-color: #0f0f23;
}

QTabBar::tab {
    background-color: #1a1a2e;
    color: #a0a0a0;
    padding: 10px 20px;
    border: 1px solid #533483;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background-color: #7b2cbf;
    color: white;
}

QTabBar::tab:hover:!selected {
    background-color: #2d2d44;
}

QStatusBar {
    background-color: #0f0f23;
    color: #a0a0a0;
    border-top: 1px solid #533483;
}

QLabel {
    color: #e0e0e0;
}

QLabel#TitleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #7b2cbf;
}

QLabel#StatusLabel {
    color: #a0a0a0;
    font-size: 12px;
}

QComboBox {
    background-color: #0f0f23;
    color: #e0e0e0;
    border: 1px solid #533483;
    border-radius: 6px;
    padding: 8px 12px;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #7b2cbf;
    margin-right: 8px;
}

QComboBox:hover {
    border: 2px solid #7b2cbf;
}

QProgressBar {
    background-color: #0f0f23;
    border: 1px solid #533483;
    border-radius: 4px;
    text-align: center;
    color: #e0e0e0;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7b2cbf, stop:1 #533483);
}

QScrollBar:vertical {
    background-color: #1a1a2e;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #533483;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #7b2cbf;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QCheckBox {
    color: #e0e0e0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #533483;
    border-radius: 4px;
    background-color: #0f0f23;
}

QCheckBox::indicator:checked {
    background-color: #7b2cbf;
    border-color: #7b2cbf;
}

QGroupBox {
    border: 1px solid #533483;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #7b2cbf;
}
"""

CALL_UI_STYLE = """
QWidget#CallWidget {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a1a2e, stop:1 #16213e);
    border-radius: 12px;
}

QLabel#CallerNameLabel {
    font-size: 24px;
    font-weight: bold;
    color: #ffffff;
}

QLabel#CallStatusLabel {
    font-size: 16px;
    color: #7b2cbf;
}

QPushButton#MuteButton {
    background-color: #2d2d44;
    border: 2px solid #533483;
}

QPushButton#MuteButton:checked {
    background-color: #c0392b;
    border: 2px solid #e74c3c;
}

QPushButton#VideoButton {
    background-color: #2d2d44;
    border: 2px solid #533483;
}

QPushButton#VideoButton:checked {
    background-color: #27ae60;
    border: 2px solid #2ecc71;
}
"""