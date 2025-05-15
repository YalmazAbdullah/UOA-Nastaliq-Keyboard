import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { endpoint_live } from "../api";

export default function ButtonStartSCondition({target}) {
    const navigate = useNavigate();

    const createSession = async () => {
        navigate(target);
    }

    return (
    <>
        <button 
        type = "submit" 
        onClick={createSession}
        className="px-10 mt-3 py-2 bg-black text-white text-lg hover:underline">
            Start Condition
        </button>
    </>
  );
}