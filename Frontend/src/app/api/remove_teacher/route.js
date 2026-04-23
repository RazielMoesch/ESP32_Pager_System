

import { post, API_URL } from "@/Helpers/ServerCalls";
import { NextResponse } from "next/server";

export const POST = async (req) => {

    const { username, authkey, targetusername} = await req.json();

    const res = await post(
        `${API_URL}/remove_teacher`,
        {
            username,
            authkey,
            targetusername
        }
    )

    const data = await res;


    return NextResponse.json(data);
}