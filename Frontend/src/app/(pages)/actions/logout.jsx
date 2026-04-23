

'use server'

import { cookies } from "next/headers"
import { redirect } from "next/navigation";

export const logout = async () => {


    const store = await cookies();

    store.delete("username");
    store.delete("password");

    redirect("/login");


}