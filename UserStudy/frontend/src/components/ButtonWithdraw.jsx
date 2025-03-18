import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function ButtonWithdraw(){
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const withdraw = async () =>{
        // Prevent duplicate requests
        if (loading) {return; }
        
        localStorage.setItem("status","withdrawn");
        navigate("/withdraw");

        // API request to fetch session
        try {
            let id = localStorage.getItem("uid")
            await axios.put("http://localhost:8000/withdraw?uid="+id);
        } catch (err) {
            console.error(err);
        } finally {
            // Enable button after request completes
            setLoading(true);
        }
    }

    return (<>
        <button 
        type = "submit" 
        onClick={withdraw}
        disabled={loading}
        className="px-10 mt-3 py-2 bg-black text-white text-lg hover:underline">
            Withdraw
        </button>
    </>)
}