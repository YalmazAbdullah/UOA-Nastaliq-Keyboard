import React from "react";
import ButtonStartSCondition from "../../components/ButtonStartCondition";

export default function ImeInst() {

    return (
        <div className={`bg-white p-6 px-[10vw] flex-col space-y-3 justify-center text-black`}>
            {/* Page title */}
            <div>
                <h1 className="text-7xl font-black  ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">IME Instructions</h3>
            </div>
            {/* Subtitle */}
            <h3 className="px-3 bg-black text-white text-2xl">
                Instructions on how to use the IME Urdu Input tool.
            </h3>
            {/* Instructions */}
            <p>
                In this condition we will be evaluating the Input Method Editor (IME) tool for Urdu. This tool takes in Roman Urdu as input and converts it to Urdu script. 
                For example, if you start typing "salam" then the system will show you a drop down menu with potential Urdu transliterations such 
                as <span className="text-lg font-ur-sans">"سلام"</span> and <span className="text-lg font-ur-sans">"سلم"</span>. This is demonstrated in the gif below.
            </p>
            <img src="/instructions/ime1.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>
                You can select between the different options by using the up and down arrow keys. To confirm your selection press <b>Enter</b> or <b>Space</b>.
            </p>
            <img src="/instructions/ime2.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>
                The following demonstrations shows how you could type out <span className="text-lg font-ur-sans">"یہ ایک"</span>
            </p>
            <img src="/instructions/ime3.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>In the following condition we will ask you to type a number of sentences in Urdu using this tool and interface. Whenever you feel ready please click on the button to navigate to the condition.</p>
            <ButtonStartSCondition target={"/ime"}/>
        </div>
    );
}