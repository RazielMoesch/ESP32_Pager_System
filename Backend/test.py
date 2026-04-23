import requests


USERNAME = ""
PW = ""
URL = ""
TEMPKEY = ""


def test_login():
    result = requests.post(f"{URL}/login", json={
        "username": USERNAME,
        "password": PW
    })
    print(f"Attempting Login ({USERNAME}): {result.text}")
    return result.json()["authkey"]


def test_add_teacher(authkey, new_username, new_pw):
    result = requests.post(f"{URL}/add_teacher", json={
        "username": USERNAME,
        "authkey": authkey,
        "newusername": new_username,
        "newpw": new_pw
    })
    print(f"Attempting Add Teacher ({new_username}): {result.text}")


def test_remove_teacher(authkey, target_username):
    result = requests.post(f"{URL}/remove_teacher", json={
        "username": USERNAME,
        "authkey": authkey,
        "targetusername": target_username
    })
    print(f"Attempting Remove Teacher ({target_username}): {result.text}")


def test_add_pager(authkey, first, last, pid, grade):
    result = requests.post(f"{URL}/add_pager", json={
        "username": USERNAME,
        "authkey": authkey,
        "studentfirst": first,
        "studentlast": last,
        "pagerid": pid,
        "grade": grade
    })
    print(f"Attempting Add Pager ({first} {last}, {pid}): {result.text}")


def test_remove_pager(authkey, pid):
    result = requests.post(f"{URL}/remove_pager", json={
        "username": USERNAME,
        "authkey": authkey,
        "pagerid": pid
    })
    print(f"Attempting Remove Pager ({pid}): {result.text}")


def test_get_pagers(authkey):
    result = requests.post(f"{URL}/get_pagers", json={
        "username": USERNAME,
        "authkey": authkey
    })
    print(f"Attempting Get Pagers: {result.text}")


def test_add_message(authkey, msgtype, content, pagerid=None, grade=None):
    if pagerid:
        result = requests.post(f"{URL}/add_message", json={
            "username": USERNAME,
            "authkey": authkey,
            "msgtype": msgtype,
            "content": content,
            "pagerid": pagerid
        })
        print(f"Attempting Add Message (to pager: {pagerid}): {result.text}")
    elif grade is not None:
        result = requests.post(f"{URL}/add_message", json={
            "username": USERNAME,
            "authkey": authkey,
            "msgtype": msgtype,
            "content": content,
            "grade": grade
        })
        print(f"Attempting Add Message (to grade: {grade}): {result.text}")
    else:
        result = requests.post(f"{URL}/add_message", json={
            "username": USERNAME,
            "authkey": authkey,
            "msgtype": msgtype,
            "content": content
        })
        print(f"Attempting Add Message (to ALL): {result.text}")


def test_remove_message(authkey, msgid):
    result = requests.post(f"{URL}/remove_message", json={
        "username": USERNAME,
        "authkey": authkey,
        "msgid": msgid
    })
    print(f"Attempting to Remove Message ({msgid}): {result.text}")


def test_teacher_get_messages(authkey, pagerid=None, grade=None):
    body = {"username": USERNAME, "authkey": authkey}
    if pagerid is not None:
        body["pagerid"] = pagerid
    if grade is not None:
        body["grade"] = grade

    result = requests.post(f"{URL}/teacher/get_messages", json=body)
    print(f"Attempting Teacher Get Messages (pagerid={pagerid}, grade={grade}): {result.text}")


def test_pager_get_messages(pagerid, authkey, grade):
    result = requests.post(f"{URL}/pager/get_messages", json={
        "pagerid": pagerid,
        "authkey": authkey,
        "grade": grade
    })
    print(f"Attempting Pager Get Messages ({pagerid}): {result.text}")


def test_pager_request_setup(pagerid, tempkey):
    result = requests.post(f"{URL}/pager/request_setup", json={
        "pagerid": pagerid,
        "tempkey": tempkey
    })
    print(f"Attempting to Request Setup ({pagerid}): {result.text}")


def test_teacher_remove_setup_request(authkey, pagerid):
    result = requests.post(f"{URL}/teacher/remove_setup_request", json={
        "username": USERNAME,
        "authkey": authkey,
        "pagerid": pagerid
    })
    print(f"Attempting Teacher Remove Setup Request ({pagerid}): {result.text}")


def test_get_setup_requests(authkey):
    result = requests.post(f"{URL}/get_setup_requests", json={
        "username": USERNAME,
        "authkey": authkey
    })
    print(f"Attempting Get Setup Requests: {result.text}")


def test_teacher_setup_pager(authkey, pagerid, first, last, grade):
    result = requests.post(f"{URL}/teacher/setup_pager", json={
        "username": USERNAME,
        "authkey": authkey,
        "pagerid": pagerid,
        "first": first,
        "last": last,
        "grade": grade
    })
    print(f"Attempting to Setup Pager ({pagerid}): {result.text}")


def test_pager_finish_setup(pagerid, tempkey):
    result = requests.post(f"{URL}/pager/finish_setup", json={
        "pagerid": pagerid,
        "tempkey": tempkey
    })
    print(f"Attempting to Finish Pager Setup ({pagerid}): {result.text}")
    return result.json()


if __name__ == "__main__":

    authkey = test_login()

    print("\n--- Teacher Management ---")
    test_add_teacher(authkey, "sstein", "789")
    test_remove_teacher(authkey, "sstein")

    print("\n--- Pager Management ---")
    test_add_pager(authkey, "Matanel", "Sher", "RKYHSPager4", 12)
    test_get_pagers(authkey)

    print("\n--- Messaging ---")
    test_add_message(authkey, "individual", "Direct message to Matanel.", pagerid="RKYHSPager4")
    test_add_message(authkey, "grade", "Hello grade 12.", grade=12)
    test_add_message(authkey, "all", "Hello everyone.")
    test_teacher_get_messages(authkey)
    test_teacher_get_messages(authkey, pagerid="RKYHSPager4")
    test_teacher_get_messages(authkey, grade=12)
    test_teacher_get_messages(authkey, pagerid="RKYHSPager4", grade=12)
    test_remove_message(authkey, 1)

    print("\n--- Pager Setup Flow ---")
    test_pager_request_setup("RKYHSPager21", TEMPKEY)
    test_get_setup_requests(authkey)
    test_teacher_setup_pager(authkey, "RKYHSPager21", "Eitan", "Kestler", 12)
    pager_info = test_pager_finish_setup("RKYHSPager21", TEMPKEY)
    print(f"Pager info returned: {pager_info}")

    print("\n--- Pager Get Messages ---")
    if pager_info.get("status") == "success":
        test_pager_get_messages(pager_info["pagerid"], pager_info["authkey"], pager_info["grade"])

    print("\n--- Cleanup ---")
    test_teacher_remove_setup_request(authkey, "RKYHSPager67")
    test_remove_pager(authkey, "RKYHSPager4")