import React from "react";
import ButtonStartSCondition from "../../components/ButtonStartCondition";

export default function CrulpInst() {

    return (
        <div className={`bg-white p-6 px-[10vw] flex-col space-y-3 justify-center text-black`}>
            {/* Page title */}
            <div>
                <h1 className="text-7xl font-black  ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">CRULP Instructions</h3>
            </div>
            {/* Subtitle */}
            <h3 className="px-3 bg-black text-white text-2xl">
                Instructions on how to use the CRULP Urdu Layout keyboard.
            </h3>
            {/* Instructions */}
            <p>
                In this condition we will be evaluating the CRULP keyboard layout. This is a phonetic keyboard layout, meaning that the Urdu letters 
                are mapped to the most similar sounding English keys. For example <span className="text-lg font-ur-sans">"د"</span> is mapped to "d" because they sound similar. 
                This is demonstrated in the gif below.
            </p>
            <img src="/instructions/crulp1.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>
                Some English keys map to multiple Urdu letters. These may be accessed using the uppercase. For example, Typing the uppercase 'D' will produce <span className="text-lg font-ur-sans">"ڈ"</span>. However, because Urdu has more
                characters than English, some mappings break this rule. For example, <span className="text-lg font-ur-sans">"ہ"</span> is mapped to "o" because "h" and "H" were already mapped 
                to <span className="text-lg font-ur-sans">"ح"</span> and <span className="text-lg font-ur-sans">"ھ"</span>
            </p>
            <img src="/instructions/crulp2.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>
                Therefore to enter <span className="text-lg font-ur-sans">"یہ ایک"</span>, you must press the following sequence of keys "i", "o", "space", "a", "i", "k". This is demonstrated below.
            </p>
            <img src="/instructions/crulp3.gif" className="w-[80%] mx-auto h-auto border-5 border-black" />
            <hr></hr>
            <p>In the following condition we will ask you to type a number of sentences in Urdu using this keyboard and interface. Whenever you feel ready please click on the button to navigate to the condition.</p>
            <ButtonStartSCondition target={"/crulp"}/>
        </div>
    );
}