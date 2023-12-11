import asyncio
import datetime
import jwt
from fastapi import FastAPI, Header, Query
from sqlalchemy import text
from trycourier import Courier
from werkzeug.security import generate_password_hash, check_password_hash
from controllers.connect_db import SessionLocal, engine
from controllers.requests import success_response, error_response, unauthorized_response
from models.contacts_model import ContactList, userData, userLogin
from models.response import Res
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

SECRET_KEY = "javainuse-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

client = Courier(auth_token="pk_prod_J06Z6Y462V4ZD5Q382ST5EEGMVSF")

url: str = '542393991440-vna922ps3roohtu0rm1bkutduu8li9hr.apps.googleusercontent.com'
key: str = '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'


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


def verifyToken(token, secret_key):
    token = token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        if payload.get("exp") < datetime.datetime.utcnow().timestamp():
            return unauthorized_response("Token is expired")
        return payload
    except jwt.ExpiredSignatureError:
        return unauthorized_response("Token is expired")
    except jwt.InvalidTokenError:
        return unauthorized_response("Token is invalid")
    except Exception as e:
        return unauthorized_response(str(e))


def verifyUserToken(token: str = Header(None)):
    if not token:
        return unauthorized_response("Token is required")

    verifyToken(token, SECRET_KEY)
    return None


def generateToken(payload, secret_key, expiration_minutes=30):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    token = jwt.encode({
        "exp": expiration_time,
        **payload},
        secret_key,
        algorithm="HS256"
    )
    return token


def PasswordHash(password):
    return generate_password_hash(password)


def PasswordCheck(provided_password, hashed_password):
    return check_password_hash(hashed_password, provided_password)


@app.post("/user", response_model=Res)
async def add_user(user: userData):
    connection = engine.connect()
    sql = text('SELECT * FROM users WHERE email = :email OR phone = :phone')
    result = connection.execute(sql, email=user.email, phone=user.phone)
    user.updated_at = datetime.datetime.now()
    user.token = generateToken({"email": user.email, "phone": user.phone}, SECRET_KEY)
    if result.rowcount > 0:
        sql = text('UPDATE users SET updated_at = :updated_at, token = :token WHERE email = :email OR phone = :phone')
        connection.execute(sql, updated_at=user.updated_at, token=user.token, email=user.email, phone=user.phone)
        connection.close()
        return success_response(user.token)
    else:
        user.blocked = False
        user.password = PasswordHash(user.password)
        user.created_at = user.updated_at
        # user not exists
        sql = text(
            'INSERT INTO users (access_token, id_token, ids, phone, email, password, name, photo_url, blocked, role, region, device, created_at, updated_at, token) VALUES (:access_token, :id_token, :ids, :phone, :email, :password, :name, :photo_url, :blocked, :role, :region, :device, :created_at, :updated_at, :token)')
        connection.execute(sql, access_token=user.access_token, id_token=user.id_token, ids=user.ids, phone=user.phone,
                           email=user.email, password=user.password, name=user.name, photo_url=user.photo_url,
                           blocked=user.blocked, role=user.role, region=user.region, device=user.device,
                           created_at=user.created_at, updated_at=user.updated_at, token=user.token)
        connection.close()
        return success_response(user.token)


@app.post("/user/login", response_model=Res)
async def login_user(login: userLogin):
    if not login.email:
        return error_response("Email is required")
    if not login.password:
        return error_response("Password is required")
    try:
        connection = engine.connect()
        sql = text('SELECT * FROM users WHERE email = :email')
        result = connection.execute(sql, email=login.email)
        if result.rowcount > 0:
            user = dict(result.fetchone())
            if PasswordCheck(login.password, user['password']):
                user['token'] = generateToken({"email": user['email'], "phone": user['phone']}, SECRET_KEY)
                sql = text('UPDATE users SET token = :token WHERE email = :email')
                connection.execute(sql, token=user['token'], email=user['email'])
                connection.close()
                return success_response(user['token'])
            else:
                connection.close()
                return error_response("Invalid password")
        else:
            connection.close()
            return error_response("User not found")
    except Exception as e:
        return error_response(str(e))


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
    sql = text('DELETE FROM users')
    connection.execute(sql)
    connection.close()
    # return element size
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


# @app.get("contacts/{search}")
# async def searchContacts(Authorization: str = Header(None), search: str = Query(None)):
#     token = verifyUserToken(Authorization)
#     if token:
#         return token
#     try:
#         session = SessionLocal()
#         query = text(
#             "SELECT * FROM contacts WHERE display_name LIKE :search OR given_name LIKE :search OR middle_name LIKE :search OR prefix LIKE :search OR suffix LIKE :search OR family_name LIKE :search OR company LIKE :search OR job_title LIKE :search OR emails LIKE :search OR phones LIKE :search OR postal_addresses LIKE :search")
#         result = session.execute(query, {"search": f'%{search}%'})
#         contacts = [dict(row) for row in result]
#         return {"contacts": contacts, "size": len(contacts)}
#     except Exception as e:
#         return error_response(str(e))


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
