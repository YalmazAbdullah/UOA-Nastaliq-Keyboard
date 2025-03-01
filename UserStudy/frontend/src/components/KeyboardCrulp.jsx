import React, { useState, useEffect } from "react";

const CRULP_LAYOUT = [
[ {en_upper : "~", ur_upper:" ً", en_lower: "`",  ur_lower:" ً"}, 
{en_upper : "!", ur_upper:"1", en_lower: "1",  ur_lower:"۱"}, 
{en_upper : "@", ur_upper:"2", en_lower: "2",  ur_lower:"۲"},
{en_upper : "#", ur_upper:"3", en_lower: "3",  ur_lower:"۳"},
{en_upper : "$", ur_upper:"4", en_lower: "4",  ur_lower:"۴"},
{en_upper : "%", ur_upper:"5", en_lower: "5",  ur_lower:"۵"},
{en_upper : "^", ur_upper:"6", en_lower: "6",  ur_lower:"۶"},
{en_upper : "&", ur_upper:"7", en_lower: "7",  ur_lower:"۷"},
{en_upper : "*", ur_upper:"8", en_lower: "8",  ur_lower:"۸"},
{en_upper : "(", ur_upper:"9", en_lower: "9",  ur_lower:"۹"},
{en_upper : ")", ur_upper:"0", en_lower: "0",  ur_lower:"۰"},
{en_upper : "_", ur_upper:"_", en_lower: "-",  ur_lower:"-"},
{en_upper : "+", ur_upper:"+", en_lower: "=",  ur_lower:"="}],

[ {en_upper : "Q", ur_upper:" ْ", en_lower: "q",  ur_lower:"ق"}, 
{en_upper : "W", ur_upper:" ّ", en_lower: "w",  ur_lower:"و"}, 
{en_upper : "E", ur_upper:" ٰ", en_lower: "e",  ur_lower:"ع"},
{en_upper : "R", ur_upper:"ڑ", en_lower: "r",  ur_lower:"ر"},
{en_upper : "T", ur_upper:"ٹ", en_lower: "t",  ur_lower:"ت"},
{en_upper : "Y", ur_upper:" َ", en_lower: "y",  ur_lower:"ے"},
{en_upper : "U", ur_upper:"ئ", en_lower: "u",  ur_lower:"ء"},
{en_upper : "I", ur_upper:" ِ", en_lower: "i",  ur_lower:"ی"},
{en_upper : "O", ur_upper:"ۃ", en_lower: "o",  ur_lower:"ہ"},
{en_upper : "P", ur_upper:" ُ", en_lower: "p",  ur_lower:"پ"},
{en_upper : "{", ur_upper:"}", en_lower: "[",  ur_lower:"]"},
{en_upper : "}", ur_upper:"{", en_lower: "]",  ur_lower:"["},
{en_upper : "|", ur_upper:"|", en_lower: "\\",  ur_lower:"\\"}],

[ {en_upper : "A", ur_upper:"آ", en_lower: "a",  ur_lower:"ا"}, 
{en_upper : "S", ur_upper:"ص", en_lower: "s",  ur_lower:"س"}, 
{en_upper : "D", ur_upper:"ڈ", en_lower: "d",  ur_lower:"د"},
{en_upper : "F", ur_upper:"ف", en_lower: "f",  ur_lower:"ف"},
{en_upper : "G", ur_upper:"غ", en_lower: "g",  ur_lower:"گ"},
{en_upper : "H", ur_upper:"ھ", en_lower: "h",  ur_lower:"ح"},
{en_upper : "J", ur_upper:"ض", en_lower: "j",  ur_lower:"ج"},
{en_upper : "K", ur_upper:"خ", en_lower: "k",  ur_lower:"ک"},
{en_upper : "L", ur_upper:"@", en_lower: "l",  ur_lower:"ل"},
{en_upper : ":", ur_upper:":", en_lower: ";",  ur_lower:"؛"},
{en_upper : "\"", ur_upper:"\"", en_lower: "\'",  ur_lower:"\'"}],

[ {en_upper : "Z", ur_upper:"ذ", en_lower: "z",  ur_lower:"ز"}, 
{en_upper : "X", ur_upper:"ژ", en_lower: "x",  ur_lower:"ش"}, 
{en_upper : "C", ur_upper:"ث", en_lower: "c",  ur_lower:"چ"},
{en_upper : "V", ur_upper:"ظ", en_lower: "v",  ur_lower:"ط"},
{en_upper : "B", ur_upper:"غ", en_lower: "b",  ur_lower:"ب"},
{en_upper : "N", ur_upper:"ں", en_lower: "n",  ur_lower:"ن"},
{en_upper : "M", ur_upper:"٘ ", en_lower: "m",  ur_lower:"م"},
{en_upper : "<", ur_upper:"٫", en_lower: ",",  ur_lower:"،"},
{en_upper : ">", ur_upper:".", en_lower: ".",  ur_lower:"۔"},
{en_upper : "?", ur_upper:"؟", en_lower: "/",  ur_lower:"/"}],
];


export default function KeyboardCrulp() {
  const [pressedKeys, setPressedKeys] = useState(new Set());

  useEffect(() => {
    const handleKeyDown = (e) => {
      setPressedKeys((prev) => new Set(prev).add(e.key));
    };

    const handleKeyUp = (e) => {
      setPressedKeys((prev) => {
        const newSet = new Set(prev);
        newSet.delete(e.key);
        //@TODO: fix the key jam that happens if shift let go first.
        newSet.delete(e.key.toUpperCase());
        return newSet;
      });
    };

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  return (
    <div className="flex flex-col items-center p-4">
      {CRULP_LAYOUT.map((row, rowIndex) => (
        <div key={rowIndex} className="flex justify-center space-x-2 mb-2">
          {row.map((key) => (
            <div
              key={key.en_upper}
              className={`w-16 h-16 p-10 border-2 border-black flex items-center justify-center shadow-[-0.2rem_0.2rem_rgba(0,0,0,1)]
                          ${pressedKeys.has(key.en_upper) || pressedKeys.has(key.en_lower) ? "bg-blue-500 text-white" : "bg-gray-200"}`}
            >
                <div className=" flex flex-col p-3">
                    {/* English Upper */}
                    <span className="text-gray-600 text-lg">{key.en_upper}</span>
                    {/* English Lower */}
                    <span className="text-gray-600 text-lg">{key.en_lower}</span>
                </div>
                <div className=" flex flex-col items-center pe-2 p-3">
                    {/* Urdu Upper */}
                    <span className="text-black text-lg font-ur-sans">{key.ur_upper}</span>
                    {/* Urdu Lower */}
                    <span className="text-black text-lg font-ur-sans">{key.ur_lower}</span>
                </div>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
