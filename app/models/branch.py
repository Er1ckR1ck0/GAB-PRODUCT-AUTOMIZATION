from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from app.modules.branch_modules import branch_dictionary

class Branch(BaseModel):
    id: int = Field(..., alias="cooperator_id")
    name: str
    address: str
    info: str
    has_double_passcode: List[str] | Optional[bool]
    recovery_passcode: str

    @classmethod
    def from_dict(cls, cooperator_id: int) -> 'Branch':
        return cls(
            cooperator_id=cooperator_id,
            name=branch_dictionary[cooperator_id]['name'],
            address=branch_dictionary[cooperator_id]['address'],
            info=branch_dictionary[cooperator_id]['info'],
            has_double_passcode=branch_dictionary[cooperator_id]['has_double_passcode'],
            recovery_passcode=branch_dictionary[cooperator_id]['recovery passcode']
        )

    class Config:
        allow_population_by_field_name = True