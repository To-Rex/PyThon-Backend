from sqlalchemy import Column, String, Integer

from controllers.connect_db import Base


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String, index=True)
    given_name = Column(String)
    middle_name = Column(String)
    prefix = Column(String)
    suffix = Column(String)
    family_name = Column(String)
    company = Column(String)
    job_title = Column(String)
    emails = Column(String)
    phones = Column(String)
    postal_addresses = Column(String)
    avatar = Column(String)
    birthday = Column(String)
    android_account_type = Column(String)
    android_account_type_raw = Column(String)
    android_account_name = Column(String)


#chat models



