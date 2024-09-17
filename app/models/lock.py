import sys
import os
import http
import json
import logging
from typing import Tuple, Optional
from datetime import datetime, timedelta
from random import randint

import pytz
from pydantic import BaseModel
from dotenv import load_dotenv

from seam import Seam
from .event import Event, EventLock
from app.modules.branch import *
from app.modules.lock import *
from app.models.branch import Branch

load_dotenv()

class Lock(BaseModel):
    name: Optional[str]
    lock_id: Optional[str]
    lock_name: Optional[str]
    passcode: Optional[int]
    start_time: Optional[str]
    end_time: Optional[str]
    cooperator_id: int
    event_data: EventLock
    branch_info: Branch

class SeamLock(Seam):
    def __init__(self, api_key: str, event: Event) -> None:
        super().__init__(api_key=api_key)
        self.events = event
        self.name = self.events.data_.name
        self.lock_id, self.lock_name = self.get_lock_id()
        self.passcode = self.create_passcode()
        self.cooperator_id = self.events.data_.cooperator_id
        self.start_format_time, self.end_format_time = self.get_format_time()

    def get_lock_id(self) -> Tuple[Optional[str], Optional[str]]:
        try:
            if self.events.data_.cooperator_id in locks:
                lock_name = locks[self.events.data_.cooperator_id]
                lock = next((lock for lock in self.locks.list() if lock.properties.name == lock_name), None)
                return (lock.device_id, lock_name) if lock else (None, None)
            else:
                return None, None
        except Exception as e:
            logging.error(f"Error occurred in get_lock_id: {e}")
            return None, None

    def create_passcode(self) -> Optional[int]:
        try:
            return randint(10000, 99999)
        except Exception as e:
            logging.error(f"Error occurred in create_passcode: {e}")
            return None

    def get_format_time(self) -> Tuple[str, str]:
        try:
            end_time = datetime.strptime(self.events.data_.record, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=int(self.events.data_.duration))
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
            moscow_start_time = datetime.strptime(self.events.data_.record, '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('Europe/Moscow'))
            moscow_end_time = end_time.astimezone(pytz.timezone('Europe/Moscow'))
            formatted_start_time = moscow_start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
            formatted_end_time = moscow_end_time.strftime('%Y-%m-%dT%H:%M:%S%z')
            return formatted_start_time, formatted_end_time
        except Exception as e:
            logging.error(f"Error occurred in get_format_time: {e}")
            return "", ""

    def create_lock_object(self) -> Lock:
        return Lock(
            name=self.name,
            lock_id=self.lock_id,
            lock_name=self.lock_name,
            passcode=self.passcode,
            start_time=self.start_format_time,
            end_time=self.end_format_time,
            cooperator_id=self.cooperator_id,
            event_data=self.events,
            branch_info=Branch.from_dict(cooperator_id=self.cooperator_id)
        )

    def create_access_code(self) -> Optional[object]:
        try:
            if not all([self.lock_id, self.passcode, self.start_format_time, self.end_format_time]):
                raise ValueError("Missing required data_ for creating access code")
            access_code = self.access_codes.create(
                device_id=self.lock_id,
                code=str(self.passcode),
                name=f"{self.name}",
                starts_at=self.start_format_time,
                ends_at=self.end_format_time
            )
            return self.create_lock_object()
        except Exception as e:
            logging.error(f"Error creating access code: {e}")
            self.passcode = Branch.from_dict(self.cooperator_id).recovery_passcode if Branch.from_dict(self.cooperator_id) else None
            return {"error": f"Error creating access code: {e}"}

    def remove_access_code(self) -> Optional[str]:
        try:
            if not all([self.lock_id, self.passcode]):
                raise ValueError("Missing required data_ for removing access code")
            return self.access_codes.delete(
                device_id=self.lock_id,
                code=str(self.passcode)
            )
        except Exception as e:
            logging.error(f"Error removing access code: {e}")
            return http.HTTPStatus.INTERNAL_SERVER_ERROR
