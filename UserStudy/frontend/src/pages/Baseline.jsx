import React from "react";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import KeyboardVis from "../components/KeyboardVis";
import InputBaseline from "../components/InputBaseline";
import {QWERTY_LAYOUT} from "../assets/layouts"
import ButtonWithdraw from "../components/ButtonWithdraw";

// Baseline condition to get measure typing speed of the user.
export default function Baseline() {
    const [currentStim, setCurrentStim] = useState(0);
    const [stimuli, setStimuli] = useState(["test"]);
    const [bg_color, setBgColor] = useState("bg-white")
    const [box_color, setBoxColor] = useState("bg-gray")
    const navigate = useNavigate();

    // retrives id and current condition.
    useEffect(()=>{
        //if current condition not baseline then move to actual current condition. Prevents back tracking.
        let cached_currentCondition = Number(localStorage.getItem("current_condition"));
        if (cached_currentCondition !=0){
            console.log("condition already completed")
            let conditions = localStorage.getItem("conditions");
            let restore = JSON.parse(conditions)[cached_currentCondition].toLowerCase();
            navigate("/"+restore);
        }

        // set user values
        setCurrentStim(Number(localStorage.getItem("current_stim")));
        setStimuli(JSON.parse(localStorage.getItem("stimuli"))[0])
    },[])

    // redirect when current surpasses stimuli count.
    useEffect(() => {
        if (currentStim >= stimuli.length) {
            // increment condition counter and move to next condition
            localStorage.setItem("current_condition", 1);
            localStorage.setItem("current_stim", 0);
            const conditions = localStorage.getItem("conditions");
            const next = JSON.parse(conditions)[1].toLowerCase();
            navigate("/" + next);
        }else if(currentStim> 0){
            // update to stimulus index
            localStorage.setItem("current_stim", currentStim);
        }
    }, [currentStim, navigate]);

    return (
        <div className={`h-screen ${bg_color} p-6 px-[10vw] flex-col space-y-3 justify-center`}>
            {/* Page title */}
            <div>
                <h1 className="text-7xl font-black">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Measuring Baseline</h3>
            </div>
            {/* Subtitle */}
            <h3 className="px-3 bg-black text-white text-2xl">
                We will begin by taking a baseline of your typing speed.
            </h3>
            {/* Instructions */}
            <p>
                To get an idea of how fast you type, we would like you to please type out the text samples below. These are pseudo sentences that use words which sound similar to English but have no actual meaning. As you type, correct input will be highlighted in <span className="bg-correct border-1">green</span>, and any mistakes will show up on the lower text highlighted in <span className="bg-error border-1">red</span>. 
            </p>
            <p>
                The first two sentences are just to help you understand the input system. When you feel ready please click on the text in the box below to begin.
            </p>
            {/* Input */}
            <div className={`${box_color} border-4 p-6`}>
                <div className="flex justify-center">
                    <div className=" w-20 text-2xl border-black border-2 bg-white text-center">{currentStim}/{stimuli.length}</div>
                </div>
                <InputBaseline targetText={stimuli[currentStim]} setCurrentStim ={setCurrentStim} setBoxColor = {setBoxColor} setBgColor = {setBgColor}/>
                <KeyboardVis layout={QWERTY_LAYOUT}/>
            </div>
            <ButtonWithdraw/>
        </div>
    );
}