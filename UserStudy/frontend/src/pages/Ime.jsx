import React from "react";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import KeyboardVis from "../components/KeyboardVis";
import InputIme from "../components/InputIme";
import {QWERTY_LAYOUT} from "../assets/layouts"
const stimuli = [
    "یہ کہانی دس بار سو لی 1",
    "یہ کہانی دس بار سو لی 2",
]

export default function Ime() {
    const [uid, setUid] = useState(null);
    const [stimuli, setStimuli] = useState(["test"]);
    const [counter, setCounter] = useState(0);
    const navigate = useNavigate();

    // retrives experiment information.
    useEffect(()=>{
        // id
        const id = localStorage.getItem("uid");
        if (id) {
            setUid(id);
        }
        else{
            console.log("no id")
        }
        
        // stimuli
        const bin = localStorage.getItem("stimuli_bins");
        let current_condition = Number(localStorage.getItem("current_condition"))
        if (bin && current_condition){
            // get stimuli list
            let all_stimuli = JSON.parse(bin)[current_condition];
            // add tutorial value
            all_stimuli.shift("test X"); 
            setStimuli(all_stimuli);
        }else{
            console.log("no stimuli")
        }

        // start counter
        const cached_counter = localStorage.getItem("counter");
        if(cached_counter){
            setCounter(Number(cached_counter))
        }
    },[])
    
    // redirect when current surpasses stimuli count.
    useEffect(() => {
        if (counter >= stimuli.length) {
            // reset counter from local storage
            localStorage.setItem("counter", 0)
            const conditions = localStorage.getItem("condition_order");
            // incremement condition count
            // figure out where next
            if (current_condition >= 2){
                navigate("/end");
            }else{
                let current_condition = Number(localStorage.getItem("current_condition")) +1;
                localStorage.setItem("current_condition", current_condition);
                const next = JSON.parse(conditions)[current_condition].toLowerCase();
            }
        }else if(counter> 0){
            // update to local storage
            localStorage.setItem("counter", counter)
        }
    }, [counter, navigate]);

    return (
        <div className=" p-6 px-[10vw] flex-col space-y-3 justify-center">
            {/* Page title */}
            <div>
                <h1 className="text-7xl font-black">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">IME</h3>
            </div>

            {/* Subtitle */}
            <h3 className="mt-10 px-3 bg-black text-white text-2xl">
                In this condition we evaluate the WINDOWS Urdu Layout keyboard.
            </h3>

            {/* Instructions */}
            <p>
                In this condtion we will be evaluating the WINDOWS keyboard layout. It is a phonetic keyboard layout, meaning that the Urdu letters are mapped to similar sounding English letters. For example <span className="text-lg font-ur-sans">'ک'</span> is mapped to 'k'. Looking at the keyboard layout below you can confirm this by looking at the 'k' key which should lookg similar to: Typing the uppercase 'K' will input <span className="text-lg font-ur-sans">'خ'</span>.
            </p>

            {/* Input */}
            <div className="bg-gray border-4 p-6">
                <div className="flex justify-center">
                    <div className=" w-20 text-2xl border-black border-2 bg-white text-center">{counter}/{stimuli.length}</div>
                </div>
                <InputIme targetText={stimuli[counter]} setCounter={setCounter}/>
                <KeyboardVis layout={QWERTY_LAYOUT}/>
            </div>
        </div>
    );
}