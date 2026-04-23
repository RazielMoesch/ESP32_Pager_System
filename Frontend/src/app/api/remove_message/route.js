



import { post, API_URL } from "@/Helpers/ServerCalls";
import { NextResponse } from "next/server";

export const POST = async (req) => {

    const { username, authkey, msgid } = await req.json();

    const res = await post(
        `${API_URL}/remove_message`,
        {
            username,
            authkey,
            msgid
            
        }
    );

    const data = await res;


    return NextResponse.json(data);
}
