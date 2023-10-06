from typing import Union

from pydantic import BaseModel
from models.contacts_model import ContactList
from models.test import Contacts


# {
#     "status": "success",
#     "message": "Request processed successfully",
#     "data": [
#         {"name": "John Doe", "age": 30},
#         {"name": "Jane Smith", "age": 25},
#         {"name": "Bob Johnson", "age": 35}
#     ]
# }

class Response(BaseModel):
    status: str
    message: str
    data: Union[ContactList, str, int, float, bool, None]

