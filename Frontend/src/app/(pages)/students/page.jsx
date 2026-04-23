


import StudentsBox from "@/Components/StudentsBox";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

const StudentsPage = async () => {

    const store = await cookies();

    const username = store.get("username")?.value;
    const authkey = store.get("authkey")?.value;

    if (!username || !authkey) {
        redirect("/login")
    }

    return <>
    
        <StudentsBox username={username} authkey={authkey}></StudentsBox>

    </>


}


export default StudentsPage;