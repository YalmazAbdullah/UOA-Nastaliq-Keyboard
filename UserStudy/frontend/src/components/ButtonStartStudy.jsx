import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

// Button that makes API request to create user and gets back
// experimental structure information such as id, stimulus bins, condition order
export default function ButtonStartStudy() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const createUserEntry = async () => {
    // Prevent duplicate requests
    if (loading) return; 
    setLoading(true);

    // API request
    try {
      const res = await axios.post("http://127.0.0.1:8000/start_session");

      if(res.data["message"] == "Study Complete"){
        navigate("/end");
      }
      else{
        // Success
        localStorage.clear();
        localStorage.setItem("uid", res.data["uid"]);
        localStorage.setItem("stimuli_bins", JSON.stringify(res.data["stimuli_bins"]));
        localStorage.setItem("condition_order", JSON.stringify(res.data["condition_order"]));
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
        onClick={createUserEntry}
        disabled={loading}
        className="px-10 mt-3 py-2 bg-black text-white text-lg hover:underline">
            Start
        </button>
    </div>
  );
}
