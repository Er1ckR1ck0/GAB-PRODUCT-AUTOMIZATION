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
from .event import EventLock
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
    def __init__(self, api_key: str, event: EventLock) -> None:
        super().__init__(api_key=api_key)
        self.events = event
        self.name = self.events.data_.name
        self.cooperator_id = self.events.data_.cooperator_id
        self.start_format_time, self.end_format_time = self.get_format_time()
        self.passcode = str(randint(10000, 99999))
        self.lock_id = locks[self.cooperator_id]

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
            if isinstance(self.lock_id, list):
                for lock_id in self.lock_id:
                    self.access_codes.create(
                        device_id=lock_id,
                        code=str(self.passcode),
                        name=self.name,
                        starts_at=self.start_format_time,
                        ends_at=self.end_format_time
                    )
            return self.create_lock_object()
        except Exception as e:
            logging.error(f"Error creating access code: {e}")
            self.passcode = Branch.from_dict(self.cooperator_id).recovery_passcode if Branch.from_dict(self.cooperator_id) else None
            return {"error": f"Error creating access code: {e}"}

    # def remove_access_code(self) -> Optional[str]:
    #     try:
    #         if isinstance(self.lock_id, list):
    #             for lock_id in self.lock_id:
    #                 self.access_codes.delete(
    #                     device_id=self.lock_id,
    #                     access_code_id=
    #                 )
    #         return self.access_codes.delete(
    #             device_id=self.lock_id,
    #             code=str(self.passcode)
    #         )
    #     except Exception as e:
    #         logging.error(f"Error removing access code: {e}")
    #         return http.HTTPStatus.INTERNAL_SERVER_ERROR
