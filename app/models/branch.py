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
        branch_info = branch_dictionary[cooperator_id]
        if not branch_info:
            raise ValueError(f"No branch found for cooperator_id: {cooperator_id}")
        
        return cls(
            cooperator_id=cooperator_id,
            name=branch_info['name'],
            address=branch_info['address'],
            info=branch_info['info'],
            has_double_passcode=branch_info['has_double_passcode'],
            recovery_passcode=branch_info['recovery passcode']
        )

    class Config:
        populate_by_name = True