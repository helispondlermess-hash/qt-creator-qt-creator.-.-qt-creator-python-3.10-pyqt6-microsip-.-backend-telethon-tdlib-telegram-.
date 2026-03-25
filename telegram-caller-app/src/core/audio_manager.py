# -*- coding: utf-8 -*-
"""
Менеджер аудио - управление устройствами ввода/вывода звука
"""

from typing import List, Optional, Dict
import platform

from ..utils.logger import logger


class AudioManager:
    """
    Класс для управления аудио устройствами
    """
    
    def __init__(self):
        self._input_devices: List[Dict[str, str]] = []
        self._output_devices: List[Dict[str, str]] = []
        self._current_input: Optional[str] = None
        self._current_output: Optional[str] = None
        self._is_muted = False
        self._volume = 100
        
        self._initialize_devices()
        logger.info("AudioManager инициализирован")
    
    def _initialize_devices(self):
        """Инициализация аудио устройств"""
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            
            if isinstance(devices, dict):
                self._input_devices = [{'id': devices['index'], 'name': devices['name']}]
                self._output_devices = [{'id': devices['index'], 'name': devices['name']}]
            else:
                for device in devices:
                    if device['max_input_channels'] > 0:
                        self._input_devices.append({
                            'id': device['index'],
                            'name': device['name']
                        })
                    if device['max_output_channels'] > 0:
                        self._output_devices.append({
                            'id': device['index'],
                            'name': device['name']
                        })
            
            if self._input_devices:
                self._current_input = self._input_devices[0]['name']
            if self._output_devices:
                self._current_output = self._output_devices[0]['name']
                
        except ImportError:
            logger.warning("sounddevice не установлен, используются системные устройства")
            self._set_default_devices()
        except Exception as e:
            logger.error(f"Ошибка инициализации аудио: {e}")
            self._set_default_devices()
    
    def _set_default_devices(self):
        """Установка устройств по умолчанию"""
        if platform.system() == "Windows":
            self._input_devices = [{'id': 'default', 'name': 'Default'}]
            self._output_devices = [{'id': 'default', 'name': 'Default'}]
        else:
            self._input_devices = [
                {'id': 'pulse', 'name': 'PulseAudio'},
                {'id': 'default', 'name': 'Default'}
            ]
            self._output_devices = [
                {'id': 'pulse', 'name': 'PulseAudio'},
                {'id': 'default', 'name': 'Default'}
            ]
        
        self._current_input = self._input_devices[0]['name']
        self._current_output = self._output_devices[0]['name']
    
    def get_input_devices(self) -> List[Dict[str, str]]:
        """Получение списка устройств ввода"""
        return self._input_devices
    
    def get_output_devices(self) -> List[Dict[str, str]]:
        """Получение списка устройств вывода"""
        return self._output_devices
    
    def set_input_device(self, device_name: str) -> bool:
        """Установка устройства ввода"""
        for device in self._input_devices:
            if device['name'] == device_name:
                self._current_input = device_name
                logger.info(f"Устройство ввода установлено: {device_name}")
                return True
        return False
    
    def set_output_device(self, device_name: str) -> bool:
        """Установка устройства вывода"""
        for device in self._output_devices:
            if device['name'] == device_name:
                self._current_output = device_name
                logger.info(f"Устройство вывода установлено: {device_name}")
                return True
        return False
    
    def get_current_input(self) -> Optional[str]:
        """Получение текущего устройства ввода"""
        return self._current_input
    
    def get_current_output(self) -> Optional[str]:
        """Получение текущего устройства вывода"""
        return self._current_output
    
    def toggle_mute(self) -> bool:
        """Переключение mute"""
        self._is_muted = not self._is_muted
        logger.info(f"Mute: {self._is_muted}")
        return self._is_muted
    
    def set_mute(self, muted: bool):
        """Установка mute"""
        self._is_muted = muted
        logger.info(f"Mute установлен: {muted}")
    
    def is_muted(self) -> bool:
        """Проверка mute"""
        return self._is_muted
    
    def set_volume(self, volume: int):
        """Установка громкости (0-100)"""
        self._volume = max(0, min(100, volume))
        logger.info(f"Громкость: {self._volume}")
    
    def get_volume(self) -> int:
        """Получение громкости"""
        return self._volume
    
    def start_capture(self) -> bool:
        """Начало захвата аудио"""
        if not self._current_input:
            logger.warning("Устройство ввода не выбрано")
            return False
        
        logger.info("Начало захвата аудио")
        return True
    
    def stop_capture(self):
        """Остановка захвата аудио"""
        logger.info("Остановка захвата аудио")
    
    def start_playback(self) -> bool:
        """Начало воспроизведения"""
        if not self._current_output:
            logger.warning("Устройство вывода не выбрано")
            return False
        
        logger.info("Начало воспроизведения")
        return True
    
    def stop_playback(self):
        """Остановка воспроизведения"""
        logger.info("Остановка воспроизведения")


class VideoManager:
    """
    Класс для управления видео (заглушка для включения камеры)
    """
    
    def __init__(self):
        self._is_camera_on = False
        self._current_device = 0
        self._available_cameras: List[Dict[str, object]] = []
        
        self._detect_cameras()
        logger.info("VideoManager инициализирован")
    
    def _detect_cameras(self):
        """Обнаружение доступных камер"""
        try:
            import cv2
            for i in range(5):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    self._available_cameras.append({'id': i, 'name': f'Camera {i}'})
                    cap.release()
        except ImportError:
            logger.warning("OpenCV не установлен")
            self._available_cameras = [{'id': 0, 'name': 'Default Camera'}]
        except Exception as e:
            logger.error(f"Ошибка обнаружения камер: {e}")
            self._available_cameras = [{'id': 0, 'name': 'Default Camera'}]
    
    def get_available_cameras(self) -> List[Dict]:
        """Получение списка доступных камер"""
        return self._available_cameras
    
    def toggle_camera(self, device_id: int = 0) -> bool:
        """Включение/выключение камеры"""
        if self._is_camera_on:
            self._stop_camera()
            return False
        else:
            return self._start_camera(device_id)
    
    def _start_camera(self, device_id: int) -> bool:
        """Запуск камеры"""
        try:
            import cv2
            self._capture = cv2.VideoCapture(device_id)
            
            if self._capture.isOpened():
                self._is_camera_on = True
                self._current_device = device_id
                logger.info(f"Камера включена: устройство {device_id}")
                return True
            else:
                logger.error(f"Не удалось открыть камеру: {device_id}")
                return False
                
        except ImportError:
            logger.warning("OpenCV не установлен")
            return False
        except Exception as e:
            logger.error(f"Ошибка запуска камеры: {e}")
            return False
    
    def _stop_camera(self):
        """Остановка камеры"""
        if hasattr(self, '_capture') and self._capture:
            self._capture.release()
        self._is_camera_on = False
        logger.info("Камера выключена")
    
    def is_camera_on(self) -> bool:
        """Проверка состояния камеры"""
        return self._is_camera_on
    
    def get_frame(self):
        """Получение кадра с камеры"""
        if self._is_camera_on and hasattr(self, '_capture'):
            ret, frame = self._capture.read()
            if ret:
                return frame
        return None
    
    def get_current_device(self) -> int:
        """Получение текущего устройства камеры"""
        return self._current_device