import React from "react";
import { useState, useRef, useEffect } from "react";

function isEnglish(str) {
    const standardKeyboardRegex = /^[\x20-\x7E]*$/;
    return standardKeyboardRegex.test(str);
}

export default function KeyboardIme(){
    const targetText = "یہ کہانی دس بار۔";
   
    const [input, setInput] = useState("");
    const [keyLog, setKeyLog] = useState([]);
    const inputRef = useRef(null);

    const [currentWord, setCurrentWord] = useState("");
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const [caretPosition, setCaretPosition] = useState({ top: 0, left: 0 });

    const suggestions = ["یہ ", "さようなら", "ありがとう", "すごい", "日本語"];

    useEffect(() => {
        if (inputRef.current) {
            const rect = inputRef.current.getBoundingClientRect();
            setCaretPosition({
            top: rect.top + 60, // Position above text
            left: rect.left,
            });
        }
        }, [input]
    );

    const handleKeyDown = (e) => {
        // Log all input for analysis
        const timestamp = Date.now();
        setKeyLog(prevLog => [...prevLog, { key: e.key, timestamp }]);

        // Handle navigation of suggestion menu.
        if (e.key === "ArrowDown") {
            setSelectedIndex((prev) =>
                prev < suggestions.length - 1 ? prev + 1 : prev
            );
        } else if (e.key === "ArrowUp") {
            setSelectedIndex((prev) => 
                prev > 0 ? prev - 1 : prev
            );
        } else if (e.key === "Enter") {
            const words = input.split(" ");
            words[words.length - 1] = suggestions[selectedIndex]; // Replace current word
            console.log(words)
            setInput(words.join(" "));
            setShowSuggestions(false);
            e.preventDefault();
            setCurrentWord("")
        } 
   };

   const handleInputChange = (e) => {
        var raw_string = e.target.value
        

        const words = raw_string.split(" ");
        const lastWord = words[words.length - 1]; // Get the word currently being typed
        setCurrentWord(lastWord);
        const remaining_input = words.slice(0,words.length-1).join(" ")
        console.log(words)
        console.log(lastWord)
        console.log(remaining_input)
        setInput(remaining_input)

        setShowSuggestions(lastWord.length > 0); // Show suggestions only if there's a word
        setSelectedIndex(0);
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
           
            {showSuggestions && (
                <ul
                className="absolute bg-white border border-gray-300 shadow-md rounded p-1"
                style={{
                    position: "absolute",
                    top: caretPosition.top,
                    left: caretPosition.left,
                }}
                >
                {suggestions.map((suggestion, index) => (
                    <li
                    key={index}
                    className={`p-1 cursor-pointer ${
                        selectedIndex === index ? "bg-blue-500 text-white" : ""
                    }`}
                    >
                    {suggestion}
                    </li>
                ))}
                </ul>
            )}
       </div>
   )
}