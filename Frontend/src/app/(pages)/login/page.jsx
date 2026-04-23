
import { cookies } from "next/headers"
import { redirect } from "next/navigation";
import { getMessagesRequest } from "@/Helpers/ServerCalls";
import LoginBox from "@/Components/LoginBox";

const LoginPage = async () => {


    const store = await cookies();

    const username = store.get("username")?.value;
    const authkey = store.get("authkey")?.value;

    console.log(`Username: ${username} | Authkey: ${authkey}`)

    if ( username && authkey ) {
        
        redirect("/students")
        
    }
    

    return <>
    
        <LoginBox></LoginBox>

    </>

}

export default LoginPage;