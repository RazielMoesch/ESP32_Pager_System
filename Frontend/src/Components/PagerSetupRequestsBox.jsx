

'use client'

import { getSetupRequestsRequest } from "@/Helpers/ServerCalls";
import { useEffect, useState } from "react";
import "./Styles/PagerSetupRequestsBox.css";
import { useRouter } from "next/navigation";


const PagerSetupRequestsBox = ({ username, authkey }) => {

    const router = useRouter();
    const [setupRequests, setSetupRequests] = useState([]);

    const getSetupRequests = async () => {

        const data = await getSetupRequestsRequest(username, authkey);

        console.log("Setup Requests:", data);
        console.log(data.setuprequests)

        if (data.status !== "success") {
            return;
        }


        setSetupRequests(data.setuprequests);

    }



    useEffect(
        () => {

            getSetupRequests();

        }, []
    )

    return <>

        <div className="setup-requests-box-container">

            {
            setupRequests ? setupRequests.map(
                (req, idx) => {
                    return(
                    <div className="setup-requests-row" key={idx}>

                        <p className="setup-requests-pagerid">{req}</p>

                        <button className="setup-requests-setup-button" onClick={() => router.push(`/setup_pager?pagerid=${req}`)}>Setup</button>

                    </div>
                    )

                } 
            ) : 
            <h1>No Setup Requests</h1>
        }

        </div>
    
        
    
    </>

}


export default PagerSetupRequestsBox;

