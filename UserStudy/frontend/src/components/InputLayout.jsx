import React from "react";
import axios from "axios";
import { useState, useRef, useEffect } from "react";
import {ADJACENCY} from "../assets/error_data"
import { endpoint_live } from "../api";

export default function InputLayout({condition = "", qwerty_ur, ur_qwerty, targetText = "", setCurrentStim, setBoxColor, setBgColor }){
    const [input, setInput] = useState("");
    const [keyLog, setKeyLog] = useState([]);
    const [startTime, setStartTime] = useState(null);
    const [errorLog, setErrorLog] = useState([]);
    const [transposition_count, setTrans] = useState(0);
    const [ommission_count, setOmm] = useState(0);
    const [substitution_count, setSub] = useState(0);
    const [addition_count, setAdd] = useState(0);
    const [isEmpty, setIsEmpty] = useState(true);

    const inputRef = useRef(null);

    const [start, setStart] = useState(false);
    const [end, setEnd] = useState(false)
    const [isFocused, setFocus] = useState(false)

    // start timer
    const handleFocus = (e) =>{
        setFocus(true)
        if (start === false){
            setStart(true);
            setBoxColor("bg-white")
            setBgColor("bg-gray")
        }
    }

    const handleKeyDown = (e) => {
        // cache time stamp
        let timestamp = Date.now()
        // dont do anything if not started
        if (start === false){
            e.preventDefault();
            return;
        }else if (start=== true && startTime === null){
            setStartTime(timestamp);
        }

        // Filter the inputs and log
        switch (e.key) {
        case "ArrowDown" || "ArrowUp" || "ArrowLeft" || "ArrowRight":
            // prevent cursor navigation.
            e.preventDefault();
        default:
            // log key input that is not navigation keys. Still logs some unneccissary stuff but that can be cleaned later.
            console.log(e.key)
            setKeyLog(prevLog => [...prevLog, { key: e.key, timestamp }]);
        }
    }

    const handleInputChange = (e) => {        
        // handle string clearing.
        var raw_string = e.target.value
        
        if(raw_string<=0){
            setInput("")
            setIsEmpty(true)
            return
        }

        // go over each element convert any english chars with avaialable mappings
        var new_string = ""
        for (let index = 0; index < raw_string.length; index++) {
            const element = raw_string[index];
            if(element in qwerty_ur){
                new_string += qwerty_ur[element]
            }
            else{
                new_string += element
            }
        }
        setIsEmpty(false)
        setInput(new_string)

        // error analysis only done when new char added.
        let new_trans = transposition_count;
        let new_omm = ommission_count;
        let new_sub = substitution_count;
        let new_add = addition_count;
        if(new_string.length>input.length){
            // transposition
            if (new_string.length>=2 && new_string.length<=targetText.length){
                let raw = new_string.slice(-2)
                let candidate = raw.split("").reverse().join("")
                let target = targetText.slice(new_string.length-2,new_string.length)
                if(candidate == target){
                    setErrorLog(prevLog => [...prevLog, { error_type: "transposition", input:raw, target:target}]);
                    new_trans +=1
                    setTrans(new_trans)
                }
            }
            // omission
            if (new_string.length<targetText.length && new_string[new_string.length-1] == targetText[new_string.length]){
                setErrorLog(prevLog => [...prevLog, { error_type: "omission", input:new_string[new_string.length-1], target:targetText[new_string.length-1]}]);
                new_omm+=1
                setOmm(new_omm)
            }
            // addition
            if (new_string.length>=3 && new_string.length<=targetText.length){
                let value = new_string[new_string.length-3] + new_string[new_string.length-2]
                let candidate = new_string[new_string.length-3] + new_string[new_string.length-1]
                let target = targetText.slice(new_string.length-3,new_string.length-1)
                if(value!== target && candidate == target){
                    setErrorLog(prevLog => [...prevLog, { error_type: "addidtion", input:new_string.slice(-3), target:target}]);
                    new_add+=1
                    setAdd(new_add)
                }
            }
            // substitution
            // build romanized target based on keyboard layout
            let roman_target = ""
            for (let index = 0; index < targetText.length; index++) {
                roman_target += ur_qwerty[targetText[index]]
            }
            // check sub erors
            if (roman_target[raw_string.length-1]!=" " && ADJACENCY[roman_target[raw_string.length-1]].includes(raw_string[raw_string.length-1])){
                setErrorLog(prevLog => [...prevLog, { error_type: "substitution", input:raw_string[raw_string.length-1], target:roman_target[raw_string.length-1]}]);
                new_sub+=1
                setSub(new_sub)
            }
        }

        // input complete send to server
        if(new_string.replace(/\s+/g, " ") == targetText.replace(/\s+/g, " ")){
            setEnd(true)
        }
    };

    // stimulus completed. Write to server and prepare for next
    useEffect(() => {
        if (end==true){
            const end_time = Date.now();
            const uid = localStorage.getItem("uid");
            try{
                axios.post(endpoint_live+"result", {
                    user: uid,
                    condition: condition,
                    stimulus: targetText,
                    start_time : startTime,
                    end_time: end_time,
                    log: keyLog,
                    error_log:errorLog,
                    transposition_count : transposition_count,
                    ommission_count : ommission_count,
                    substitution_count : substitution_count,
                    addition_count : addition_count,
                    wpm : (end_time-startTime) / targetText.split("").length
                }, {headers: {
                        "Content-Type": "application/json",
                    },
                })
            } catch (err) {
                console.error("Error submitting data:", err);
            }
            // reset for next stimulus
            setStartTime(null)
            setCurrentStim((prev) => prev + 1)
            setInput("")
            setIsEmpty(true)
            setKeyLog([])
            setErrorLog([])
            setEnd(false)
        }
    }, [end]);

    // Function for rendering the text input by a user. Provides highlighting.
    const renderText = () => {
        let result = [];
        
        // loop over each charachter
        for (let i = 0; i < input.length; i++){
            // highlight based on whether it is correct or incorrect
            if (input[i] === targetText[i]) {
                // correct
                result.push(
                    <span key={i} className=" bg-correct">
                        {input[i]}
                    </span>
                );
            }else if(input[i] == " "){
                // accounts for multiple space charachters
                result.push(
                    <span key={i} className=" bg-error">
                        &nbsp;
                    </span>
                );
            }else{
                // incorrect
                result.push(
                    <span key={i} className=" bg-error">
                        {input[i]}
                    </span>
                );
            }
        }
        return result 
    }

    // render remaining text
    const renderRemaining = () => {
        let result = [];
        if(input.length<targetText.length){
            result.push(
                <span key="remaining" className="text-deactive">{targetText.slice(input.length)}</span>
            );
        }
        return result 
    }

    return(
        <div className="p-4 flex flex-col items-center">

            {/* Stimulus Text */}
            <div className="text-4xl font-ur-sans relative cursor-text" onClick={() => inputRef.current.focus()}>
                {targetText}
            </div>

            {/* Rendered Input Field */}
            <div className="pt-7">
            <div className="text-4xl font-ur-sans relative cursor-text" onClick={() => inputRef.current.focus()}>
                <span>{renderText()}</span>
                {!isEmpty && (
                <span
                    className={`absolute w-[5px] h-[1.2em] bg-black z-20 transition-all duration-100 animate-[blink_0.7s_step-start_infinite] ${
                    isFocused ? "" : "hidden"
                    }`}
                />
                )}
                {renderRemaining()}
                {isEmpty && (
                <span
                    className={`absolute w-[5px] h-[1.2em] bg-black z-20 transition-all duration-100 animate-[blink_0.7s_step-start_infinite] ${
                    isFocused ? "" : "hidden"
                    }`}
                />
                )}
            </div>
            </div>

            {/* Hidden Input Field Both rendered options set focus on inputRef*/}
            <input
                ref={inputRef}
                type="text"
                className="absolute opacity-0 w-0 h-0"
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                onFocus={handleFocus}
                onBlur={() => setFocus(false)}
                value={input}
            />
        </div>
    )
}