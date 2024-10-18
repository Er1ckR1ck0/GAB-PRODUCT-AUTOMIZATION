from pydantic import BaseModel, Field
from typing import Optional

class EventData(BaseModel):
    id: Optional[int] | Optional[int]
    whom: Optional[int] | Optional[int]
    created_at: Optional[str] | Optional[int]
    updated_at: Optional[str] | Optional[int]
    record: Optional[str] | Optional[int]
    name: Optional[str] | Optional[int]
    price: Optional[str] | Optional[int]
    phone: Optional[str] | Optional[int]
    email: Optional[str] | Optional[int]
    comment: Optional[str] | Optional[int]
    status: Optional[int] | Optional[int]
    status_title: Optional[str] | Optional[int]
    cooperator_id: Optional[int] | Optional[int]
    cooperator_title: Optional[str] | Optional[int]
    branch_id: Optional[int] | Optional[int]
    branch_title: Optional[str] | Optional[int]
    service_id: Optional[int] | Optional[int]
    service_title: Optional[str] | Optional[int]
    url: Optional[str] | Optional[int]
    coupon: Optional[str] | Optional[int]
    coupon_discount: Optional[str] | Optional[int]
    source: Optional[str] | Optional[int]
    cancelReason: Optional[str] | Optional[int]
    duration: Optional[str] | Optional[int]
    prepayment: Optional[str] | Optional[int]
    prepayment_date: Optional[str] | Optional[int]
    prepayment_url: Optional[str] | Optional[int]
    reminder: Optional[str] | Optional[int]
    custom_field1: Optional[str] | Optional[int]
    custom_field2: Optional[str] | Optional[int]
    custom_field3: Optional[str] | Optional[int]
    custom_field4: Optional[str] | Optional[int]
    custom_field5: Optional[str] | Optional[int]
    custom_field6: Optional[str] | Optional[int]
    custom_field7: Optional[str] | Optional[int]
    custom_field8: Optional[str] | Optional[int]
    custom_field9: Optional[str] | Optional[int]
    custom_field10: Optional[str] | Optional[int]


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