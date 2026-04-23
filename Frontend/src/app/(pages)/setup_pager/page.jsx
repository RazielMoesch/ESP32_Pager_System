
import SetupPagerBox from "@/Components/SetupPagerBox";
import { cookies } from "next/headers";




const SetupPagerPage = async () => {


    const store = await cookies();
    const username = store.get("username")?.value;
    const authkey = store.get("authkey")?.value;



    return <>
    
        <SetupPagerBox username={username} authkey={authkey}  ></SetupPagerBox>
    
    </>

}

export default SetupPagerPage;