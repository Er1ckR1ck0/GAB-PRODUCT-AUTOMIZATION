from seam import Seam
from .event import Event
import sys
import os
import http
from typing import Tuple, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import json
from app.modules.branch_modules import *
from app.modules.lock_modules import *
from app.models.branch import Branch
from pydantic import BaseModel
from datetime import datetime, timedelta
import pytz
import logging
from dotenv import load_dotenv

load_dotenv()

class Lock(BaseModel):
    name: str
    lock_id: str
    lock_name: str
    passcode: int
    start_time: str
    end_time: str
    cooperator_id: int
    event_data: Event
    branch_info: Branch
    
class SeamLock(Seam):
    def __init__(self, api_key: str, event: Event) -> None:
        super().__init__(api_key=api_key)
        print(type(event), event)
        self.events = event
        self.name = self.events.DATA.name
        self.lock_id, self.lock_name = self.get_lock_id
        self.passcode = self.create_passcode
        self.cooperator_id = self.events.DATA.cooperator_id
        self.start_format_time, self.end_format_time = self.get_format_time()

    @property
    def get_lock_id(self) -> Tuple[Optional[str], Optional[str]]:
        try:
            if self.events.DATA.cooperator_id in locks:
                lock_name = locks[self.events.DATA.cooperator_id]
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
            from random import randint #Refactoring
            return randint(1000, 9999)
        except Exception as e:
            print(f"Error occurred in create_passcode: {e}")
            return None

    def get_format_time(self) -> Tuple[str, str]:
        self.end_time = datetime.strptime(self.events.DATA.record, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=int(self.events.DATA.duration))
        self.end_time = self.end_time.strftime('%Y-%m-%d %H:%M:%S')
        moscow_start_time = datetime.strptime(self.events.DATA.record, '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('Europe/Moscow'))
        moscow_end_time = datetime.strptime(self.end_time, '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('Europe/Moscow'))
        formatted_start_time = moscow_start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
        formatted_end_time = moscow_end_time.strftime('%Y-%m-%dT%H:%M:%S%z')
        return formatted_start_time, formatted_end_time
    
    def create_lock_object(self) -> Lock:
        return Lock(
            name=self.name,
            lock_id=self.lock_id,
            lock_name=self.lock_name,
            passcode=self.passcode,
            start_time=self.start_format_time,
            end_time=self.end_format_time,
            branch_id=self.cooperator_id,
            event_data = self.events,
            branch_info=Branch.from_dict(branch_id=self.cooperator_id)
        )

    def create_access_code(self) -> Optional[object]:
        try:
            if not all([self.lock_id, self.passcode, self.start_format_time, self.end_format_time]):
                raise ValueError("Missing required data for creating access code")
            try:
                access_code = self.access_codes.create(
                    device_id=self.lock_id,
                    code=str(self.passcode),
                    name=f"Access code for {self.name}",
                    starts_at=self.start_format_time,
                    ends_at=self.end_format_time
                )
            except Exception as e:
                if branch_dictionary[self.branch_id]["recovery passcode"]:
                    access_code = self.access_codes.create(
                        device_id=self.lock_id,
                        code=str(branch_dictionary[self.branch_id]["recovery passcode"]),
                        name=f"Access code | {self.name}",
                        starts_at=self.start_format_time,
                        ends_at=self.end_format_time
                    )
                else:
                    self.passcode = None
                    return {"error": f"Error creating access code: {e}"}
            return self.create_lock_object()
        except Exception as e:
            print(f"Error creating access code: {e}")
            self.passcode = Branch(self.cooperator_id).recovery_passcode if Branch(self.cooperator_id) else None
            return http.HTTPStatus.INTERNAL_SERVER_ERROR
    
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
            return http.HTTPStatus.INTERNAL_SERVER_ERROR

data = {
  "from": "user",
  "event": "event-update-record",
  "data": {
    "id": 3894383,
    "whom": 0,
    "created_at": "2024-01-02 23:09:16",
    "updated_at": "2024-01-02 23:10:07",
    "record": "2024-01-10 17:00:00",
    "name": "Nikolai Nesterov",
    "price": "780",
    "phone": "+79035847738",
    "email": "hello.iamegor@yandex.ru",
    "comment": "",
    "status": 3,
    "status_title": "Записан",
    "cooperator_id": 21357,
    "cooperator_title": "САМОРЭК",
    "branch_id": 25261,
    "branch_title": "Studio MINI",
    "service_id": 39420,
    "service_title": "Почасово \"ДНЕВНОЕ\"",
    "url": "https://gabsound.rubitime.ru/widget/card/7cadbffaa754dc8a9ec4bcbc0ee0bdab422e7b0a6309e3461ee04f8b0830c511",
    "coupon": None,
    "coupon_discount": None,
    "source": None,
    "cancelReason": None,
    "duration": "120",
    "prepayment": "780",
    "prepayment_date": "2024-01-02 23:10:07",
    "prepayment_url": "https://gabsound.rubitime.ru/widget/prp/7389438365946d766ac00918",
    "reminder": "2024-01-02 17:00:00",
    "custom_field1": "1",
    "custom_field2": "",
    "custom_field3": "Telegram",
    "custom_field4": "givemecarolcristianpoel",
    "custom_field5": "20.09.2009",
    "custom_field6": "ДА",
    "custom_field7": None,
    "custom_field8": None,
    "custom_field9": None,
    "custom_field10": None
  }
}


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    event_data = json.dumps(data)
    seam_lock = SeamLock(api_key=os.getenv("SEAM_API_KEY"), event=event_data)
    print(seam_lock.start_format_time, seam_lock.end_format_time)
    result = seam_lock.create_lock_object()
    print(result.model_dump_json())
    print(result.branch_info.recovery_passcode)