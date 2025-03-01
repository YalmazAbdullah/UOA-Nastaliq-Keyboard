import React from "react";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import KeyboardVis from "../components/KeyboardVis";
import InputIme from "../components/InputIme";
import {QWERTY_LAYOUT} from "../assets/layouts"
const stimuli = [
    "this is a test input for the baseline 1",
    "this is a test input for the baseline 2",
    "this is a test input for the baseline 3",
    "this is a test input for the baseline 4",
    "this is a test input for the baseline 5",
]

export default function Ime() {
    const [counter, setCounter] = useState(0);
    const navigate = useNavigate();

    // Redirect when current > 20
    useEffect(() => {
        if (counter > 20) {
            navigate("/crulp");
        }
    }, [counter, navigate]);

    useEffect(()=>{},[])

    return (
        <div className="flex-col justify-center space-y-3 p-6">
            <div>
                <h1 className="text-7xl font-bold">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl">Measuring Baseline</h3>
            </div>
            <div className="bg-gray-700 border-2 p-6 mt-10">
                <div className="flex justify-center">
                    <div className=" w-20 text-2xl border-black border-2 bg-white text-center">{counter}/20</div>
                </div>
                <InputIme layout={QWERTY_LAYOUT} setCounter={setCounter}/>
                <KeyboardVis layout={QWERTY_LAYOUT}/>
            </div>
        </div>
    );
}