import React from "react";
import axios from "axios";
import { useState, useRef, useEffect } from "react";

// API call to google translitarate. Used to power the IME
async function getTransliterations(text) {
    const url = `https://inputtools.google.com/request?itc=ur-t-i0-und&text=${encodeURIComponent(text)}&num=5`;

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

// Comparison function for chars that treates different spaces as the same
function compare_safe(text,target){
    if (text=== "\u00A0" && target === " "){
        return true;
    }else {
        return text === target;
    }
}

export default function InputIme({ id = -1, condition = "", targetText = "", setCounter }){
    const [input, setInput] = useState("");
    const [keyLog, setKeyLog] = useState([]);
    const [startTime, setStartTime] = useState(null);
    const [errorLog, setErrorLog] = useState([]);
    const [transposition_count, setTrans] = useState(0);
    const [ommission_count, setOmm] = useState(0);
    const [substitution_count, setSub] = useState(0);
    const [addition_count, setAdd] = useState(0);
    
    
    const [current_word, setCurrentWord] = useState("");
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [suggestions, setSuggestions] = useState([]);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const [position, setPosition] = useState({ top: 0, left: 0 });
    
    const lastWordRef = useRef(null);
    const inputAreaRef = useRef(null);
    const [isEmpty, setIsEmpty] = useState("");
    
    const inputRef = useRef(null);

    const [start, setStart] = useState(false);
    const [end, setEnd] = useState(false)
    
    // start timer
    const handleFocus = (e) =>{
        if (start === false){
            setStart(true);
            console.log("started")
        }
    }

    // unlike layout a majority of the ime logic is here at the key level.
    const handleKeyDown = (e) => {
        // cache time stamp
        timestamp = Date.now()
        // dont do anything if not started
        if (start === false){
            e.preventDefault();
            return;
        }else if (start=== true && startTime === null){
            setStartTime(timestamp);
        }

        // Log the key presses
        setKeyLog(prevLog => [...prevLog, { key: e.key, timestamp }]); 
        
        // navigate transliteration options
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
            // option Selected. Apply.
            let new_string = new_input + suggestions[selectedIndex]

            // error analysis only done when new char added.
            let new_trans = transposition_count;
            let new_omm = ommission_count;
            let new_add = addition_count;
            // transposition
            if (new_string.length>=2 && new_string.length<=targetText.length){
                let raw = new_string.slice(-2)
                let candidate = raw.split("").reverse().join("")
                let target = targetText.slice(new_string.length-2,new_string.length)
                console.log(raw)
                console.log(candidate)
                console.log(target)
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
                let candidate = new_string[new_string.length-3] + new_string[new_string.length-1]
                let target = targetText.slice(new_string.length-3,new_string.length-1)
                if(candidate == target){
                    setErrorLog(prevLog => [...prevLog, { error_type: "addidtion", input:new_string.slice(-3), target:target}]);
                    new_add+=1
                    setAdd(new_add)
                }
            }
            
            // apply the selected word
            setInput(new_string+" ");
            setShowSuggestions(false);
            e.preventDefault();
            setCurrentWord("")
        } else if (e.key === " " && showSuggestions === false){
            // handle spaces. For confirmed text.
            new_input = new_input + "\u00A0"
            setInput(new_input)
            e.preventDefault();
            setCurrentWord("")
        }else if (e.key === "Backspace" && showSuggestions===false){
            // handle charachter deleting for confirmed text
            new_input = new_input.slice(0,-1)
            setInput(new_input)
        }else if(e.key == "ArrowLeft" || e.key == "ArrowRight"){
            // ignore navigation
            e.preventDefault();
        }

        // handle empty string as input
        if(new_input.length<1){setIsEmpty(true)}
        else{setIsEmpty(false)}

        // handle text completion
        if(new_input.trim()==targetText){
            setEnd(true)
        }
    };

    // The input feild onyl deals with one token. The roman input
    const handleInputChange = (e) => {
        const raw_input = e.target.value
        const word = raw_input.trim();
        setCurrentWord(word)
        if(word.length>0){
            setShowSuggestions(true)
            getTransliterations(word).then(setSuggestions);
        }else{
            setShowSuggestions(false)
            setSuggestions([])
        }
    };

    // shows and hides drop down for transliteration suggestions
    useEffect(() => {
        if (isEmpty){
            const rect = inputAreaRef.current.getBoundingClientRect();
            setPosition({ top: rect.bottom + window.scrollY, left: rect.right + window.scrollX });
        }else if(lastWordRef.current) {
            const rect = lastWordRef.current.getBoundingClientRect();
            setPosition({ top: rect.bottom + window.scrollY, left: rect.left + window.scrollX });
        }
    }, [showSuggestions]);

    // stimulus completed. Write to server and prepare for next
    useEffect(() => {
        if (end==true){
            const end_time = Date.now();
            try{
                axios.post("http://127.0.0.1:8000/result", {
                    user: id,
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
            setCounter((prev) => prev + 1)
            setInput("")
            setKeyLog([])
            setErrorLog([])
            setEnd(false)
        }
    }, [end]);

    // render transliterated text
    const renderText = () => {
        let result = [];
        
        for (let i = 0; i < input.length; i++){
            const isLastWord = i === input.length - 1;
            if (compare_safe(input[i],targetText[i])) {
                result.push(
                    <span key={i} className="bg-correct">
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
                    <span key={i} className="bg-error">
                        {input[i]}
                    </span>
                );
            }
        }
        return result;
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
            <div ref = {inputAreaRef} className="text-4xl pt-7 font-ur-sans relative cursor-text" onClick={() => inputRef.current.focus()}>
                <span ref={lastWordRef}>{renderText()}</span>
                {renderRemaining()}
            </div>

            {/* Show Suggestions */}
            {showSuggestions && (
                <ul
                className="absolute text-xl bg-white border border-black shadow-md rounded p-1"
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
                    <li key={index} className={`font-ur-sans p-1 cursor-pointer ${
                        selectedIndex === index ? "bg-select text-black" : ""
                    }`}>
                    {suggestion}
                    </li>
                ))}
                </ul>
            )}

            {/* Hidden Input Field Both rendered options set focus on inputRef*/}
            <input
                ref={inputRef}
                type="text"
                className="absolute opacity-0 w-0 h-0"
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                onFocus={handleFocus}
                value={current_word}
            />
        </div>
    )
}