import React, { useState, useEffect } from "react";

export default function KeyboardVisNoInteract({layout}) {
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
    <div className="flex flex-col items-center">
      {layout.map((row, rowIndex) => (
        <div key={rowIndex} className="flex justify-center space-x-2 mb-2 py-1">
          {row.map((key) => (
            <div
              key={key.en_upper}
              className={`w-16 h-16 border-2 border-black flex items-center justify-around shadow-[-0.2rem_0.2rem_rgba(0,0,0,1)] bg-white text-black`}
            >
                <div className=" flex flex-col">
                    {/* English Upper */}
                    <span className="text-gray-dark text-lg">{key.en_upper}</span>
                    {/* English Lower */}
                    <span className="text-gray-dark text-lg">{key.en_lower}</span>
                </div>
                <div className=" flex flex-col items-center">
                    {/* Urdu Upper */}
                    <span className="text-black font-semibold text-lg font-ur-sans">{key.ur_upper}</span>
                    {/* Urdu Lower */}
                    <span className="text-black font-semibold text-lg font-ur-sans">{key.ur_lower}</span>
                </div>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
