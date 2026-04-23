import { API_URL, post } from "@/Helpers/ServerCalls";
import { NextResponse } from "next/server";




export const POST = async (req) => {

    const {username, authkey} = await req.json();

    const data = await post(
        `${API_URL}/get_setup_requests`,
        {
            username,
            authkey
        }
    )

    return NextResponse.json(data);

}