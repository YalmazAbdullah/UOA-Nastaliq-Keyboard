import React from "react";
import { useState, useRef, useEffect } from "react";

const CRULP = {
    "~":" ً","!":"1","@":"2","#":"3","$":"4","%":"5","^":"6","&":"7","*":"8","(":"9",")":"0","_":"_","+":"+",
    "Q":" ْ","W":" ّ","E":" ٰ","R":"ڑ","T":"ٹ","Y":" َ","U":"ئ","I":" ِ","O":"ۃ","P":" ُ","{":"}","}":"{","|":"|",
    "A":"آ","S":"ص","D":"ڈ","G":"غ","H":"ھ","J":"ض","K":"خ","L":"@", ":":":", "\"":"\"",
    "Z":"ذ","X":"ژ","C":"ث","V":"ظ","N":"ں","M":" ٘","<":"٫",">":".","?":"؟",
    
    "1":"۱","2":"۲","3":"۳","4":"۴","5":"۵","6":"۶","7":"۷","8":"۸","9":"۹","0":"۰","-":"-","=":"=",
    "q":"ق","w":"و","e":"ع","r":"ر","t":"ت","y":"ے","u":"ء","i":"ی","o":"ہ","p":"پ","[":"]","]":"[", "\\":"\\",
    "a":"ا","s":"س","d":"د","f":"ف","g":"گ","h":"ح","j":"ج","k":"ک","l":"ل",";":"؛","'":"'",
    "z":"ز","x":"ش","c":"چ","v":"ط","b":"ب","n":"ن","m":"م",",":"،",".":"۔","/":"/",
    
    " ":" "
}

export default function KeyboardCrulp(){
    const targetText = "یہ کہانی دس بار سون لی۔";
   
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
        if(raw_string<=0){
            setInput("")
            return
        }

        var new_string = ""
        for (let index = 0; index < raw_string.length; index++) {
            const element = raw_string[index];
            if(element in CRULP){
                new_string += CRULP[element]
            }
            else{
                new_string += element
            }
        }
        setInput(new_string)
    };


    const renderText = () => {
        let result = [];
        
        for (let i = 0; i < input.length; i++){
            if (input[i] === targetText[i]) {
                result.push(
                    <span key={i} className="text-white bg-green-500">
                        {input[i]}
                    </span>
                );
            }else{
                result.push(
                    <span key={i} className="text-white bg-red-600">
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