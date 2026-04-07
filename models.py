from pydantic import BaseModel
from typing import Optional
class IncomingEmail(BaseModel):
    sender: str
    subject: Optional[str] = ""
    body: str
