

import { post, API_URL } from "@/Helpers/ServerCalls";
import { NextResponse } from "next/server";

export const POST = async (req) => {

    const { username, authkey, pagerid } = await req.json();

    const res = await post(
        `${API_URL}/remove_pager`,
        {
            username,
            authkey,
            pagerid
        }
    );

    const data = await res;


    return NextResponse.json(data);
}
