from typing import Union

from pydantic import BaseModel
from models.contacts_model import ContactList, userData


class Res(BaseModel):
    status: str = None
    message: str = None
    data: Union[ContactList, userData, str, int, float, bool, None] = None
