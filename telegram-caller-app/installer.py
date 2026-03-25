# -*- coding: utf-8 -*-
"""
Telegram Caller - Установщик (Installer)
Создает выбор между веб-версией и десктоп приложением
"""

import sys
import os
import subprocess
import webbrowser
import threading

try:
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QFrame
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QFont
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False

APP_NAME = "Telegram Caller"
APP_VERSION = "1.0.0"
WEB_PORT = 3000

def get_web_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'web')

def get_desktop_exe_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'TelegramCaller.exe')

def start_simple_http_server(port, web_path):
    import http.server
    import socketserver
    
    os.chdir(web_path)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        httpd.serve_forever()

def start_web_server():
    web_path = get_web_path()
    if os.path.exists(web_path):
        thread = threading.Thread(target=start_simple_http_server, args=(WEB_PORT, web_path), daemon=True)
        thread.start()
        QTimer.singleShot(1000, lambda: webbrowser.open(f'http://localhost:{WEB_PORT}'))
    else:
        QMessageBox.warning(None, "Ошибка", f"Веб-версия не найдена!\nПуть: {web_path}")

def start_desktop_app():
    exe_path = get_desktop_exe_path()
    if os.path.exists(exe_path):
        subprocess.Popen([exe_path])
    else:
        QMessageBox.warning(None, "Ошибка", f"Десктоп приложение не найдено!\nПуть: {exe_path}")

class InstallerWindow:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.window.setFixedSize(500, 350)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        title = QLabel("Telegram Caller")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Универсальный клиент для звонков")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #888;")
        
        web_btn = QPushButton("Веб-версия")
        web_btn.setFont(QFont("Arial", 12))
        web_btn.setMinimumHeight(50)
        web_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        web_btn.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #4338ca; }
        """)
        web_btn.clicked.connect(start_web_server)
        
        desktop_btn = QPushButton("Десктоп приложение")
        desktop_btn.setFont(QFont("Arial", 12))
        desktop_btn.setMinimumHeight(50)
        desktop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        desktop_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #047857; }
        """)
        desktop_btn.clicked.connect(start_desktop_app)
        
        version_label = QLabel(f"Версия {APP_VERSION}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #666; font-size: 10px;")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(web_btn)
        layout.addWidget(desktop_btn)
        layout.addStretch()
        layout.addWidget(version_label)
        
        self.window.setLayout(layout)
        self.window.setStyleSheet("QWidget { background-color: #1a1a2e; color: white; }")
    
    def run(self):
        self.window.show()
        return self.app.exec()

def run_console():
    print(f"Telegram Caller v{APP_VERSION}")
    print("1 - Веб-версия | 2 - Десктоп | 0 - Выход")
    choice = input("Выбор: ").strip()
    
    if choice == "1":
        print(f"Запуск веб-версии на порту {WEB_PORT}...")
        start_web_server()
        print(f"Откройте http://localhost:{WEB_PORT}")
    elif choice == "2":
        start_desktop_app()

def main():
    if PYQT_AVAILABLE:
        w = InstallerWindow()
        sys.exit(w.run())
    else:
        run_console()

if __name__ == "__main__":
    main()