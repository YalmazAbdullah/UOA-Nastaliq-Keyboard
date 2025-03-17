import React, { useEffect, useRef, useState } from "react";
import {Reorder} from "framer-motion"
import KeyboardVisNoInteract from "../components/KeyboardVisNoInteract";
import {QWERTY_LAYOUT, WINDOWS_LAYOUT, CRULP_LAYOUT} from "../assets/layouts"

export default function TextWithCaret() {
  const [boards,setBoards] = useState([
    {id:"CRULP", text:"phonetic keybaord", body:<KeyboardVisNoInteract layout={CRULP_LAYOUT}/>},
    {id:"IME", text:"roman text input",  body:<KeyboardVisNoInteract layout={QWERTY_LAYOUT}/>},
    {id:"WINDOWS", text:"frequency keybaord", body:<KeyboardVisNoInteract layout={WINDOWS_LAYOUT}/>},
  ]);

  const reorderBoards = (e) =>{
    setBoards(e);
    console.log(e)
  }

  return (
    <>
    <Reorder.Group values={boards} onReorder={reorderBoards}>
    {boards.map((board)=>(
      <Reorder.Item value={board} key={board.id} _dragX={false} className="p-10 m-10 bg-gray border-3 rounded-md">
      {board.body}
      </Reorder.Item>
    ))}
    </Reorder.Group>
    </>
  );
}
