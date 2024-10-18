from pydantic import BaseModel, Field
from typing import Optional

class EventData(BaseModel):
    id: Optional[int]
    whom: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    record: Optional[str]
    name: Optional[str]
    price: Optional[str] | Optional[int]
    phone: Optional[str]
    email: Optional[str]
    comment: Optional[str]
    status: Optional[int]
    status_title: Optional[str]
    cooperator_id: Optional[int]
    cooperator_title: Optional[str]
    branch_id: Optional[int]
    branch_title: Optional[str]
    service_id: Optional[int]
    service_title: Optional[str]
    url: Optional[str]
    coupon: Optional[str]
    coupon_discount: Optional[str]
    source: Optional[str]
    cancelReason: Optional[str]
    duration: Optional[str]
    prepayment: Optional[str]
    prepayment_date: Optional[str]
    prepayment_url: Optional[str]
    reminder: Optional[str]
    custom_field1: Optional[str]
    custom_field2: Optional[str]
    custom_field3: Optional[str]
    custom_field4: Optional[str]
    custom_field5: Optional[str]
    custom_field6: Optional[str]
    custom_field7: Optional[str]
    custom_field8: Optional[str]
    custom_field9: Optional[str]
    custom_field10: Optional[str]


class BaseEvent(BaseModel):
    from_: Optional[str] = Field(..., alias="from")
    event_: Optional[str] = Field(..., alias="event")
    data_: EventData = Field(..., alias="data")

class EventLock(BaseModel):
    from_: Optional[str]
    event_: Optional[str] 
    data_: EventData

class Event(BaseEvent):
    pass