import React from "react";
import { useState, useRef } from "react";
import { Link } from "react-router-dom";
import ButtonStartStudy from "../components/ButtonStartStudy";

// Home page. Requests user consent.
export default function Exit() {
    return (
        <div className="p-6 px-[10vw] flex-col space-y-3 ">
            <div>
                <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Informed Consent</h3>
            </div>

            <h3 className="mt-10 px-3 bg-black text-white text-2xl">Hello! and thank you for participating.</h3>

            <p>In this project, we are evaluating three different Urdu text entry tools. You will be asked to type a series of sentences using each tool, followed by a short questionnaire at the end of the session. The entire process is expected to take no more than XX minutes. <b>We request that you complete this in one sitting and one attempt.</b> Before we begin, we would like you to read the following consent form carefully.
            </p>

            <div className="flex justify-center">
                <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSdRVf2LNa6Xta3PeZGCgW_FzjHP46ljKuTtoJMzad1bOGzbXw/viewform?embedded=true" width="640" height="382" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
            </div>
        </div>
    );
}