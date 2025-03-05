import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import KeyboardVis from "../components/KeyboardVis";
import InputBaseline from "../components/InputBaseline";
import {QWERTY_LAYOUT} from "../assets/layouts"

// Hard Coded Stimuli
const stimuli = [
    "this is a test input for the baseline 1",
    "this is a test input for the baseline 2",
    "this is a test input for the baseline 3",
    "this is a test input for the baseline 4",
    "this is a test input for the baseline 5",
]

export default function Baseline() {
    const [uid, setUid] = useState(null);
    const [counter, setCounter] = useState(0);
    const navigate = useNavigate();

    // Retrives id and @TODO: first condition from local storage.
    useEffect(()=>{
        const id = localStorage.getItem("uid");
        if (id) {
            setUid(id);
        }
        else{
            console.log("no id")
        }
        
        const cached_counter = localStorage.getItem("counter");
        if(cached_counter){
            console.log("should be first")
            console.log(cached_counter)
            setCounter(Number(cached_counter))
        }
    },[])
 
    // Redirect when current surpasses stimuli count.
    useEffect(() => {
        if (counter >= stimuli.length) {
            // reset counter from local storage
            localStorage.setItem("counter", 0)
            navigate("/crulp");
        }else if(counter> 0){
            // update to local storage
            localStorage.setItem("counter", counter)
        }
    }, [counter, navigate]);

    return (
        <div className=" p-6 px-[10vw] flex-col space-y-3 justify-center">
            <div>
                <h1 className="text-7xl font-black">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Measuring Baseline</h3>
            </div>
            <h3 className="mt-10 px-3 bg-black text-white text-2xl">
                We will begin by taking a baseline of your typing speed.
            </h3>
            <p>
                To get an idea of how fast you type, we would like you to please enter the text below. As you type, correct input will be highlighted in <span className="bg-correct border-1">green</span>, and any mistakes will show up on the lower text highlighted in <span className="bg-error border-1">red</span>. 
            </p>
            <div className="bg-gray border-4 p-6">
                <div className="flex justify-center">
                    <div className=" w-20 text-2xl border-black border-2 bg-white text-center">{counter}/{stimuli.length}</div>
                </div>
                <InputBaseline id={uid} targetText={stimuli[counter]} setCounter={setCounter}/>
                <KeyboardVis layout={QWERTY_LAYOUT}/>
            </div>
        </div>
    );
}