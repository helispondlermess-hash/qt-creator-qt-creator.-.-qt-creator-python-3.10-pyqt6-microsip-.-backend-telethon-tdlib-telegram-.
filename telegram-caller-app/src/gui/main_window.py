# -*- coding: utf-8 -*-
"""
Главное окно приложения Telegram Caller
Современный тёмный дизайн в стиле синего/фиолетового
"""

import sys
import asyncio
from typing import Optional
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QTabWidget, QStatusBar, QComboBox, QGroupBox, QFrame,
    QDialog, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QFont, QAction

from .styles import DARK_STYLE, CALL_UI_STYLE
from ..core.telegram_client import TelegramClient
from ..core.call_manager import CallManager, CallState
from ..core.audio_manager import AudioManager, VideoManager
from ..utils.validators import validate_phone_number, validate_username
from ..utils.logger import logger


class AuthDialog(QDialog):
    """Диалог авторизации"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Авторизация Telegram")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel("Вход в Telegram")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.phone_label = QLabel("Номер телефона:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+7XXXXXXXXXX")
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        
        self.code_label = QLabel("Код подтверждения:")
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Введите код из SMS")
        self.code_input.setEnabled(False)
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_input)
        
        self.password_label = QLabel("2FA пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setEnabled(False)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
        self.setLayout(layout)
        self.setStyleSheet(DARK_STYLE)


class CallWidget(QFrame):
    """Виджет активного звонка"""
    
    call_ended = pyqtSignal()
    mute_toggled = pyqtSignal(bool)
    video_toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CallWidget")
        self._is_muted = False
        self._is_video = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.caller_name = QLabel("Имя абонента")
        self.caller_name.setObjectName("CallerNameLabel")
        self.caller_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.caller_name)
        
        self.call_status = QLabel("Соединение...")
        self.call_status.setObjectName("CallStatusLabel")
        self.call_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.call_status)
        
        self.duration_label = QLabel("00:00")
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.duration_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        layout.addWidget(self.duration_label)
        
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)
        
        self.mute_btn = QPushButton("🎤")
        self.mute_btn.setObjectName("MuteButton")
        self.mute_btn.setFixedSize(60, 60)
        self.mute_btn.clicked.connect(self._on_mute_clicked)
        controls_layout.addWidget(self.mute_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.video_btn = QPushButton("📹")
        self.video_btn.setObjectName("VideoButton")
        self.video_btn.setFixedSize(60, 60)
        self.video_btn.clicked.connect(self._on_video_clicked)
        controls_layout.addWidget(self.video_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.end_btn = QPushButton("Завершить")
        self.end_btn.setObjectName("EndCallButton")
        self.end_btn.setFixedSize(120, 50)
        self.end_btn.clicked.connect(self.call_ended.emit)
        controls_layout.addWidget(self.end_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(controls_layout)
        
        self.setLayout(layout)
        self.setStyleSheet(DARK_STYLE + CALL_UI_STYLE)
        self.setVisible(False)
    
    def _on_mute_clicked(self):
        self._is_muted = not self._is_muted
        self.mute_btn.setText("🔇" if self._is_muted else "🎤")
        self.mute_toggled.emit(self._is_muted)
    
    def _on_video_clicked(self):
        self._is_video = not self._is_video
        self.video_btn.setText("📹" if self._is_video else "📷")
        self.video_toggled.emit(self._is_video)
    
    def set_caller_name(self, name: str):
        self.caller_name.setText(name)
    
    def set_status(self, status: str):
        self.call_status.setText(status)
    
    def update_duration(self, duration: int):
        mins = duration // 60
        secs = duration % 60
        self.duration_label.setText(f"{mins:02d}:{secs:02d}")


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Caller")
        self.setFixedSize(450, 700)
        
        self.telegram_client: Optional[TelegramClient] = None
        self.call_manager = CallManager()
        self.audio_manager = AudioManager()
        self.video_manager = VideoManager()
        
        self._auth_phone = ""
        self._auth_code_hash = ""
        
        self._setup_ui()
        self._setup_callbacks()
        self._apply_styles()
        
        logger.info("Главное окно создано")
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        header_layout = QHBoxLayout()
        self.title_label = QLabel("Telegram Caller")
        self.title_label.setObjectName("TitleLabel")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        self.auth_status_label = QLabel("Не авторизован")
        self.auth_status_label.setObjectName("StatusLabel")
        header_layout.addWidget(self.auth_status_label)
        main_layout.addLayout(header_layout)
        
        self.tabs = QTabWidget()
        
        self.dial_tab = self._create_dial_tab()
        self.contacts_tab = self._create_contacts_tab()
        self.settings_tab = self._create_settings_tab()
        
        self.tabs.addTab(self.dial_tab, "Набор")
        self.tabs.addTab(self.contacts_tab, "Контакты")
        self.tabs.addTab(self.settings_tab, "Настройки")
        
        main_layout.addWidget(self.tabs)
        
        self.call_widget = CallWidget()
        self.call_widget.call_ended.connect(self._on_end_call)
        self.call_widget.mute_toggled.connect(self._on_mute_toggled)
        self.call_widget.video_toggled.connect(self._on_video_toggled)
        main_layout.addWidget(self.call_widget)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")
        
        central_widget.setLayout(main_layout)
    
    def _create_dial_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Введите номер или @username")
        self.number_input.setFont(QFont("Segoe UI", 14))
        layout.addWidget(self.number_input)
        
        dial_pad_layout = QGridLayout()
        
        buttons = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("*", 3, 0), ("0", 3, 1), ("#", 3, 2),
        ]
        
        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(80, 60)
            btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
            btn.clicked.connect(lambda checked, t=text: self._on_dial_pad_click(t))
            dial_pad_layout.addWidget(btn, row, col)
        
        layout.addLayout(dial_pad_layout)
        
        call_buttons_layout = QHBoxLayout()
        
        self.call_btn = QPushButton("📞 Позвонить")
        self.call_btn.setObjectName("CallButton")
        self.call_btn.setFixedHeight(50)
        self.call_btn.clicked.connect(self._on_call_clicked)
        call_buttons_layout.addWidget(self.call_btn)
        
        widget.setLayout(layout)
        return widget
    
    def _create_contacts_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск контактов...")
        self.search_input.textChanged.connect(self._on_search_changed)
        layout.addWidget(self.search_input)
        
        self.contacts_list = QListWidget()
        self.contacts_list.itemDoubleClicked.connect(self._on_contact_double_clicked)
        layout.addWidget(self.contacts_list)
        
        widget.setLayout(layout)
        return widget
    
    def _create_settings_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        
        audio_group = QGroupBox("Аудио")
        audio_layout = QVBoxLayout()
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Микрофон:"))
        self.input_combo = QComboBox()
        self._populate_audio_devices()
        input_layout.addWidget(self.input_combo)
        audio_layout.addLayout(input_layout)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Динамики:"))
        self.output_combo = QComboBox()
        output_layout.addWidget(self.output_combo)
        audio_layout.addLayout(output_layout)
        
        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)
        
        video_group = QGroupBox("Видео")
        video_layout = QVBoxLayout()
        
        self.camera_combo = QComboBox()
        for cam in self.video_manager.get_available_cameras():
            self.camera_combo.addItem(cam['name'], cam['id'])
        video_layout.addWidget(QLabel("Камера:"))
        video_layout.addWidget(self.camera_combo)
        
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)
        
        login_group = QGroupBox("Аккаунт")
        login_layout = QVBoxLayout()
        
        self.login_btn = QPushButton("Войти / Авторизоваться")
        self.login_btn.clicked.connect(self._on_login_clicked)
        login_layout.addWidget(self.login_btn)
        
        self.logout_btn = QPushButton("Выйти")
        self.logout_btn.clicked.connect(self._on_logout_clicked)
        self.logout_btn.setEnabled(False)
        login_layout.addWidget(self.logout_btn)
        
        login_group.setLayout(login_layout)
        layout.addWidget(login_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _populate_audio_devices(self):
        self.input_combo.clear()
        for device in self.audio_manager.get_input_devices():
            self.input_combo.addItem(device['name'], device['id'])
        
        self.output_combo.clear()
        for device in self.audio_manager.get_output_devices():
            self.output_combo.addItem(device['name'], device['id'])
    
    def _apply_styles(self):
        self.setStyleSheet(DARK_STYLE)
    
    def _setup_callbacks(self):
        self.call_manager.set_state_changed_callback(self._on_call_state_changed)
        self.call_manager.set_call_started_callback(self._on_call_started)
        self.call_manager.set_call_ended_callback(self._on_call_ended)
        
        self.duration_timer = QTimer()
        self.duration_timer.timeout.connect(self._update_call_duration)
    
    def _on_dial_pad_click(self, digit: str):
        current = self.number_input.text()
        self.number_input.setText(current + digit)
    
    def _on_call_clicked(self):
        target = self.number_input.text().strip()
        
        if not target:
            self.status_bar.showMessage("Введите номер или username")
            return
        
        if validate_username(target):
            self._initiate_call_to_username(target)
        elif validate_phone_number(target):
            self._initiate_call_to_phone(target)
        else:
            self.status_bar.showMessage("Неверный формат номера или username")
    
    def _initiate_call_to_username(self, username: str):
        self.status_bar.showMessage(f"Звоним {username}...")
        logger.info(f"Инициируем звонок на {username}")
        
        self.call_widget.set_caller_name(username)
        self.call_widget.set_status("Звоним...")
        self.call_widget.setVisible(True)
        
        self.call_manager.start_call(
            call_id=1,
            peer_id=0,
            peer_name=username,
            is_video=False
        )
        
        self.call_widget.set_status("Ожидание ответа...")
        self.duration_timer.start(1000)
    
    def _initiate_call_to_phone(self, phone: str):
        self.status_bar.showMessage(f"Звоним на {phone}...")
        logger.info(f"Инициируем звонок на {phone}")
        
        self.call_widget.set_caller_name(phone)
        self.call_widget.set_status("Звоним...")
        self.call_widget.setVisible(True)
        
        self.call_manager.start_call(
            call_id=1,
            peer_id=0,
            peer_name=phone,
            is_video=False
        )
        
        self.call_widget.set_status("Ожидание ответа...")
        self.duration_timer.start(1000)
    
    def _on_end_call(self):
        result = self.call_manager.end_call()
        self.duration_timer.stop()
        self.call_widget.setVisible(False)
        self.status_bar.showMessage(f"Звонок завершён. Длительность: {result.get('duration', 0)}с")
        self.number_input.clear()
    
    def _on_mute_toggled(self, muted: bool):
        self.audio_manager.set_mute(muted)
        status = "выключен" if muted else "включён"
        self.status_bar.showMessage(f"Микрофон {status}")
    
    def _on_video_toggled(self, enabled: bool):
        self.video_manager.toggle_camera()
        status = "включена" if enabled else "выключена"
        self.status_bar.showMessage(f"Камера {status}")
    
    def _on_call_state_changed(self, state: CallState):
        if state == CallState.CONNECTED:
            self.call_widget.set_status("Разговор")
        elif state == CallState.ENDED:
            self._on_end_call()
        elif state == CallState.FAILED:
            self.call_widget.set_status("Ошибка звонка")
            self.status_bar.showMessage("Звонок не удался")
    
    def _on_call_started(self, call_info):
        self.call_widget.set_caller_name(call_info.peer_name)
        self.call_widget.setVisible(True)
    
    def _on_call_ended(self, result):
        self.duration_timer.stop()
        self.call_widget.setVisible(False)
    
    def _update_call_duration(self):
        duration = self.call_manager.get_call_duration()
        self.call_widget.update_duration(duration)
    
    def _on_login_clicked(self):
        dialog = AuthDialog(self)
        dialog.phone_input.textChanged.connect(
            lambda: self._on_auth_phone_changed(dialog))
        
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            phone = dialog.phone_input.text().strip()
            code = dialog.code_input.text().strip()
            password = dialog.password_input.text().strip()
            
            if phone and not code and not password:
                self._start_auth(phone, dialog)
            elif code:
                self._verify_code(code, phone, dialog)
            elif password:
                self._verify_2fa(password, phone, dialog)
    
    def _on_auth_phone_changed(self, dialog: AuthDialog):
        phone = dialog.phone_input.text().strip()
        
        if validate_phone_number(phone):
            dialog.status_label.setText("Нажмите OK для отправки кода")
            dialog.status_label.setStyleSheet("color: #7b2cbf;")
        else:
            dialog.status_label.setText("Введите корректный номер")
            dialog.status_label.setStyleSheet("color: #c0392b;")
    
    def _start_auth(self, phone: str, dialog: AuthDialog):
        dialog.status_label.setText("Отправка кода...")
        
        self.telegram_client = TelegramClient()
        self._auth_phone = phone
        
        asyncio.run(self._async_start_auth(phone, dialog))
    
    async def _async_start_auth(self, phone: str, dialog: AuthDialog):
        try:
            await self.telegram_client.connect()
            result = await self.telegram_client.send_code_request(phone)
            
            if result.get("success"):
                self._auth_code_hash = result["phone_code_hash"]
                dialog.code_input.setEnabled(True)
                dialog.status_label.setText("Код отправлен! Введите его")
                dialog.status_label.setStyleSheet("color: #27ae60;")
            else:
                dialog.status_label.setText(f"Ошибка: {result.get('error')}")
                dialog.status_label.setStyleSheet("color: #c0392b;")
                
        except Exception as e:
            dialog.status_label.setText(f"Ошибка: {str(e)}")
            dialog.status_label.setStyleSheet("color: #c0392b;")
    
    def _verify_code(self, code: str, phone: str, dialog: AuthDialog):
        asyncio.run(self._async_verify_code(code, phone, dialog))
    
    async def _async_verify_code(self, code: str, phone: str, dialog: AuthDialog):
        try:
            result = await self.telegram_client.verify_code(
                code, phone, self._auth_code_hash
            )
            
            if result.get("success"):
                dialog.status_label.setText("Авторизация успешна!")
                self._on_auth_success()
                dialog.accept()
            elif result.get("requires_2fa"):
                dialog.password_input.setEnabled(True)
                dialog.status_label.setText("Введите 2FA пароль")
            else:
                dialog.status_label.setText(f"Ошибка: {result.get('error')}")
                
        except Exception as e:
            dialog.status_label.setText(f"Ошибка: {str(e)}")
    
    def _verify_2fa(self, password: str, phone: str, dialog: AuthDialog):
        asyncio.run(self._async_verify_2fa(password, phone, dialog))
    
    async def _async_verify_2fa(self, password: str, phone: str, dialog: AuthDialog):
        try:
            result = await self.telegram_client.verify_2fa_password(
                password, phone, self._auth_code_hash
            )
            
            if result.get("success"):
                dialog.status_label.setText("Авторизация успешна!")
                self._on_auth_success()
                dialog.accept()
            else:
                dialog.status_label.setText(f"Ошибка: {result.get('error')}")
                
        except Exception as e:
            dialog.status_label.setText(f"Ошибка: {str(e)}")
    
    def _on_auth_success(self):
        self.auth_status_label.setText("Авторизован")
        self.auth_status_label.setStyleSheet("color: #27ae60;")
        self.login_btn.setEnabled(False)
        self.logout_btn.setEnabled(True)
        self.status_bar.showMessage("Авторизация успешна!")
        
        self._load_contacts()
    
    def _on_logout_clicked(self):
        if self.telegram_client:
            asyncio.run(self.telegram_client.disconnect())
        
        self.telegram_client = None
        self.auth_status_label.setText("Не авторизован")
        self.auth_status_label.setStyleSheet("")
        self.login_btn.setEnabled(True)
        self.logout_btn.setEnabled(False)
        self.status_bar.showMessage("Вы вышли из аккаунта")
    
    def _load_contacts(self):
        if not self.telegram_client:
            return
        
        asyncio.run(self._async_load_contacts())
    
    async def _async_load_contacts(self):
        try:
            contacts = await self.telegram_client.get_contacts()
            self.contacts_list.clear()
            
            for contact in contacts:
                item = QListWidgetItem(contact['display_name'])
                item.setData(Qt.ItemDataRole.UserRole, contact)
                self.contacts_list.addItem(item)
                
        except Exception as e:
            logger.error(f"Ошибка загрузки контактов: {e}")
    
    def _on_search_changed(self, text: str):
        for i in range(self.contacts_list.count()):
            item = self.contacts_list.item(i)
            contact = item.data(Qt.ItemDataRole.UserRole)
            
            if text.lower() in contact.get('display_name', '').lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
    
    def _on_contact_double_clicked(self, item: QListWidgetItem):
        contact = item.data(Qt.ItemDataRole.UserRole)
        
        username = contact.get('username')
        phone = contact.get('phone')
        
        if username:
            self.number_input.setText(f"@{username}")
            self._initiate_call_to_username(username)
        elif phone:
            self.number_input.setText(phone)
            self._initiate_call_to_phone(phone)
    
    def closeEvent(self, event):
        if self.telegram_client:
            asyncio.run(self.telegram_client.disconnect())
        event.accept()