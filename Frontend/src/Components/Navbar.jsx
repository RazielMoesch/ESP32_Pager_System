
'use client'

import "./Styles/Navbar.css";
import { useRouter } from "next/navigation";
import { logout } from "@/app/(pages)/actions/logout";
import { usePathname } from "next/navigation";

const Navbar = () => {

    const pathname = usePathname();
    const router = useRouter();    


    return <>

        <div className="navbar-container">


            <h1 className="navbar-header">Pagers</h1>

            <div className="navbar-links-wrapper">

                <p onClick={() => router.push("/students")} className="navbar-link-text">Students</p>
                <p onClick={() => router.push("/pager_setup_requests")} className="navbar-link-text">Pager Setup</p>

                {
                    pathname !== "/login" &&
                    <p onClick={logout} className="logout-button">Logout</p>
                }
               

            </div>

        </div>
    
    
    </>
}

export default Navbar;

