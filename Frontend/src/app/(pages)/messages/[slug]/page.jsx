
import StudentMessagesBox from "@/Components/StudentMessagesBox";
import { cookies } from "next/headers";




const MessagesPageSlug = async ({ params, searchParams }) => {

    const store = await cookies();

    const username = store.get("username")?.value;
    const authkey = store.get("authkey")?.value;

    const {slug} = await params;
    const { first, last, } = await searchParams;



    return <>
    
        <StudentMessagesBox username={username} authkey={authkey} pagerid={slug} first={first} last={last}></StudentMessagesBox>
    
    </>


}


export default MessagesPageSlug;

