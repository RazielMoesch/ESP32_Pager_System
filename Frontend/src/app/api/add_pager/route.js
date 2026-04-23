

import { post, API_URL } from "@/Helpers/ServerCalls";
import { NextResponse } from "next/server";

export const POST = async (req) => {

    const { username, authkey, studentfirst, studentlast, pagerid, grade } = await req.json();

    const res = await post(
        `${API_URL}/add_pager`,
        {
            username,
            authkey,
            studentfirst,
            studentlast,
            pagerid,
            grade
        }
    );

    const data = await res;


    return NextResponse.json(data);
}
