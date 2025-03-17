import React from "react";

// Home page. Requests user consent.
export default function Exit() {
    return (
        <div className="p-6 px-[10vw] flex-col space-y-3 ">
            <div>
                <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Exit</h3>
            </div>

            <h3 className=" px-3 bg-black text-white text-2xl">The study is now complete! Thank you for participating.</h3>

            <p>
                To recive remuneration please make sure to complete the google form below. We need this information to transfer your honorarium. It will be stored seperately from the study data. 
            </p>
            <p>
                Also please make sure to save a copy of your unique code it will be needed if you have any questions or would like to withdraw in the future.
            </p>
            <p className="mb-5 text-2xl font-bold">Your Uniqe Code is: <span className="font-normal underline">{localStorage.getItem("code")}</span></p>

            <hr></hr>

            <div className="flex justify-center">
            <iframe
                src="https://docs.google.com/forms/d/e/1FAIpQLSdRVf2LNa6Xta3PeZGCgW_FzjHP46ljKuTtoJMzad1bOGzbXw/viewform?embedded=true"
                className="w-full h-auto"
                style={{ minHeight: "85vh" }} // Adjust as needed
            >
                Loading…
            </iframe>
            </div>
        </div>
    );
}