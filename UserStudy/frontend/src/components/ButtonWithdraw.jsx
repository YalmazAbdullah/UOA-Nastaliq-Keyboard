import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { endpoint_live } from "../api";

export default function ButtonWithdraw(){
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const withdraw = async () =>{
        // Prevent duplicate requests
        if (loading) return;

        // Show confirmation popup
        const confirmed = window.confirm("Are you sure you want to withdraw?");
        if (!confirmed) return; // Stop if user clicks Cancel

        // Enable button after request intiated
        setLoading(true);
        
        localStorage.setItem("status","withdrawn");
        navigate("/withdraw");

        // API request to fetch session
        try {
            let id = localStorage.getItem("uid")
            await axios.put(endpoint_live+"withdraw?uid="+id);
        } catch (err) {
            console.error(err);
        } finally {
            // Renable after complete
            setLoading(false);
        }
    }

    return (<>
        <button 
        type = "button" 
        onClick={withdraw}
        disabled={loading}
        className="px-10 mt-3 py-2 bg-gray text-black border-3 hover:bg-black hover:text-white text-lg hover:underline">
            Withdraw
        </button>
    </>)
}