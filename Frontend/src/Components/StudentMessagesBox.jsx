'use client'

import { addMessageRequest, getMessagesRequest, removeMessageRequest } from "@/Helpers/ServerCalls";
import "./Styles/StudentMessagesBox.css";
import { useEffect, useState } from "react";

const StudentMessagesBox = ({ username, authkey, pagerid, first, last }) => {

    const [messages, setMessages] = useState();
    const [sendingMsg, setSendingMsg] = useState(false);
    const [newMsg, setNewMsg] = useState("");


    const getMessages = async () => {

        const data = await getMessagesRequest(username, authkey, pagerid);

        setMessages(data.messages)


    }

    const deleteMessage = async (msgid) => {

        await removeMessageRequest(username, authkey, msgid);
        getMessages();
    }

    const sendMessage = async () => {

        if (newMsg.length === 0 || newMsg === null) {
            return;
        }

        const result = await addMessageRequest(username, authkey, "individual", newMsg, pagerid)
        if ( result.status === "success" ) {
            setNewMsg("");
            getMessages();
            return;
        } 

        alert("Send Message Failed. Please Try Again.");

    }


    useEffect(
        () => {
            getMessages();
        }, []
    )

    console.log("Slug:", pagerid, first, last)
    return (
        <div className="student-messages-box-container">
            <h1 className="students-messages-box-title">{String(first)} {last} | {pagerid}</h1>

            {
                sendingMsg && 
                
                <div className="send-message-container">

                    <p className="send-message-from">From: {username}</p>
                    <textarea value={newMsg} onChange={e => setNewMsg(e.target.value)} className="send-message-text-area" placeholder="Message Goes Here."></textarea>
                    
                </div>
            }

            <div className="send-message-buttons-container">

                <button onClick={() => setSendingMsg(p=>!p)} className="send-message-toggle-button">
                {
                    sendingMsg ? "Cancel" : "Send Message"
                }
                </button>

                {
                    sendingMsg && 
                    <button className="send-message-button" onClick={sendMessage}>
                        Send
                    </button>
                }
                

            </div>
            

            {

                (messages?.length!==0 && messages) ? [...messages].reverse().map(
                    (msg, idx) => {
                        return (
                            
                            <div className="student-message-row" key={idx}> 
                            
                                <div className="student-message-row-info">
                                    <p className="student-message-sentby-text">{msg[1]}</p>
                                    <p className="student-message">{msg[3]}</p>
                                </div>
                                
                                <button className="student-message-delete-button" onClick={() => deleteMessage(msg[0])}>Delete</button>

                             </div>
                            

                        )
                    }
                ) :
                <h3>No Messages.</h3>


            }


        </div>
    );
}

export default StudentMessagesBox;