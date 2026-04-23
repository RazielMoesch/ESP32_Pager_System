

export const API_URL = "http://localhost:8000";


export const post = async (endpoint, body) => {
    const res = await fetch(`${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    if (!res.ok) throw new Error(`Request failed: ${res.status}`);

    return res.json();
};




export const sendLoginRequest = ( username, password ) => {

    return post("/api/login", { username, password });

}

export const addTeacherRequest = ( username, authkey, newusername, newpw ) => {

    return post(
        "/api/add_teacher", 
        {
            username,
            authkey,
            newusername,
            newpw
    });

}

export const removeTeacherRequest = ( username, authkey, targetusername ) => {

    return post(
        "/api/remove_teacher",
        {
            username,
            authkey,
            targetusername
        });

}

export const addPagerRequest = ( username, authkey, studentfirst, studentlast, pagerid, grade ) => {

    return post(
        "/api/add_pager",
        {
            username,
            authkey,
            studentfirst,
            studentlast,
            pagerid,
            grade
        });

}

export const removePagerRequest = ( username, authkey, pagerid ) => {

    return post(
        "/api/remove_pager",
        {
            username,
            authkey,
            pagerid
        });

}

export const getPagersRequest = ( username, authkey ) => {

    return post(
        "/api/get_pagers",
        {
            username,
            authkey
        }
    )

}

export const addMessageRequest = ( username, authkey, msgtype, content, pagerid=null, grade=null ) => {

    return post(
        "/api/add_message",
        {
            username,
            authkey,
            msgtype,
            content,
            pagerid,
            grade
        });

}

export const removeMessageRequest = ( username, authkey, msgid ) => {

    return post(
        "/api/remove_message",
        {
            username,
            authkey,
            msgid
        });

}

export const getMessagesRequest = ( username, authkey, pagerid=null, grade=null ) => {

    return post(
        "/api/get_messages",
        {
            username,
            authkey,
            pagerid,
            grade
        });

}

export const removeSetupRequestRequest = ( username, authkey, pagerid ) => {

    return post(
        "/api/remove_setup_request",
        {
            username,
            authkey,
            pagerid
        });

}

export const getSetupRequestsRequest = ( username, authkey ) => {

    return post(
        "/api/get_setup_requests",
        {
            username,
            authkey
        }
    )

}

export const setupPagerRequest = ( username, authkey, pagerid, first, last, grade ) => {

    return post(
        "/api/setup_pager",
        {
            username,
            authkey,
            pagerid,
            first,
            last,
            grade,
        });

}
















