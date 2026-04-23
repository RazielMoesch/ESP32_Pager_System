
'use client'

import { useEffect, useState } from "react";
import "./Styles/StudentsBox.css";
import { getPagersRequest, removePagerRequest } from "@/Helpers/ServerCalls";
import { useRouter } from "next/navigation";


const StudentsBox = ({ username, authkey }) => {

    const [students, setStudents] = useState([]);
    const router = useRouter();

    const getStudents = async () => {

        const res = await getPagersRequest(username, authkey);
        console.log("Students: ", res)
        setStudents(res.pagers)

    }

    const deleteStudent = async (pid) => {

        const res = await removePagerRequest(username, authkey, pid);
        await getStudents();
    }

    useEffect(
        () => {

            getStudents();

        }, []
    )
    

    return <>


    <div className="students-box-container">

        <h1>Students</h1>


        {

            students && students
                        .sort((a, b) => a[1].localeCompare(b[1], undefined, { sensitivity: "base" }))
                        .map(
                (student, idx) => (

                    <div key={idx} className="student-box-row-wrapper">

                        <div className="student-name-id-wrapper">
                            <p className="student-box-row-name" onClick={() => router.push(`/messages/${student[2]}?first=${student[0]}&last=${student[1]}`)}> {student[0]} {student[1]}</p>
                            <p className="student-box-row-id"> {student[2]} </p>
                        </div>
                        
                        <button className="student-box-row-delete-button" onClick={() => deleteStudent(student[2])}>Delete</button>

                        
                    </div>
                    
                )
            )
        }


    </div>
    
    </>

}


export default StudentsBox;