from pydantic import BaseModel


class NewLink(BaseModel):
    client_name: str
    is_premium: str
    original_link: str
    