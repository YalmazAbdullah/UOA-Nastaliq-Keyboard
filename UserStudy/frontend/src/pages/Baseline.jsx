import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import KeyboardVis from "../components/KeyboardVis";
import InputBaseline from "../components/InputBaseline";
import {QWERTY_LAYOUT} from "../assets/layouts"
const stimuli = [
    "this is a test input for the baseline 1",
    "this is a test input for the baseline 2",
]

export default function Baseline() {
    const [counter, setCounter] = useState(0);
    const navigate = useNavigate();

    // Redirect when current > 20
    useEffect(() => {
        if (counter >= stimuli.length-1) {
            navigate("/crulp");
        }
    }, [counter, navigate]);

    useEffect(()=>{},[])

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
                <InputBaseline targetText={stimuli[counter]} setCounter={setCounter}/>
                <KeyboardVis layout={QWERTY_LAYOUT}/>
            </div>
        </div>
    );
}