import React from "react";
import ButtonStartSCondition from "../../components/ButtonStartCondition";

export default function WindowsInst() {

    return (
        <div className={`bg-white p-6 px-[10vw] flex-col space-y-3 justify-center text-black`}>
            {/* Page title */}
            <div>
                <h1 className="text-7xl font-black  ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">WINDOWS Instructions</h3>
            </div>
            {/* Subtitle */}
            <h3 className="px-3 bg-black text-white text-2xl">
                Instructions on how to use the WINDOWS Urdu Layout keyboard.
            </h3>
            {/* Instructions */}
            <p>
                In this condition we will be evaluating the WINDOWS keyboard layout. This is a frequency based keyboard layout, meaning that the most commonly used Urdu letters 
                are mapped to the most easily accessible keys. For example <span className="text-lg font-ur-sans">"ن"</span> is mapped to "f" because <span className="text-lg font-ur-sans">"ن"</span> is
                one of the most frequently occurring letters in Urdu and "f" is one of the most easily accessible keys on the keyboard. This is demonstrated in the gif below.
            </p>
            <img src="/instructions/windows1.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>
                Less commonly occurring letters are mapped to the uppercase keys. For example, <span className="text-lg font-ur-sans">"ں"</span> can by typed by entering the uppercase uppercase "F".
            </p>
            <img src="/instructions/windows2.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>
                Therefore to enter <span className="text-lg font-ur-sans">"یہ ایک"</span>, you must press the following sequence of keys "l", "h", "space", "j", "l", "k". This is demonstrated below.
            </p>
            <img src="/instructions/windows3.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>In the following condition we will ask you to type a number of sentences in Urdu using this keyboard and interface. Whenever you feel ready please click on the button to navigate to the condition.</p>
            <ButtonStartSCondition target={"/windows"}/>
        </div>
    );
}