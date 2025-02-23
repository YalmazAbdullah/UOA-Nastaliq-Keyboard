 import React from "react";
 import { useState, useRef, useEffect } from "react";


export default function KeyboardTest(){
    const targetText = "This is a hello world test.";
    
    const [input, setInput] = useState("");
    const [keyLog, setKeyLog] = useState([]);
    const inputRef = useRef(null);

    const handleKeyDown = (e) => {
        const timestamp = Date.now();
        setKeyLog(prevLog => [...prevLog, { key: e.key, timestamp }]); // Log the key presses
        console.log(keyLog)
    };

    const handleInputChange = (e) => {
        var raw_string = e.target.value
        setInput(raw_string)
    };


    const renderText = () => {
        let result = [];
        
        for (let i = 0; i < input.length; i++){
            if (input[i] === targetText[i]) {
                result.push(
                    <span key={i} className="text-green-500">
                        {input[i]}
                    </span>
                );
            }

            else if (i<targetText.length && targetText[i]!==" "){
                result.push(
                    <span key={i} className="text-red-600">
                        {input[i]}
                    </span>
                );
            }

            else{
                result.push(
                    <span key={i} className="text-red-900">
                        {input[i]}
                    </span>
                );
            }
        }

        // add the remaining text
        if(input.length<targetText.length){
            result.push(
                <span key="remaining" className="text-gray-500">{targetText.slice(input.length)}</span>
            );
        }

        return result;
    }

    return(
        <div className="p-4 flex flex-col items-center">
            <div className="text-2xl font-mono relative cursor-text" onClick={() => inputRef.current.focus()}>
                {targetText}
            </div>

            <div className="text-2xl font-mono relative cursor-text" onClick={() => inputRef.current.focus()}>
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