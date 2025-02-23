import React from "react";
import { useState, useRef, useEffect } from "react";

const WINDOWS = {
    "~":"~", "!":"!", "@":"@", "#":"#", "$":"$", "%":"٪", "^":"^", "&":" ۖ", "*":"٭", "(":")", ")":"(", "_":"_", "+":"+",
    "Q":"ظ","W":"ض","E":"ذ","R":"ڈ","T":"ث","Y":" ّ","U":"ۃ","I":"ـ","O":"چ","P":"خ","{":"}","}":"{","|":"|",
    "A":"ژ","S":"ز","D":"ڑ","F":"ں","G":"ۂ","H":"ء","J":"آ","K":"گ","L":"ي", ":":":", "\"":"\"",
    "C":"ۓ","B":"ؤ","N":"ئ","<":">",">":"<","?":"؟",
    
    "`":"`","1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","7":"7","8":"8","9":"9","0":"0","-":"-","=":"=",
    "q":"ط","w":"ص","e":"ھ","r":"د","t":"ٹ","y":"پ","u":"ت","i":"ب","o":"ج","p":"ح","[":"]","]":"[", "\\":"\\",
    "a":"م","s":"و","d":"ر","f":"ن","g":"ل","h":"ہ","j":"ا","k":"ک","l":"ی",";":"؛","'":"'",
    "z":"ق","x":"ف","c":"ے","v":"س","b":"ش","n":"غ","m":"ع",",":"،",".":"۔","/":"/",
    
    " ":" "
}

export default function KeyboardWindows(){
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
            if(element in WINDOWS){
                new_string += WINDOWS[element]
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