from typing import Any, Optional, List
from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: bool = True
    data: Optional[Any] = None
    errors: Optional[List[dict]] = None
