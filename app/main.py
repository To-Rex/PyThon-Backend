import asyncio
import boto3
from fastapi import FastAPI, Header, Query, UploadFile, File
from sqlalchemy import text
from trycourier import Courier
from controllers.connect_db import SessionLocal, engine
from controllers.requests import success_response, error_response, unauthorized_response
from models.contacts_model import ContactList, userData
from models.response import Res
from starlette.middleware.sessions import SessionMiddleware
import firebase_admin
from firebase_admin import credentials, auth

from serices.services import upload_to_s3, S3_ACCESS_KEY, S3_SECRET_KEY, S3_REGION

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

client = Courier(auth_token="pk_prod_J06Z6Y462V4ZD5Q382ST5EEGMVSF")

cred = credentials.Certificate("controllers/keyFirebase.json")
firebase_admin.initialize_app(cred)


def send_email(email, title, body, data):
    resp = client.send_message(
        message={
            "to": {
                "email": email
            },
            "content": {
                "title": title,
                "body": body
            },
            "data": {
                "joke": data
            }
        }
    )

    return resp


def get_user(uid):
    user = auth.get_user(uid)
    return user


def verifyUserToken(token: str = Header(None)):
    if not token:
        return unauthorized_response("Token is required")
    try:
        if auth.get_user(token.replace("Bearer ", "")):
            return None
        else:
            return unauthorized_response("Token is invalid")
    except Exception as e:
        return unauthorized_response(str(e))


@app.post("/contacts", response_model=Res)
async def add_contacts(contact: ContactList):
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
        # insert_query = text('INSERT INTO contacts (display_name, given_name, middle_name, prefix, suffix, family_name, company, job_title, emails, phones, postal_addresses, avatar, birthday, android_account_type, android_account_type_raw, android_account_name) VALUES (:display_name, :given_name, :middle_name, :prefix, :suffix, :family_name, :company, :job_title, :emails, :phones, :postal_addresses, :avatar, :birthday, :android_account_type, :android_account_type_raw, :android_account_name)')
        insert_query = text(
            'INSERT INTO contacts (display_name, given_name, middle_name, prefix, suffix, family_name, company, job_title, emails, phones, postal_addresses, birthday, android_account_type, android_account_type_raw, android_account_name) SELECT :display_name, :given_name, :middle_name, :prefix, :suffix, :family_name, :company, :job_title, :emails, :phones, :postal_addresses, :birthday, :android_account_type, :android_account_type_raw, :android_account_name WHERE NOT EXISTS (SELECT display_name, phones FROM contacts WHERE display_name = :display_name AND phones = :phones)')
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


@app.get("/contacts", )
async def get_all_contacts(Authorization: str = Header(None)):
    token = verifyUserToken(Authorization)
    if token:
        return token
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
    connection.close()
    return success_response(size.rowcount + " rows deleted")


@app.get("/")
async def searchContacts(Authorization: str = Header(None), search: str = Query(None)):
    token = verifyUserToken(Authorization)
    if token:
        return token
    # try:
    #     session = SessionLocal()
    #     query = text(
    #         "SELECT * FROM contacts WHERE display_name LIKE :search OR given_name LIKE :search OR middle_name LIKE :search OR prefix LIKE :search OR suffix LIKE :search OR family_name LIKE :search OR company LIKE :search OR job_title LIKE :search OR emails LIKE :search OR phones LIKE :search OR postal_addresses LIKE :search")
    #     result = session.execute(query, {"search": f'%{search}%'})
    #     contacts = [dict(row) for row in result]
    #     return {"contacts": contacts, "size": len(contacts)}
    # except Exception as e:
    #     return error_response(str(e))
    # Do not care about uppercase and lowercase letters when searching
    try:
        session = SessionLocal()
        query = text(
            "SELECT * FROM contacts WHERE LOWER(display_name) LIKE :search OR LOWER(given_name) LIKE :search OR LOWER(middle_name) LIKE :search OR LOWER(prefix) LIKE :search OR LOWER(suffix) LIKE :search OR LOWER(family_name) LIKE :search OR LOWER(company) LIKE :search OR LOWER(job_title) LIKE :search OR LOWER(emails) LIKE :search OR LOWER(phones) LIKE :search OR LOWER(postal_addresses) LIKE :search")
        result = session.execute(query, {"search": f'%{search.lower()}%'})
        contacts = [dict(row) for row in result]
        return {"contacts": contacts, "size": len(contacts)}
    except Exception as e:
        return error_response(str(e))


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/getUsers")
async def get_users():
    all_users = auth.list_users()
    return all_users


@app.get("/getUsers/uid")
async def get_users_uid():
    all_users = auth.list_users()
    lit_uid = []
    for user in all_users.users:
        lit_uid.append(user.uid)
    return lit_uid


@app.get("/getUsers/{uid}")
async def get_user(uid: str):
    print(uid)
    user = auth.get_user(uid)
    return user


@app.post("/createUser")
async def create_user(user: userData):
    try:
        user = auth.create_user(
            email=user.email,
            email_verified='true',
            phone_number=user.phone,
            password=user.password,
            display_name=user.name,
            photo_url=user.photo_url,
            disabled=user.blocked,
        )
        auth.generate_email_verification_link(user.email)
        return user
    except Exception as e:
        return error_response(str(e))


S3_BUCKET_NAME = 'showcontact'
s3_client = boto3.client('s3', region_name='ap-southeast-1')



@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    print(file.filename)
    if not file.filename:
        return error_response("No file provided")
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: upload_to_s3(file.file, S3_BUCKET_NAME, file.filename,
                                                                      S3_ACCESS_KEY, S3_SECRET_KEY, S3_REGION))
        if result:
            return success_response(file.filename)
        else:
            return error_response("Request processed failed")
    except Exception as e:
        return error_response(str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    if not filename:
        return error_response("No file provided")
    try:
        s3_key = f"{filename}"  # Customize the S3 key as needed
        s3_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
        return {"message": "File uploaded successfully", "s3_url": s3_url}
    except Exception as e:
        return error_response(str(e))


