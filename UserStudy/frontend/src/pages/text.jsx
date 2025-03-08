import React, { useEffect, useRef, useState } from "react";

export default function TextWithCaret() {
  const textContainerRef = useRef(null);
  const caretRef = useRef(null);
  const [text, setText] = useState("Hello, world");

  useEffect(() => {
    updateCaretPosition();
  }, [text]);

  const updateCaretPosition = () => {
    if (!textContainerRef.current || !caretRef.current) return;

    const spans = textContainerRef.current.querySelectorAll("span");
    if (spans.length === 0) return;

    const lastSpan = spans[spans.length - 1];
    const rect = lastSpan.getBoundingClientRect();
    const containerRect = textContainerRef.current.getBoundingClientRect();

    caretRef.current.style.left = `${rect.right - containerRect.left}px`;
    caretRef.current.style.top = `${rect.top - containerRect.top}px`;
  };

  return (
    <div className="relative inline-block p-4">
      {/* Text Container */}
      <div ref={textContainerRef} className="relative inline-block text-2xl font-mono mx-2">
        {text.split("").map((char, index) => (
          <span key={index}>{char}</span>
        ))}
        {/* Caret */}
        <div
            ref={caretRef}
            className="absolute w-[2px] h-[1em] bg-black z-20 transition-all duration-100"
        />
      </div>


      {/* Button to update text */}
      <button onClick={() => setText(text + " ")} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
        Add Text
      </button>
    </div>
  );
}
