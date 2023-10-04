from http.client import HTTPException
from typing import List
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from controllers.connect_db import SessionLocal, engine
from models.contacts_model import ContactList, Contact
from controllers import connect_db
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

@app.post("/contacts", response_model=ContactList)
async def get_contacts(contact: ContactList):
    try:
        connection = engine.connect()
        # save data contacts to database
        for item in contact.contacts:
            sql = text(
                'INSERT INTO contacts (display_name, given_name, middle_name, prefix, suffix, family_name, company, job_title, emails, phones, postal_addresses, birthday, android_account_type, android_account_type_raw, android_account_name) VALUES (:display_name, :given_name, :middle_name, :prefix, :suffix, :family_name, :company, :job_title, :emails, :phones, :postal_addresses, :birthday, :android_account_type, :android_account_type_raw, :android_account_name)')
            connection.execute(sql, display_name=item.display_name, given_name=item.given_name,
                               middle_name=item.middle_name, prefix=item.prefix, suffix=item.suffix,
                               family_name=item.family_name, company=item.company, job_title=item.job_title,
                               emails=item.emails, phones=item.phones, postal_addresses=item.postal_addresses,
                               birthday=item.birthday, android_account_type=item.android_account_type,
                               android_account_type_raw=item.android_account_type_raw,
                               android_account_name=item.android_account_name)
        connection.close()
        return contact
    except OperationalError as e:
        print(e)
        return {"message": "Error"}
    except HTTPException as e:
        print(e)
        return {"message": "Error"}
    except Exception as e:
        print(e)
        return {"message": "Error"}


# get data from database
@app.get("/contacts", response_model=ContactList)
async def get_contacts():
    connection = engine.connect()
    sql = text('SELECT * FROM contacts')
    result = connection.execute(sql)
    existing_contacts = set()  # To store existing contact display names

    contacts = []
    # for row in result:
    #     display_name = row[1]
    #     # Check if the contact's display name is not already in the set of existing contacts
    #     if display_name in existing_contacts:
    #         contacts.append(
    #             Contact(
    #                 display_name=row[1],
    #                 given_name=row[2],
    #                 middle_name=row[3],
    #                 prefix=row[4],
    #                 suffix=row[5],
    #                 family_name=row[6],
    #                 company=row[7],
    #                 job_title=row[8],
    #                 emails=row[9].split(';'),
    #                 phones=row[10].split(';'),
    #                 postal_addresses=row[11].split(';'),
    #                 birthday=row[12],
    #                 android_account_type=row[13],
    #                 android_account_type_raw=row[14],
    #                 android_account_name=row[15]
    #             )
    #         )
    #         existing_contacts.add(display_name)
    insert_statement = text(
        'INSERT INTO contacts (display_name, given_name, middle_name, prefix, suffix, family_name, company, job_title, emails, phones, postal_addresses, birthday, android_account_type, android_account_type_raw, android_account_name) VALUES (:display_name, :given_name, :middle_name, :prefix, :suffix, :family_name, :company, :job_title, :emails, :phones, :postal_addresses, :birthday, :android_account_type, :android_account_type_raw, :android_account_name)'
    )
    connection.execute(insert_statement, contacts)
    connection.close()
    #number of contacts
    return {"message": len(contacts)}


@app.post("/users")
async def create_user():
    connection = engine.connect() #connect db and get data if users table is exist in database
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
    #clear data in users table
    sql = text('DELETE FROM users')
    size = connection.execute(sql)
    connection.execute(sql)

    connection.close()
    # return element size
    return {"message": size}



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
