from pydantic import BaseModel
from typing import List


class Contact(BaseModel):
    display_name: str
    given_name: str
    middle_name: str
    prefix: str
    suffix: str
    family_name: str
    company: str
    job_title: str
    emails: str
    phones: str
    postal_addresses: str
    avatar: str
    birthday: str
    android_account_type: str
    android_account_type_raw: str
    android_account_name: str


class ContactList(BaseModel):
    contacts: List[Contact]
