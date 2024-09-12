from seam import Seam
from event import Event
import sys
import os
from typing import Tuple, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.modules.lock_modules import *
from app.models.branch import Bracnh
from pydantic import BaseModel
from datetime import datetime, timedelta

class Lock(BaseModel):
    name: str
    lock_id: str
    lock_name: str
    passcode: int
    branch_id: int
    branch_info: Bracnh
    
class SeamLock(Seam):
    def __init__(self, api_key: str, event: Event) -> None:
        super().__init__(api_key=api_key)
        self.events = event
        self.name = event.DATA.name
        self.lock_id, self.lock_name = self.get_lock_id
        self.passcode = self.create_passcode
        self.branch_id = event.DATA.branch_id
        self.start_format_time, self.end_format_time = self.get_format_time()

    @property
    def get_lock_id(self) -> Tuple[Optional[str], Optional[str]]:
        try:
            if self.events.DATA.branch_id in locks:
                lock_name = locks[self.events.DATA.branch_id]
                try:
                    lock = next((lock for lock in self.locks.list() if lock.properties.name == lock_name), None)
                    return (lock.device_id, lock_name) if lock else (None, None)
                except Exception as e:
                    print(f"Error getting lock: {e}")
                    return None, None
            else:
                return None, None
        except Exception as e:
            print(f"Error occurred in get_lock_id: {e}")
            return None, None

    @property
    def create_passcode(self) -> Optional[int]:
        try:
            from random import randint
            return randint(1000, 9999)
        except Exception as e:
            print(f"Error occurred in create_passcode: {e}")
            return None

    def get_format_time(self) -> Tuple[str, str]:
        try:
            now = datetime.now()
            start_time = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            end_time = (now + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            return start_time, end_time
        except Exception as e:
            print(f"Error occurred in get_format_time: {e}")
            return "", ""

    def create_lock_object(self) -> Lock:
        return Lock(
            name=self.name,
            lock_id=self.lock_id,
            lock_name=self.lock_name,
            passcode=self.passcode,
            branch_id=self.branch_id,
            branch_info=Bracnh(self.branch_id)
        )

    def create_access_code(self) -> Optional[object]:
        try:
            if not all([self.lock_id, self.passcode, self.start_format_time, self.end_format_time]):
                raise ValueError("Missing required data for creating access code")
            access_code = self.access_codes.create(
                device_id=self.lock_id,
                code=str(self.passcode),
                name=f"Access code for {self.name}",
                starts_at=self.start_format_time,
                ends_at=self.end_format_time
            )
            return self.create_lock_object()
        except Exception as e:
            print(f"Error creating access code: {e}")
            return 2306
    
    def remove_access_code(self) -> Optional[str]:
        try:
            if not all([self.lock_id, self.passcode]):
                raise ValueError("Missing required data for removing access code")
            return self.access_codes.delete(
                device_id=self.lock_id,
                code=str(self.passcode)
            )
        except Exception as e:
            print(f"Error removing access code: {e}")
            return None
