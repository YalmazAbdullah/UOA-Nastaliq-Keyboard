import React from "react";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import InputLayout from "../components/InputLayout";
import KeyboardVis from "../components/KeyboardVis";
import {CRULP_LAYOUT} from "../assets/layouts"
import {QWERTY_TO_CRULP} from "../assets/layouts"
import {CRULP_TO_QWERTY} from "../assets/layouts"
const stimuli = [
    "یہ کہانی دس بار سو لی 1",
    "یہ کہانی دس بار سو لی 2",
]

// @TODO:
// retrive id
// retrive stimulus
// retrive next condition
// send it over to the input
// fix item counter to handle local storage
// navigate to next condition 
export default function Crulp() {
    const [counter, setCounter] = useState(0);
    const navigate = useNavigate();

    // Redirect when current > 20
    useEffect(() => {
        if (counter >= stimuli.length) {
            navigate("/windows");
        }
    }, [counter, navigate]);

    useEffect(()=>{},[])

    return (
        <div className=" p-6 px-[10vw] flex-col space-y-3 justify-center">
            <div>
                <h1 className="text-7xl font-black">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">CRULP</h3>
            </div>
            <h3 className="mt-10 px-3 bg-black text-white text-2xl">
                In this condition we evaluate the CRULP Urdu Layout keyboard.
            </h3>
            <p>
                To get an idea of how fast you type, we would like you to please enter the text below. As you type, correct input will be highlighted in <span className="bg-correct border-1">green</span>, and any mistakes will show up on the lower text highlighted in <span className="bg-error border-1">red</span>. 
            </p>
            <div className="bg-gray border-4 p-6">
                <div className="flex justify-center">
                    <div className=" w-20 text-2xl border-black border-2 bg-white text-center">{counter}/{stimuli.length}</div>
                </div>
                <InputLayout qwerty_ur = {QWERTY_TO_CRULP} ur_qwerty = {CRULP_TO_QWERTY} targetText={stimuli[counter]} setCounter={setCounter}/>
                <KeyboardVis layout={CRULP_LAYOUT}/>
            </div>
        </div>
    );
}