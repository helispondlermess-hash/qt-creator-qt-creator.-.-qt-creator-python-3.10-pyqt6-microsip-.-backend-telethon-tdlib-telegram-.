# -*- coding: utf-8 -*-
"""
Клиент для взаимодействия с Telegram API
Использует библиотеку Telethon для авторизации и управления звонками
"""

import asyncio
import os
from pathlib import Path
from typing import Optional, Callable, List, Dict, Any

from telethon import TelegramClient as TelethonClient
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    PasswordHashInvalidError
)
from telethon.tl.functions.account import GetPasswordRequest
from telethon.tl.types import User

from ..config import API_ID, API_HASH
from ..utils.logger import logger


class TelegramClient:
    """
    Класс для управления подключением к Telegram и выполнения звонков
    """
    
    def __init__(self, session_path: Optional[str] = None):
        """
        Инициализация клиента
        
        Args:
            session_path: Путь к файлу сессии (по умолчанию создаётся в ~/.telegram_caller/)
        """
        if session_path is None:
            session_dir = Path.home() / '.telegram_caller' / 'sessions'
            session_dir.mkdir(parents=True, exist_ok=True)
            session_path = str(session_dir / 'session')
        
        self._session_path = session_path
        self._client: Optional[TelethonClient] = None
        self._authenticated = False
        self._me: Optional[User] = None
        self._phone_required = False
        self._password_required = False
        self._2fa_password: Optional[str] = None
        
        self._on_auth_code_required: Optional[Callable] = None
        self._on_2fa_password_required: Optional[Callable] = None
        self._on_auth_complete: Optional[Callable] = None
        self._on_connection_status: Optional[Callable] = None
        self._on_call_state_changed: Optional[Callable] = None
        
        logger.info(f"TelegramClient инициализирован с сессией: {session_path}")
    
    @property
    def is_authenticated(self) -> bool:
        """Проверка аутентификации"""
        return self._authenticated
    
    @property
    def me(self) -> Optional[User]:
        """Получение информации о текущем пользователе"""
        return self._me
    
    def set_auth_code_callback(self, callback: Callable):
        """Установка колбэка для запроса кода подтверждения"""
        self._on_auth_code_required = callback
    
    def set_2fa_password_callback(self: Callable):
        """Установка колбэка для запроса 2FA пароля"""
        self._on_2fa_password_required = callback
    
    def set_auth_complete_callback(self, callback: Callable):
        """Установка колбэка при успешной авторизации"""
        self._on_auth_complete = callback
    
    def set_connection_status_callback(self, callback: Callable):
        """Установка колбэка для статуса подключения"""
        self._on_connection_status = callback
    
    def set_call_state_callback(self, callback: Callable):
        """Установка колбэка для изменения состояния звонка"""
        self._on_call_state_changed = callback
    
    async def connect(self) -> bool:
        """
        Подключение к Telegram
        
        Returns:
            True если подключение успешно
        """
        try:
            logger.info("Подключение к Telegram...")
            
            self._client = TelethonClient(
                session=self._session_path,
                api_id=API_ID,
                api_hash=API_HASH,
                device_model="Telegram Caller Desktop",
                app_version="1.0.0",
                system_version="1.0"
            )
            
            await self._client.connect()
            
            if self._on_connection_status:
                self._on_connection_status("connected")
            
            logger.info("Подключение к Telegram успешно")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка подключения к Telegram: {e}")
            if self._on_connection_status:
                self._on_connection_status(f"error: {str(e)}")
            return False
    
    async def disconnect(self):
        """Отключение от Telegram"""
        if self._client:
            try:
                await self._client.disconnect()
                logger.info("Отключение от Telegram")
            except Exception as e:
                logger.error(f"Ошибка при отключении: {e}")
    
    async def check_authorization(self) -> bool:
        """
        Проверка авторизации
        
        Returns:
            True если пользователь авторизован
        """
        if not self._client:
            return False
        
        try:
            self._me = await self._client.get_me()
            self._authenticated = True
            logger.info(f"Пользователь авторизован: {self._me.username or self._me.phone}")
            return True
        except Exception as e:
            logger.info(f"Требуется авторизация: {e}")
            self._authenticated = False
            return False
    
    async def send_code_request(self, phone: str) -> Dict[str, Any]:
        """
        Отправка запроса на код подтверждения
        
        Args:
            phone: Номер телефона
            
        Returns:
            Словарь с результатом
        """
        if not self._client:
            return {"success": False, "error": "Клиент не подключён"}
        
        try:
            result = await self._client.send_code_request(phone)
            logger.info(f"Код подтверждения отправлен на {phone}")
            return {
                "success": True,
                "phone_code_hash": result.phone_code_hash,
                "next_type": str(result.next_type) if result.next_type else None,
                "timeout": result.timeout
            }
        except Exception as e:
            logger.error(f"Ошибка отправки кода: {e}")
            return {"success": False, "error": str(e)}
    
    async def verify_code(self, code: str, phone: str, phone_code_hash: str) -> Dict[str, Any]:
        """
        Проверка кода подтверждения
        
        Args:
            code: Код из SMS
            phone: Номер телефона
            phone_code_hash: Хэш из ответа send_code_request
            
        Returns:
            Словарь с результатом
        """
        if not self._client:
            return {"success": False, "error": "Клиент не подключён"}
        
        try:
            self._me = await self._client.sign_in(
                phone=phone,
                code=code,
                phone_code_hash=phone_code_hash
            )
            self._authenticated = True
            
            if self._on_auth_complete:
                self._on_auth_complete()
            
            logger.info("Авторизация успешна!")
            return {"success": True, "user": self._me}
            
        except SessionPasswordNeededError:
            logger.info("Требуется 2FA пароль")
            self._password_required = True
            return {"success": False, "requires_2fa": True}
            
        except PhoneCodeInvalidError:
            logger.warning("Неверный код подтверждения")
            return {"success": False, "error": "Неверный код подтверждения"}
            
        except Exception as e:
            logger.error(f"Ошибка верификации кода: {e}")
            return {"success": False, "error": str(e)}
    
    async def verify_2fa_password(self, password: str, phone: str, phone_code_hash: str) -> Dict[str, Any]:
        """
        Проверка 2FA пароля
        
        Args:
            password: 2FA пароль
            phone: Номер телефона
            phone_code_hash: Хэш из ответа send_code_request
            
        Returns:
            Словарь с результатом
        """
        if not self._client:
            return {"success": False, "error": "Клиент не подключён"}
        
        try:
            self._me = await self._client.sign_in(
                phone=phone,
                password=password,
                phone_code_hash=phone_code_hash
            )
            self._authenticated = True
            
            if self._on_auth_complete:
                self._on_auth_complete()
            
            logger.info("Авторизация с 2FA успешна!")
            return {"success": True, "user": self._me}
            
        except PasswordHashInvalidError:
            logger.warning("Неверный 2FA пароль")
            return {"success": False, "error": "Неверный пароль"}
            
        except Exception as e:
            logger.error(f"Ошибка верификации 2FA: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_contacts(self) -> List[Dict[str, Any]]:
        """
        Получение списка контактов
        
        Returns:
            Список контактов
        """
        if not self._client or not self._authenticated:
            return []
        
        try:
            contacts = await self._client.get_contacts()
            result = []
            
            for contact in contacts:
                result.append({
                    "id": contact.id,
                    "username": contact.username,
                    "first_name": contact.first_name,
                    "last_name": contact.last_name,
                    "phone": contact.phone,
                    "display_name": contact.first_name or contact.username or contact.phone
                })
            
            logger.info(f"Получено контактов: {len(result)}")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка получения контактов: {e}")
            return []
    
    async def search_users(self, query: str) -> List[Dict[str, Any]]:
        """
        Поиск пользователей по username или номеру телефона
        
        Args:
            query: Запрос для поиска
            
        Returns:
            Список найденных пользователей
        """
        if not self._client or not self._authenticated:
            return []
        
        try:
            if query.startswith('+') or query.isdigit():
                users = await self._client.get_contacts()
                query_digits = ''.join(c for c in query if c.isdigit())
                
                for user in users:
                    if user.phone and query_digits in user.phone.replace('+', ''):
                        return [{
                            "id": user.id,
                            "username": user.username,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "phone": user.phone,
                            "display_name": user.first_name or user.username or user.phone
                        }]
            
            users = await self._client.search(query)
            result = []
            
            for user in users:
                if hasattr(user, 'username'):
                    result.append({
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone": getattr(user, 'phone', None),
                        "display_name": user.first_name or user.username or str(user.id)
                    })
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка поиска пользователей: {e}")
            return []
    
    async def initiate_call(self, user_id: int, video: bool = False) -> Dict[str, Any]:
        """
        Инициирование звонка
        
        Args:
            user_id: ID пользователя
            video: Использовать видеозвонок
            
        Returns:
            Словарь с результатом
        """
        if not self._client or not self._authenticated:
            return {"success": False, "error": "Не авторизован"}
        
        try:
            from telethon.tl.functions.phone import CreateGroupCallRequest
            
            logger.info(f"Инициирование звонка user_id={user_id}, video={video}")
            
            call = await self._client.call(
                user_id=user_id,
                video=video,
                callback=lambda state: self._on_call_state_changed(state) if self._on_call_state_changed else None
            )
            
            logger.info(f"Звонок инициирован: {call}")
            return {"success": True, "call": call}
            
        except Exception as e:
            logger.error(f"Ошибка инициирования звонка: {e}")
            return {"success": False, "error": str(e)}
    
    async def end_call(self, call_id: int) -> Dict[str, Any]:
        """
        Завершение звонка
        
        Args:
            call_id: ID звонка
            
        Returns:
            Словарь с результатом
        """
        if not self._client or not self._authenticated:
            return {"success": False, "error": "Не авторизован"}
        
        try:
            await self._client.disconnect(call_id)
            logger.info(f"Звонок {call_id} завершён")
            return {"success": True}
            
        except Exception as e:
            logger.error(f"Ошибка завершения звонка: {e}")
            return {"success": False, "error": str(e)}


class AsyncCaller:
    """Асинхронный интерфейс для синхронного использования"""
    
    def __init__(self, client: TelegramClient):
        self._client = client
    
    def __getattr__(self, name):
        method = getattr(self._client, name, None)
        if method and callable(method):
            if asyncio.iscoroutinefunction(method):
                def wrapper(*args, **kwargs):
                    loop = asyncio.get_event_loop()
                    return loop.run_until_complete(method(*args, **kwargs))
                return wrapper
        return getattr(self._client, name)
