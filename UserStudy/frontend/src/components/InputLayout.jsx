import React from "react";
import { useState, useRef } from "react";
import {ADJACENCY} from "../assets/error_data"

export default function InputLayout({ qwerty_ur, ur_qwerty, targetText, setCounter }){
   
    const [input, setInput] = useState("");
    const [roman_input, setRoman] = useState("")
    const [keyLog, setKeyLog] = useState([]);
    const [errorLog, setErrorLog] = useState([]);
    const inputRef = useRef(null);

    const handleKeyDown = (e) => {
        const timestamp = Date.now();
        setKeyLog(prevLog => [...prevLog, { key: e.key, timestamp }]); // Log the key presses
    };

    const handleInputChange = (e) => {
        var raw_string = e.target.value
        if(raw_string<=0){
            setInput("")
            return
        }

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

        // error analysis only done when new char added.
        if(new_string.length>input.length){
            
            // transposition
            if (new_string.length>=2 && new_string.length<=targetText.length){
                let raw = new_string.slice(-2)
                let candidate = raw.split("").reverse().join("")
                let target = targetText.slice(new_string.length-2,new_string.length)
                if(candidate == target){
                    setErrorLog(prevLog => [...prevLog, { error_type: "transposition", input:raw, target:target}]);
                }
            }

            // omission
            if (new_string.length<targetText.length && new_string[new_string.length-1] == targetText[new_string.length]){
                setErrorLog(prevLog => [...prevLog, { error_type: "omission", input:new_string[new_string.length-1], target:targetText[new_string.length-1]}]);
            }

            // addition
            if (new_string.length>=3 && new_string.length<=targetText.length){
                let candidate = new_string[new_string.length-3] + new_string[new_string.length-1]
                let target = targetText.slice(new_string.length-3,new_string.length-1)
                if(candidate == target){
                    setErrorLog(prevLog => [...prevLog, { error_type: "addidtion", input:new_string.slice(-3), target:target}]);
                }
            }

            // substitution
            // build romanized target based on keyboard layout
            let roman_target = ""
            for (let index = 0; index < targetText.length; index++) {
                roman_target += ur_qwerty[targetText[index]]
            }
            if (roman_target[raw_string.length-1]!=" " && ADJACENCY[roman_target[raw_string.length-1]].includes(raw_string[raw_string.length-1])){
                setErrorLog(prevLog => [...prevLog, { error_type: "substitution", input:raw_string[raw_string.length-1], target:roman_target[raw_string.length-1]}]);
            }
        }

        setInput(new_string)

        if(new_string===targetText){
            setCounter((prev) => prev + 1)
            setInput("")
            setKeyLog([])
            setErrorLog([])
        }
    };


    const renderText = () => {
        let result = [];
        
        for (let i = 0; i < input.length; i++){
            if (input[i] === targetText[i]) {
                result.push(
                    <span key={i} className=" bg-correct">
                         {input[i]}
                     </span>
                 );
             }else if(input[i] == " "){
                 result.push(
                     <span key={i} className=" bg-error">
                         &nbsp;
                     </span>
                 );
             }else{
                 result.push(
                     <span key={i} className=" bg-error">
                         {input[i]}
                     </span>
                 );
             }
        }

        // add the remaining text
        if(input.length<targetText.length){
            result.push(
                <span key="remaining" className="text-deactive">{targetText.slice(input.length)}</span>
            );
        }

        return result;
    }

    return(
        <div className="p-4 flex flex-col items-center">
            <div className="text-4xl font-ur-sans relative cursor-text" onClick={() => inputRef.current.focus()}>
                {targetText}
            </div>

            <div className="text-4xl pt-7 font-ur-sans relative cursor-text" onClick={() => inputRef.current.focus()}>
                {renderText()}
            </div>

            {/* Hidden Input Field */}
            <input
                ref={inputRef}
                type="text"
                className="absolute opacity-0 w-0 h-0"
                onKeyDown={handleKeyDown}
                onChange={handleInputChange}
                value={input}
                autoFocus
            />
        </div>
    )
}