import React from "react";
import ButtonStartSCondition from "../../components/ButtonStartCondition";

export default function BaselineInst() {

    return (
        <div className={`bg-white p-6 px-[10vw] flex-col space-y-3 justify-center text-black`}>
            {/* Page title */}
            <div>
                <h1 className="text-7xl font-black  ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Instructions</h3>
            </div>
            {/* Subtitle */}
            <h3 className="px-3 bg-black text-white text-2xl">
                Instructions on how to use the interface and baseline measurement.
            </h3>
            {/* Instructions */}
            <p>
               Over the course of this experiment we will be asking you to enter text using three different text entry options (CRULP, Windows, IME). We will be referring to these as conditions. 
               All of these will use a similar interface as the one shown below. When you are ready to start a condition, click on the text inside the box. This will start the condition which 
               is indicated by the change in background color and appearance of the cursor.
            </p>
            <img src="/instructions/start.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            
            <hr></hr>
            <p>
                As you type, correct input will be highlighted in <span className="bg-correct border-1">green</span>, 
                and any mistakes will show up highlighted in <span className="bg-error border-1">red</span>. 
            </p>
            <img src="/instructions/highlighting.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>
                Note that if you click outside away from the text it may deselect the input field. This will be indicated by the cursor going away as seen below. To reselect the input field please click on the text again.
            </p>
            <img src="/instructions/deselect.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>
                To begin with, we would like to get an idea of how fast you type. Therefore the following condition serves as a baseline measurement of your typing speed. You will be asked to type a set of pseudo sentences. 
                Pseudo sentences are sentences that use words which sound similar to English but have no actual meaning. The first two sentences are just to help you practice using the interface and will not count towards 
                your typing speed measurement. Whenever you feel ready please click on the button to navigate to the condition.
            </p>
            <ButtonStartSCondition target={"/baseline"}/>
        </div>
    );
}