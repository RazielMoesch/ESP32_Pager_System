

import { post, API_URL } from "@/Helpers/ServerCalls";
import { NextResponse } from "next/server";

export const POST = async (req) => {

    const { username, authkey, msgtype, content, pagerid, grade } = await req.json();

    const res = await post(
        `${API_URL}/add_message`,
        {
            username,
            authkey,
            msgtype, 
            content, 
            pagerid, 
            grade
            
        }
    );

    const data = await res;


    return NextResponse.json(data);
}
