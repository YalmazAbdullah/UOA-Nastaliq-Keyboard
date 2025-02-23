import { useState, useRef, useEffect } from "react";

export default function KeyboardImeNaive() {
  const [input, setInput] = useState("");
  const [currentWord, setCurrentWord] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [caretPosition, setCaretPosition] = useState({ top: 0, left: 0 });

  const inputRef = useRef(null);

  const suggestions = ["ورنور", "さようなら", "ありがとう", "すごい", "日本語"]; // Dummy suggestions

  useEffect(() => {
    if (inputRef.current) {
      const rect = inputRef.current.getBoundingClientRect();
      const caretX = rect.left + (inputRef.current.selectionEnd || 0) * 8; // Approximate caret X
      setCaretPosition({
        top: rect.top - 30, // Position above text
        left: caretX,
      });
    }
  }, [input]);

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setInput(newValue);
    
    const words = newValue.split(" ");
    const lastWord = words[words.length - 1]; // Get the word currently being typed
    setCurrentWord(lastWord);
    
    setShowSuggestions(lastWord.length > 0); // Show suggestions only if there's a word
    setSelectedIndex(-1);
  };

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      setSelectedIndex((prev) =>
        prev < suggestions.length - 1 ? prev + 1 : prev
      );
    } else if (e.key === "ArrowUp") {
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : prev));
    } else if (e.key === "Enter" && selectedIndex >= 0) {
      const words = input.split(" ");
      words[words.length - 1] = suggestions[selectedIndex]; // Replace current word
      setInput(words.join(" "));
      setCurrentWord(""); // Clear highlight
      setShowSuggestions(false);
      e.preventDefault();
    }
  };

  return (
    <div className="relative w-64">
      <div className="w-full p-2 border border-gray-300 rounded bg-white text-gray-900">
        {/* Display input text with highlighted current word */}
        {input.split(" ").map((word, index, arr) => (
          <span
            key={index}
            className={
              index === arr.length - 1 ? "bg-yellow-200 px-1 rounded" : ""
            }
          >
            {word}
            {index < arr.length - 1 && " "}
          </span>
        ))}
      </div>
      <input
        ref={inputRef}
        type="text"
        value={input}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        className="absolute top-0 left-0 w-full p-2 opacity-0"
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
              onMouseDown={() => {
                const words = input.split(" ");
                words[words.length - 1] = suggestion;
                setInput(words.join(" "));
                setCurrentWord("");
                setShowSuggestions(false);
              }}
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
