import asyncio
from fastapi import FastAPI, Depends, status, Response
from sqlalchemy import text
from controllers.connect_db import SessionLocal, engine
from models.contacts_model import ContactList
from models.response import Res
from controllers.requests import success_response, error_response, not_found_response, bad_request_response, \
    forbidden_response, internal_server_error_response

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


@app.post("/contacts", response_model=Res)
async def get_contacts(contact: ContactList):
    if not contact.contacts:
        return error_response("No contacts provided")
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: insert_contacts(contact.contacts))
        if result:
            return success_response(contact)
        else:
            return error_response("Request processed failed")
    except Exception as e:
        return error_response(str(e))


def insert_contacts(contacts):
    try:
        session = SessionLocal()
        insert_query = text(
            'INSERT INTO contacts (display_name, given_name, middle_name, prefix, suffix, family_name, company, job_title, emails, phones, postal_addresses, avatar, birthday, android_account_type, android_account_type_raw, android_account_name) VALUES (:display_name, :given_name, :middle_name, :prefix, :suffix, :family_name, :company, :job_title, :emails, :phones, :postal_addresses, :avatar, :birthday, :android_account_type, :android_account_type_raw, :android_account_name)')
        # insert_query = text('INSERT INTO contacts (display_name, given_name, middle_name, prefix, suffix, family_name, company, job_title, emails, phones, postal_addresses, birthday, android_account_type, android_account_type_raw, android_account_name) SELECT :display_name, :given_name, :middle_name, :prefix, :suffix, :family_name, :company, :job_title, :emails, :phones, :postal_addresses, :birthday, :android_account_type, :android_account_type_raw, :android_account_name WHERE NOT EXISTS (SELECT display_name, phones FROM contacts WHERE display_name = :display_name AND phones = :phones)')
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
                "avatar": item.avatar,
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


@app.get("/contacts")
async def get_all_contacts():
    try:
        session = SessionLocal()
        query = text("SELECT * FROM contacts")
        result = session.execute(query)
        contacts = [dict(row) for row in result]
        return {"contacts": contacts}, {"size": len(contacts)}
    except Exception as e:
        return error_response(str(e))


@app.get("/clear")
async def clear_db():
    connection = engine.connect()
    sql = text('DELETE FROM contacts')
    size = connection.execute(sql)
    connection.execute(sql)
    sql = text('DELETE FROM users')
    connection.execute(sql)
    connection.close()
    # return element size
    return success_response(size.rowcount + " rows deleted")


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
