

import PagerSetupRequestsBox from "@/Components/PagerSetupRequestsBox";
import { cookies } from "next/headers";


const PagerSetup = async () => {


    const store = await cookies();

    const username = store.get("username")?.value;
    const authkey = store.get("authkey")?.value;


    return <>
    
    
        
    <PagerSetupRequestsBox username={username} authkey={authkey} ></PagerSetupRequestsBox>
    
    </>

}


export default PagerSetup;