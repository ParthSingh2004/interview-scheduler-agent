class IncomingEmail(BaseModel):
    sender: str
    subject: Optional[str] = ""
    body: str