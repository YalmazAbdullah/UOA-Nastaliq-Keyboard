import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

// Button that makes API request to create user and gets back
// experimental structure information such as id, stimulus bins, condition order
export default function ButtonStartStudy() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Create the user session or restore if already exists
  const createSession = async () => {
    // Prevent duplicate requests
    if (loading) return; 
    setLoading(true);


    // check local storage to see if already in progress/completed
    const status = localStorage.getItem("status");
    if(status && status==="completed"){
      console.log("Study already completed.");
      navigate("/end");
    }
    else if(status && status==="inprogress"){
      console.log("Study already in progress. Restore session.");
      let index = Number(localStorage.getItem("current_condition"));
      let conditions = localStorage.getItem("conditions");
      restore = JSON.parse(conditions)[index].toLowerCase();
      navigate("/"+restore);
    }
    

    // API request to fetch session
    try {
      const res = await axios.post("http://127.0.0.1:8000/start_session");
      //double check if study is complete
      if(res.data["message"] == "Study Complete"){
        // study is already completed
        navigate("/end");
      }
      else{
        // Success
        localStorage.clear();
        localStorage.setItem("current_condition", 0);
        localStorage.setItem("current_stim", 0);
        localStorage.setItem("uid", res.data["uid"]);
        localStorage.setItem("code", res.data["code"]);
        localStorage.setItem("conditions", JSON.stringify(res.data["conditions"]));
        localStorage.setItem("stimuli", JSON.stringify(res.data["stimuli"]));
        navigate("/baseline");
      }

    } catch (err) {
      console.error(err);
    } finally {
      // Enable button after request completes
      setLoading(false);
    }
  };

  return (
    <div>
        <button 
        type = "submit" 
        onClick={createSession}
        disabled={loading}
        className="px-10 mt-3 py-2 bg-black text-white text-lg hover:underline">
            Start
        </button>
    </div>
  );
}
