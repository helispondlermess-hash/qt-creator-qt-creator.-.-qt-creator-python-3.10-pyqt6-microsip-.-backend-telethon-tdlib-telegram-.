# -*- coding: utf-8 -*-
"""
Менеджер звонков - управление состоянием звонков
"""

from enum import Enum
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from ..utils.logger import logger


class CallState(Enum):
    """Состояния звонка"""
    IDLE = "idle"
    CALLING = "calling"
    RINGING = "ringing"
    CONNECTED = "connected"
    ON_HOLD = "on_hold"
    ENDED = "ended"
    FAILED = "failed"


@dataclass
class CallInfo:
    """Информация о звонке"""
    call_id: int
    peer_id: int
    peer_name: str
    state: CallState
    start_time: Optional[datetime] = None
    duration: int = 0
    is_video: bool = False
    is_muted: bool = False
    is_on_hold: bool = False


class CallManager:
    """
    Класс для управления звонками
    """
    
    def __init__(self):
        self._current_call: Optional[CallInfo] = None
        self._call_history: list = []
        self._on_state_changed: Optional[Callable] = None
        self._on_call_started: Optional[Callable] = None
        self._on_call_ended: Optional[Callable] = None
        
        logger.info("CallManager инициализирован")
    
    @property
    def current_call(self) -> Optional[CallInfo]:
        """Получение текущего звонка"""
        return self._current_call
    
    @property
    def is_in_call(self) -> bool:
        """Проверка нахождения в звонке"""
        return self._current_call is not None and self._current_call.state in [
            CallState.CALLING, CallState.RINGING, CallState.CONNECTED, CallState.ON_HOLD
        ]
    
    def set_state_changed_callback(self, callback: Callable):
        """Установка колбэка при изменении состояния"""
        self._on_state_changed = callback
    
    def set_call_started_callback(self, callback: Callable):
        """Установка колбэка при начале звонка"""
        self._on_call_started = callback
    
    def set_call_ended_callback(self, callback: Callable):
        """Установка колбэка при завершении звонка"""
        self._on_call_ended = callback
    
    def start_call(self, call_id: int, peer_id: int, peer_name: str, 
                   is_video: bool = False) -> CallInfo:
        """
        Начало нового звонка
        
        Args:
            call_id: ID звонка
            peer_id: ID абонента
            peer_name: Имя абонента
            is_video: Видеозвонок
            
        Returns:
            Информация о звонке
        """
        self._current_call = CallInfo(
            call_id=call_id,
            peer_id=peer_id,
            peer_name=peer_name,
            state=CallState.CALLING,
            start_time=datetime.now(),
            is_video=is_video
        )
        
        logger.info(f"Звонок начат: {peer_name} (ID: {call_id})")
        
        if self._on_call_started:
            self._on_call_started(self._current_call)
        
        if self._on_state_changed:
            self._on_state_changed(CallState.CALLING)
        
        return self._current_call
    
    def set_state(self, state: CallState):
        """
        Установка состояния звонка
        
        Args:
            state: Новое состояние
        """
        if self._current_call:
            self._current_call.state = state
            
            if state == CallState.CONNECTED:
                logger.info(f"Звонок подключён: {self._current_call.peer_name}")
            
            if self._on_state_changed:
                self._on_state_changed(state)
    
    def toggle_mute(self) -> bool:
        """
        Переключение режима mute
        
        Returns:
            Новое состояние mute
        """
        if self._current_call:
            self._current_call.is_muted = not self._current_call.is_muted
            logger.info(f"Mute переключён: {self._current_call.is_muted}")
            return self._current_call.is_muted
        return False
    
    def toggle_hold(self) -> bool:
        """
        Переключение режима удержания
        
        Returns:
            Новое состояние hold
        """
        if self._current_call:
            self._current_call.is_on_hold = not self._current_call.is_on_hold
            
            if self._current_call.is_on_hold:
                self.set_state(CallState.ON_HOLD)
            else:
                self.set_state(CallState.CONNECTED)
            
            logger.info(f"Hold переключён: {self._current_call.is_on_hold}")
            return self._current_call.is_on_hold
        return False
    
    def end_call(self, reason: str = "Завершено пользователем") -> Dict[str, Any]:
        """
        Завершение текущего звонка
        
        Args:
            reason: Причина завершения
            
        Returns:
            Информация о завершённом звонке
        """
        if self._current_call:
            call_info = self._current_call
            
            if call_info.start_time:
                call_info.duration = int((datetime.now() - call_info.start_time).total_seconds())
            
            call_info.state = CallState.ENDED
            
            self._call_history.append(call_info)
            
            logger.info(f"Звонок завершён: {call_info.peer_name}, длительность: {call_info.duration}с")
            
            result = {
                "call_id": call_info.call_id,
                "peer_name": call_info.peer_name,
                "duration": call_info.duration,
                "reason": reason
            }
            
            if self._on_call_ended:
                self._on_call_ended(result)
            
            if self._on_state_changed:
                self._on_state_changed(CallState.ENDED)
            
            self._current_call = None
            return result
        
        return {"error": "Нет активного звонка"}
    
    def call_failed(self, error: str):
        """
        Обработка ошибки звонка
        
        Args:
            error: Сообщение об ошибке
        """
        if self._current_call:
            self._current_call.state = CallState.FAILED
            
            logger.error(f"Звонок не удался: {error}")
            
            if self._on_state_changed:
                self._on_state_changed(CallState.FAILED)
            
            self._current_call = None
    
    def get_call_history(self) -> list:
        """Получение истории звонков"""
        return self._call_history.copy()
    
    def get_call_duration(self) -> int:
        """Получение длительности текущего звонка"""
        if self._current_call and self._current_call.start_time:
            return int((datetime.now() - self._current_call.start_time).total_seconds())
        return 0
