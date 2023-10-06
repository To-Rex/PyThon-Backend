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


class userData(BaseModel):
    access_token: str
    id_token: str
    ids: str
    phone: str
    email: str
    password: str
    name: str
    photo_url: str
    blocked: str
    role: str
    region: str
    device: str
    created_at: str
    updated_at: str
    token: str


class userLogin(BaseModel):
    email: str
    password: str
