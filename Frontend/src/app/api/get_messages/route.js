

import { post, API_URL } from "@/Helpers/ServerCalls";
import { NextResponse } from "next/server";

export const POST = async (req) => {

    const { username, authkey, pagerid, grade } = await req.json();

    const res = await post(
        `${API_URL}/teacher/get_messages`,
        {
            username,
            authkey,
            pagerid, 
            grade
            
        }
    );

    const data = await res;


    return NextResponse.json(data);
}
