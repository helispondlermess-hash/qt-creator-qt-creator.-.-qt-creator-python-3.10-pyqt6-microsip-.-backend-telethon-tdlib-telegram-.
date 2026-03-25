# -*- mode: python ; coding: utf-8 -*-
"""
Спецификация PyInstaller для сборки Telegram Caller в один EXE файл

Сборка: pyinstaller telegram_caller.spec
"""

import os
import sys
from pathlib import Path

block_cipher = None

# Пути
ROOT_DIR = Path(SPECPATH)
ASSETS_DIR = ROOT_DIR / 'assets'

a = Analysis(
    ['main.py'],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=[
        # Добавляем assets если есть
        # (str(ASSETS_DIR), 'assets'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'telethon',
        'telethon.network',
        'telethon.client',
        'telethon.crypto',
        'sounddevice',
        'cv2',
        'numpy',
        'asyncio',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'PySide2',
        'PySide6',
        'PyQt5',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TelegramCaller',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Без консоли для десктопного приложения
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Добавить иконку если нужно: 'assets/icon.ico'
    version_file='version.txt',
)

# Для включения всех зависимостей (Target ~1.5GB)
# Добавить все необходимые библиотеки
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TelegramCaller',
)