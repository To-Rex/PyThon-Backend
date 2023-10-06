import asyncio
from http.client import HTTPException
from typing import List
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from controllers.connect_db import SessionLocal, engine
from models.contacts_model import ContactList, Contact
from controllers import connect_db
from models.response import Response
from models.test import Userr

app = FastAPI()

# {
#     "contacts": [
#         {
#             "display_name": "John Doesss",
#             "given_name": "Johnas",
#             "middle_name": "Michaesasl",
#             "prefix": "Mdr.",
#             "suffix": "Jdr.",
#             "family_name": "Ddaoe",
#             "company": "ABC SCorp",
#             "job_title": "Software Engineerrr",
#             "emails": "john.doe@example.com",
#             "phones": "121-456-121",
#             "postal_addresses": "123 Main St, City, State, Country",
#             //"avatar": "base64-encoded-avatar-data",
#             "birthday": "1911-01-03",
#             "android_account_type": "com.example.account_type",
#             "android_account_type_raw": "Raw Account Type",
#             "android_account_name": "JohnDoeAccount"
#         },
#         {
#             "display_name": "Ali John Doeaww",
#             "given_name": "Johna",
#             "middle_name": "Michaele",
#             "prefix": "Mr.",
#             "suffix": "Jr.",
#             "family_name": "Doe",
#             "company": "ABC Corp",
#             "job_title": "Software Engineer",
#             "emails": "john.doe@example.com",
#             "phones": "123-456-7009",
#             "postal_addresses": "123 Main St, City, State, Country",
#             //"avatar": "base64-encoded-avatar-data",
#             "birthday": "1990-01-01",
#             "android_account_type": "com.example.account_type",
#             "android_account_type_raw": "Raw Account Type",
#             "android_account_name": "JohnDoeAccount"
#         },
#         {
#             "display_name": "Var John Doe",
#             "given_name": "asas John",
#             "middle_name": "Michael",
#             "prefix": "Mr.",
#             "suffix": "Jr.",
#             "family_name": "Doe",
#             "company": "ABC Corp",
#             "job_title": "Software Engineer",
#             "emails": "john.doe@example.com",
#             "phones": "123-456-7111",
#             "postal_addresses": "123 Main St, City, State, Country",
#             //"avatar": "base64-encoded-avatar-data",
#             "birthday": "1990-01-01",
#             "android_account_type": "com.example.account_type",
#             "android_account_type_raw": "Raw Account Type",
#             "android_account_name": "JohnDoeAccount"
#         }
#     ]
# }

# save to database

engine = connect_db.engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.post("/contacts")
async def get_contacts(contact: ContactList):
    if not contact:
        return Response(
            status="error",
            message="Request processed failed",
            data=contact,
        )
    if not contact.contacts:
        return Response(
            status="error",
            message="Request processed failed",
            data=contact,
        )

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: insert_contacts(contact.contacts))

        return Response(
            status="success",
            message="Request processed successfully",
            data=contact,
        )
        #return 200 ok

    except Exception as e:
        print(e)
        # return Response(
        #     status="error",
        #     message="Request processed failed",
        #     data=contact,
        # )
        raise HTTPException(status_code=400, detail=Response(
            status="error",
            message="Request processed failed",
            data=contact,
        ))



def insert_contacts(contacts):
    try:
        session = SessionLocal()
        insert_query = text(
            'INSERT INTO contacts (display_name, given_name, middle_name, prefix, suffix, family_name, company, job_title, emails, phones, postal_addresses, birthday, android_account_type, android_account_type_raw, android_account_name) VALUES (:display_name, :given_name, :middle_name, :prefix, :suffix, :family_name, :company, :job_title, :emails, :phones, :postal_addresses, :birthday, :android_account_type, :android_account_type_raw, :android_account_name)'
        )
        insert_data = [
            {
                "display_name": item.display_name,
                "given_name": item.given_name,
                "middle_name": item.middle_name,
                "prefix": item.prefix,
                "suffix": item.suffix,
                "family_name": item.family_name,
                "company": item.company,
                "job_title": item.job_title,
                "emails": item.emails,
                "phones": item.phones,
                "postal_addresses": item.postal_addresses,
                "birthday": item.birthday,
                "android_account_type": item.android_account_type,
                "android_account_type_raw": item.android_account_type_raw,
                "android_account_name": item.android_account_name,
            }
            for item in contacts
        ]
        session.execute(insert_query, insert_data)
        session.commit()

        return True
    except Exception as e:
        print(e)
        return False


@app.get("/contacts", response_model=Response)
async def get_contacts():
    connection = engine.connect()
    connection.close()
    #return connection.execute('SELECT COUNT(*) FROM contacts').scalar()
    return Response(
        status="success",
        message="Request processed successfully",
        data=connection.execute('SELECT COUNT(*) FROM contacts').scalar(),
    )


@app.post("/users")
async def create_user():
    connection = engine.connect()  # connect db and get data if users table is exist in database
    users_data = [
        {"username": "user1", "email": "user1@example.com"},
        {"username": "user2", "email": "user2@example.com"},
        {"username": "user3", "email": "user3@example.com"},
        {"username": "user4", "email": "user4@example.com"},
        {"username": "user5", "email": "user5@example.com"},
        {"username": "user6", "email": "user6@example.com"},
        {"username": "user7", "email": "user7@example.com"},
        {"username": "user8", "email": "user8@example.com"},
        {"username": "user9", "email": "user9@example.com"},
        {"username": "user10", "email": "user10@example.com"},
    ]

    insert_statement = text(
        'INSERT INTO users (username, email) VALUES (:username, :email)'
    )
    connection.execute(insert_statement, users_data)

    connection.close()
    return {"message": "Success"}


@app.get("/")
async def root():
    # connect db and get data if users table is exist in database
    return {"message": "Hello World"}


@app.get("/clear")
async def clear_db():
    connection = engine.connect()
    sql = text('DELETE FROM contacts')
    size = connection.execute(sql)
    connection.execute(sql)
    # clear data in users table
    sql = text('DELETE FROM users')
    size = connection.execute(sql)
    connection.execute(sql)

    connection.close()
    # return element size
    return {"message": size}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
