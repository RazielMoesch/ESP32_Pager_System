

import { post, API_URL } from "@/Helpers/ServerCalls";
import { NextResponse } from "next/server";
import { cookies } from "next/headers";

export const POST = async (req) => {

    const { username, password } = await req.json();

    const res = await post(
        `${API_URL}/login`,
        {
            username,
            password
        }
    )

    const data = await res;

    console.log("Authkey: ", data.authkey);

    const response = NextResponse.json({ success: true })

    response.cookies.set("username", username,
        {
        httpOnly: true,
        path: "/",
        maxAge: 60 * 60 * 24 * 30,
    });

    response.cookies.set("authkey", data.authkey,
        {
            httpOnly: true,
            path: "/",
            maxAge: 60 * 60 * 24 * 30,
        });

    return response;
}