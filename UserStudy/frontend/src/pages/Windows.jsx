import React from "react";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import InputLayout from "../components/InputLayout";
import KeyboardVis from "../components/KeyboardVis";
import {WINDOWS_LAYOUT} from "../assets/layouts"
import {QWERTY_TO_WINDOWS} from "../assets/layouts"
import {WINDOWS_TO_QWERTY} from "../assets/layouts"
import ButtonWithdraw from "../components/ButtonWithdraw";

export default function Windows() {
    const [currentStim, setCurrentStim] = useState(0);
    const [stimuli, setStimuli] = useState(["test"]);
    const [bg_color, setBgColor] = useState("bg-white")
    const [box_color, setBoxColor] = useState("bg-gray")
    const navigate = useNavigate();

    // retrives experiment information.
    useEffect(()=>{
            //if current condition not baseline then move to actual current condition. Prevents back tracking.
            let conditionIndex = Number(localStorage.getItem("current_condition"))
            let conditions = JSON.parse(localStorage.getItem("conditions"))
            let currentCondition = conditions[conditionIndex];
            console.log(conditions)
            currentCondition = currentCondition.toLowerCase();
            if (currentCondition !== "ime"){
                console.log("condition already completed")
                navigate("/"+currentCondition);
            }
    
            // set user values
            setCurrentStim(Number(localStorage.getItem("current_stim")));
            setStimuli(JSON.parse(localStorage.getItem("stimuli"))[conditionIndex])
        },[])

    // redirect when current surpasses stimuli count.
    useEffect(() => {
        if (currentStim >= stimuli.length) {
            // increment condition counter and move to next condition
            let conditionIndex = Number(localStorage.getItem("current_condition")) +1;
            localStorage.setItem("current_condition", conditionIndex);
            localStorage.setItem("current_stim", 0);
            const conditions = localStorage.getItem("conditions");
            const next = JSON.parse(conditions)[conditionIndex].toLowerCase();
            navigate("/" + next);
        }else if(currentStim> 0){
            // update to stimulus index
            localStorage.setItem("current_stim", currentStim)
        }
    }, [currentStim, navigate]);

    return (
        <div className={`h-screen ${bg_color} p-6 px-[10vw] flex-col space-y-3 justify-center`}>
            {/* Page title */}
            <div>
                <h1 className="text-7xl font-black">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">WINDOWS</h3>
            </div>
            
            {/* Subtitle */}
            <h3 className="px-3 bg-black text-white text-2xl">
                In this condition we evaluate the WINDOWS Urdu Layout keyboard.
            </h3>

            {/* Instructions */}
            <p>
                In this condtion we will be evaluating the WINDOWS keyboard layout. This is a frequency based keyboard layout, meaning that the most frequently occuring Urdu letters are mapped to the most easily accessible keys. For example <span className="text-lg font-ur-sans">"ن"</span> is mapped to "f" because <span className="text-lg font-ur-sans">"ن"</span> is one of the most frequently occuring letters in Urdu and "f" is one of the most easily accessible keys on the keyboard. Typing the uppercase "F" will input <span className="text-lg font-ur-sans">"ں"</span>. We can confirm this by examining a visualization of the layout shown below. 
            </p>
            <p>
                As before the first two sentences are just to help you understand the input system. When you feel ready please click on the text in the box below to begin. 
            </p>

            {/* Input */}
            <div className={`${box_color} border-4 p-6`}>
                <div className="flex justify-center">
                    <div className=" w-20 text-2xl border-black border-2 bg-white text-center">{currentStim}/{stimuli.length}</div>
                </div>
                <InputLayout condition = {"windows"} qwerty_ur = {QWERTY_TO_WINDOWS} ur_qwerty = {WINDOWS_TO_QWERTY} targetText={stimuli[currentStim]} setCurrentStim ={setCurrentStim} setBoxColor = {setBoxColor} setBgColor = {setBgColor}/>
                <KeyboardVis layout={WINDOWS_LAYOUT}/>
            </div>
            <ButtonWithdraw/>
        </div>
    );
}