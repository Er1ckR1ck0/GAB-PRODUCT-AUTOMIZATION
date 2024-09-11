from pydantic import BaseModel, Field
from typing import Optional

class Data(BaseModel):
    id: int
    whom: int
    created_at: str
    updated_at: str
    record: str
    name: str
    price: str
    phone: str
    email: str
    comment: Optional[str]
    status: int
    status_title: str
    cooperator_id: int
    cooperator_title: str
    branch_id: int
    branch_title: str
    service_id: int
    service_title: str
    url: Optional[str]
    coupon: Optional[str]
    coupon_discount: Optional[str]
    source: Optional[str]
    cancelReason: Optional[str]
    duration: Optional[str]
    prepayment: str
    prepayment_date: str
    prepayment_url: str
    reminder: str
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

class Event(BaseModel):
    FROM: str = Field(alias="from")
    EVENT: str = Field(alias="event")
    DATA: Data = Field(alias="data")
