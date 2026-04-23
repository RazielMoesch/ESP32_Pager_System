
'use client'

import { sendLoginRequest } from "@/Helpers/ServerCalls"
import { useState } from "react"
import { useRouter } from "next/navigation"
import "./Styles/LoginBox.css"




const LoginBox = () => {

    const router = useRouter();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState(null);


    const handleEnter = (e) => {

        if (e.key === "Enter") {
            handleLogin()
        }

    }

    const handleLogin = async () => {
        
        const data = await sendLoginRequest(username, password);
        console.log("Sent Login Request.");
        
        if (data.success === true) {
            router.push("/students")
        }
        else {
            console.log("Login Did Not Work. Status:", data)
            setError("Username & Password Combination do not match.");
        }

    }


    return <>

    <div className="login-box-container">

        <h1 className="login-box-title">Teacher Login</h1>

        <div className="login-box-inputs-wrapper">

            <input 
                className="login-box-username-input" 
                placeholder="Username"
                type="text" value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                onKeyDown={handleEnter}
                />

            <div className="login-box-password-input-wrapper">

                <input 
                    className="login-box-password-input" 
                    placeholder="Password"
                    type={showPassword ? "text" : "password"} 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    onKeyDown={handleEnter}
                    />

                <button 
                    className="login-box-toggle-show-pw-button" 
                    onClick={() => setShowPassword(p=>!p)}
                    
                    > 
                    {showPassword ? "Hide" : "Show"} 
                    </button>

            </div>
            
        </div>

        <button className="login-box-login-button"
            onClick={handleLogin}
        >
            Log In
        </button>

    </div>
    
    
    </>


}


export default LoginBox;