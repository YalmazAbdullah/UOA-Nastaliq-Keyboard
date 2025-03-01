import React from "react";
import { useState, useRef, useEffect } from "react";

async function getTransliterations(text, langCode = "ur") {
    const url = `https://inputtools.google.com/request?itc=${langCode}-t-i0-und&text=${encodeURIComponent(text)}`;
    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data[0] === "SUCCESS") {
            return data[1][0][1]; // List of transliterations
        } else {
            throw new Error("Failed to fetch transliterations");
        }

    } catch (error) {
        console.error("Error:", error);
        return null;
    }
}

function compare_safe(text,target){
    if (text=== "\u00A0" && target === " "){
        return true;
    }else {
        return text === target;
    }
}

export default function InputIme({ setCounter }){
    const targetText = "یہ کہانی دس بار سو لی";
   
    const [keyLog, setKeyLog] = useState([]);
    
    const inputRef = useRef(null);
    const [input, setInput] = useState("");

    const [current_word, setCurrentWord] = useState("");
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [suggestions, setSuggestions] = useState([]);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const [position, setPosition] = useState({ top: 0, left: 0 });

    const lastWordRef = useRef(null);
    const inputAreaRef = useRef(null);
    const [isEmpty, setIsEmpty] = useState("");

    const handleKeyDown = (e) => {
        const timestamp = Date.now();
        setKeyLog(prevLog => [...prevLog, { key: e.key, timestamp }]); // Log the key presses
        
        let new_input = input
        if (e.key === "ArrowDown") {
            setSelectedIndex((prev) =>
                prev < suggestions.length - 1 ? prev + 1 : prev
            );
        } else if (e.key === "ArrowUp") {
            setSelectedIndex((prev) => 
                prev > 0 ? prev - 1 : prev
            );
        } else if (e.key === "Enter" || (e.key === " " && showSuggestions === true)) {
            new_input = new_input + suggestions[selectedIndex] +" "
            setInput(new_input);
            setShowSuggestions(false);
            e.preventDefault();
            setCurrentWord("")
        } else if (e.key === " " && showSuggestions === false){
            new_input = new_input + "\u00A0"
            setInput(new_input)
            e.preventDefault();
            setCurrentWord("")
        }else if (e.key === "Backspace" && showSuggestions===false){
            new_input = new_input.slice(0,-1)
            setInput(new_input)
        }else if(e.key == "ArrowLeft" || e.key == "ArrowRight"){
            e.preventDefault();
        }

        if(new_input.length<1){setIsEmpty(true)}
        else{setIsEmpty(false)}

        if(new_input.trim()==targetText){
            console.log(new_input)
            // TODO: change this to also account for number of stimuli
            setCounter(21)
        }
    };

    const handleInputChange = (e) => {
        const raw_input = e.target.value
        const word = raw_input.trim();
        setCurrentWord(word)
        if(word.length>0){
            setShowSuggestions(true)
            getTransliterations(word, "ur").then(setSuggestions);
        }else{
            setShowSuggestions(false)
            setSuggestions([])
        }
    };

    useEffect(() => {
        if (isEmpty){
            const rect = inputAreaRef.current.getBoundingClientRect();
            setPosition({ top: rect.bottom + window.scrollY, left: rect.right + window.scrollX });
        }else if(lastWordRef.current) {
            const rect = lastWordRef.current.getBoundingClientRect();
            setPosition({ top: rect.bottom + window.scrollY, left: rect.left + window.scrollX });
        }
    }, [showSuggestions]);

    const renderText = () => {
        let result = [];
        
        for (let i = 0; i < input.length; i++){
            const isLastWord = i === input.length - 1;
            if (compare_safe(input[i],targetText[i])) {
                result.push(
                    <span key={i} className="text-white bg-green-500">
                        {input[i]}
                    </span>
                );
            }
            else{
                result.push(
                    <span key={i} className="text-white bg-red-600">
                        {input[i]}
                    </span>
                );
            }
        }
        return result;
    }

    const renderRemaining = () => {
        let result = [];
        if(input.length<targetText.length){
            result.push(
                <span key="remaining" className="text-gray-500">{targetText.slice(input.length)}</span>
            );
        }
        return result 
    }

    return(
        <div className="p-4 flex flex-col items-center">
            <div className="text-2xl font-mono relative cursor-text" onClick={() => inputRef.current.focus()}>
                {targetText}
            </div>

            <div ref = {inputAreaRef} className="text-2xl font-mono relative cursor-text" onClick={() => inputRef.current.focus()}>
                <span ref={lastWordRef}>{renderText()}</span>
                {renderRemaining()}
            </div>

            {/* Hidden Input Field */}
            <input
                ref={inputRef}
                type="text"
                className="absolute opacity-0 w-0 h-0"
                onKeyDown={handleKeyDown}
                onChange={handleInputChange}
                value={current_word}
                autoFocus
            />

            {/* Show Suggestions */}
            {showSuggestions && (
                <ul
                className="absolute bg-white border border-gray-300 shadow-md rounded p-1"
                style={{
                    position: "absolute",
                    top: `${position.top}px`,
                    left: `${position.left}px`,
                    transform: "translateX(-100%)",
                }}
                >
                <li key="current">
                    {current_word}
                </li>
                <hr></hr>
                {suggestions.map((suggestion, index) => (
                    <li key={index} className={`p-1 cursor-pointer ${
                        selectedIndex === index ? "bg-blue-500 text-white" : ""
                    }`}>
                    {suggestion}
                    </li>
                ))}
                </ul>
            )}
        </div>
    )
}