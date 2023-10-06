from pydantic import BaseModel
from typing import List


class Contact(BaseModel):
    display_name: str = None
    given_name: str = None
    middle_name: str = None
    prefix: str = None
    suffix: str = None
    family_name: str = None
    company: str = None
    job_title: str = None
    emails: str = None
    phones: str = None
    postal_addresses: str = None
    avatar: str = None
    birthday: str = None
    android_account_type: str = None
    android_account_type_raw: str = None
    android_account_name: str = None


class ContactList(BaseModel):
    contacts: List[Contact] = None


class userData(BaseModel):
    access_token: str = None
    id_token: str = None
    ids: str = None
    phone: str = None
    email: str = None
    password: str = None
    name: str = None
    photo_url: str = None
    blocked: str = None
    role: str = None
    region: str = None
    device: str = None
    created_at: str = None
    updated_at: str = None
    token: str = None


class userLogin(BaseModel):
    email: str = None
    password: str = None
