from typing import Union

from pydantic import BaseModel
from models.contacts_model import ContactList


class Res(BaseModel):
    status: str
    message: str
    data: Union[ContactList, str, int, float, bool, None]
