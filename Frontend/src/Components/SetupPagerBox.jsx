
'use client'

import { addPagerRequest, setupPagerRequest } from "@/Helpers/ServerCalls"
import { useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import "./Styles/SetupPagerBox.css";

const SetupPagerBox = ({ username, authkey }) => {

    const router = useRouter();
    const searchParams = useSearchParams();
    const [first, setFirst] = useState("");
    const [last, setLast] = useState("");
    const [grade, setGrade] = useState(9);
    const [pagerid, setPagerid] = useState(searchParams.get("pagerid"));


    const addPager = async () => {

        const result = await addPagerRequest(username, authkey, first, last, pagerid, grade);

        if (result.status !== "success") {
            return;
        }



    }
    
    const setupPager = async () => {

        if (first === "") {
            alert("Missing First Name");
            return;
        }

        if (last==="") {
            alert("Missing Last Name");
            return;
        }
        if ( parseInt(grade) < 9 || parseInt(grade) > 12 ) {
            alert("Grade Needs to be between 9 and 12.");
            return;
        }
        const result = await setupPagerRequest(username, authkey, pagerid, first, last, parseInt(grade));

        if (result.status !== "success") {
            alert("Failed to setup pager.");
            return;
        }

        await addPager();
        alert("Pager has been setup. Redirecting...")
        router.push("/pager_setup_requests")


    }

    return <>
    
        <div className="setup-pager-box-container">

            <input className="setup-pager-box-input" type="text" placeholder="First" value={first} onChange={e => setFirst(e.target.value)} />
            <input className="setup-pager-box-input" type="text" placeholder="Last" value={last} onChange={e => setLast(e.target.value)} />
            <input className="setup-pager-box-input" type="text" placeholder="Grade" value={grade} onChange={e => setGrade(e.target.value)} />
            <input className="setup-pager-box-input" type="text" placeholder="PagerID" value={pagerid} onChange={e => setPagerid(e.target.value)} />

            <button onClick={setupPager}>Finish Setup</button>

        </div>
    
    
    </>

}





export default SetupPagerBox;








