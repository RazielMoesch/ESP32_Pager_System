


from fastapi import FastAPI, Depends
from pydantic import BaseModel
import bcrypt
import secrets
from database import *
import sqlite3
from typing import Optional

DATABASE_URL = "app.db"

SEED_USERNAME = ""
SEED_PASSWORD = ""
SEED_AUTHKEY = ""
PAGER_BATCH_KEY = ""

app = FastAPI()


def verify_teacher_authkey(conn: sqlite3.Connection, username: str, authkey: str):
    realkey = get_teacher_authkey(conn, username)
    return secrets.compare_digest(authkey, realkey) if realkey else False


def verify_pager_authkey(conn: sqlite3.Connection, pagerid: str, authkey: str):
    realkey = get_pager_authkey(conn, pagerid)
    return secrets.compare_digest(authkey, realkey) if realkey else False


def get_db():
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


setup_conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
init_db(setup_conn)
add_teacher(setup_conn, SEED_USERNAME, bcrypt.hashpw(SEED_PASSWORD.encode("utf-8"), bcrypt.gensalt()), SEED_AUTHKEY)
setup_conn.close()


@app.get("/health")
def health_endpoint():
    return "Healthy"

class LoginModel(BaseModel):
    username: str
    password: str

@app.post("/login")
def login_endpoint(data: LoginModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        byte_pass = data.password.encode()
        hashpass = get_teacher_pw(conn, username)
        if hashpass is None:
            return {"status": "failure", "message": "Could Not Find Username. Please make sure you have an account."}
        result = bcrypt.checkpw(byte_pass, hashpass)
        if result:
            authkey = get_teacher_authkey(conn, username)
            return {"status": "success", "authkey": authkey}
        return {"status": "failure", "message": "Incorrect Password"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class AddTeacherModel(BaseModel):
    username: str
    authkey: str
    newusername: str
    newpw: str

@app.post("/add_teacher")
def add_teacher_endpoint(data: AddTeacherModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        new_authkey = secrets.token_urlsafe(32)
        hashedpw = bcrypt.hashpw(data.newpw.encode("utf-8"), bcrypt.gensalt())
        add_teacher(conn, data.newusername, hashedpw, new_authkey)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class RemoveTeacherModel(BaseModel):
    username: str
    authkey: str
    targetusername: str

@app.post("/remove_teacher")
def remove_teacher_endpoint(data: RemoveTeacherModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        remove_teacher(conn, data.targetusername)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class AddPagerModel(BaseModel):
    username: str
    authkey: str
    studentfirst: str
    studentlast: str
    pagerid: str
    grade: int

@app.post("/add_pager")
def add_pager_endpoint(data: AddPagerModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        new_authkey = secrets.token_urlsafe(32)
        add_pager(conn, data.studentfirst, data.studentlast, data.pagerid, data.grade, new_authkey)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class RemovePagerModel(BaseModel):
    username: str
    authkey: str
    pagerid: str

@app.post("/remove_pager")
def remove_pager_endpoint(data: RemovePagerModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        remove_pager(conn, data.pagerid)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class GetPagersModel(BaseModel):
    username: str
    authkey: str

@app.post("/get_pagers")
def get_pagers_endpoint(data: GetPagersModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        pagers = get_pagers(conn)
        return {"status": "success", "pagers": pagers}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class AddMessageModel(BaseModel):
    username: str
    authkey: str
    msgtype: str
    content: str
    pagerid: Optional[str] = None
    grade: Optional[int] = None

@app.post("/add_message")
def add_message_endpoint(data: AddMessageModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        add_message(conn, username, data.msgtype, data.content, data.pagerid, data.grade)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class RemoveMessageModel(BaseModel):
    username: str
    authkey: str
    msgid: int

@app.post("/remove_message")
def remove_message_endpoint(data: RemoveMessageModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        remove_message(conn, data.msgid)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class TeacherGetMessagesModel(BaseModel):
    username: str
    authkey: str
    pagerid: Optional[str] = None
    grade: Optional[int] = None

@app.post("/teacher/get_messages")
def teacher_get_messages_endpoint(data: TeacherGetMessagesModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        msgs = get_messages(conn, data.pagerid, data.grade)
        return {"status": "success", "messages": msgs}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class PagerGetMessagesModel(BaseModel):
    authkey: str
    pagerid: str
    grade: int

@app.post("/pager/get_messages")
def pager_get_messages_endpoint(data: PagerGetMessagesModel, conn=Depends(get_db)):
    try:
        if not verify_pager_authkey(conn, data.pagerid, data.authkey):
            return {"status": "failure", "message": "Authentication Key and PagerID Do Not Match."}
        msgs = get_messages(conn, data.pagerid, data.grade)
        return {"status": "success", "messages": msgs}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class PagerRequestSetupModel(BaseModel):
    pagerid: str
    tempkey: str

@app.post("/pager/request_setup")
def request_setup_endpoint(data: PagerRequestSetupModel, conn=Depends(get_db)):
    try:
        if not secrets.compare_digest(data.tempkey, PAGER_BATCH_KEY):
            return {"status": "failure"}
        add_setup_request(conn, data.pagerid)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class TeacherRemoveSetupRequestModel(BaseModel):
    username: str
    authkey: str
    pagerid: str

@app.post("/teacher/remove_setup_request")
def remove_setup_request_endpoint(data: TeacherRemoveSetupRequestModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        remove_setup_request(conn, data.pagerid)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class GetSetupRequestsModel(BaseModel):
    username: str
    authkey: str

@app.post("/get_setup_requests")
def get_setup_requests_endpoint(data: GetSetupRequestsModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        result = get_setup_requests(conn)
        return {"status": "success", "setuprequests": result}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class TeacherSetupPagerModel(BaseModel):
    username: str
    authkey: str
    pagerid: str
    first: str
    last: str
    grade: int

@app.post("/teacher/setup_pager")
def setup_pager_endpoint(data: TeacherSetupPagerModel, conn=Depends(get_db)):
    try:
        username = data.username.lower()
        if not verify_teacher_authkey(conn, username, data.authkey):
            return {"status": "failure", "message": "Authentication Key and Account Do Not Match."}
        new_authkey = secrets.token_urlsafe(32)
        add_new_pager_info(conn, data.pagerid, new_authkey, data.first, data.last, data.grade)
        remove_setup_request(conn, data.pagerid)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class PagerFinishSetupModel(BaseModel):
    pagerid: str
    tempkey: str

@app.post("/pager/finish_setup")
def finish_pager_setup_endpoint(data: PagerFinishSetupModel, conn=Depends(get_db)):
    try:
        if not secrets.compare_digest(data.tempkey, PAGER_BATCH_KEY):
            return {"status": "failure"}
        info = get_new_pager_info(conn, data.pagerid)
        if info is None:
            return {"status": "failure", "message": "No pending setup for this pagerID. Has a teacher approved it?"}
        add_pager_replace(conn, info[0], info[1], data.pagerid, info[4], info[2])
        remove_new_pager_info(conn, data.pagerid)
        return {
            "status": "success",
            "first": info[0],
            "last": info[1],
            "authkey": info[2],
            "pagerid": info[3],
            "grade": info[4]
        }
    except Exception as e:
        return {"status": "failure", "message": str(e)}