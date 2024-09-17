from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union
from app.modules.branch import branch_dictionary


class Branch(BaseModel):
    id: int = Field(..., alias="cooperator_id")
    name: str
    address: str
    info: str
    has_double_passcode: Union[List[str], bool, None]
    recovery_passcode: Optional[str] = None

    @classmethod
    def from_dict(cls, cooperator_id: int) -> 'Branch':
        branch_info = branch_dictionary.get(cooperator_id)
        if not branch_info:
            raise ValueError(f"No branch found for cooperator_id: {cooperator_id}")
        
        return cls(
            cooperator_id=cooperator_id,
            name=branch_info.get('name', ''),
            address=branch_info.get('address', ''),
            info=branch_info.get('info', ''),
            has_double_passcode=branch_info.get('has_double_passcode', False),
            recovery_passcode=branch_info.get('recovery passcode', None)
        )

    class Config:
        populate_by_name = True