import React from "react";
import { useState, useRef } from "react";
import { Link } from "react-router-dom";

export default function Consent() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");

    return (
        <div className="p-6 px-[10vw] flex-col space-y-3 ">
            <div>
                <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Informed Consent</h3>
            </div>
            <h3 className="mt-10 px-3 bg-black text-white text-2xl">Hello! and thank you for participating.</h3>
            <p>In this project, we are evaluating three different Urdu text entry tools. You will be asked to type a series of sentences using each tool, followed by a short questionnaire at the end of the session. The entire process is expected to take no more than XX minutes. <b>We request that you complete this in one sitting and one attempt.</b> Before we begin, we would like you to read the following consent form carefully.
            </p>

            <div className="bg-white border-4">
            <h3 className="text-3xl p-3 font-bold bg-black text-white  border-b-2 px-3">Consent Form.</h3>
            <div className="h-100 overflow-y-auto ">
            <div className="flex-col space-y-2  p-3">
            <p>
                The data collected from this study will be used in articles for publication in journals and conference proceedings. Any write-ups of the data will not include information that can be linked directly to you.
            </p>

            <h3 className=" text-xl font-bold underline">1. Benefits:</h3>
            <p>
                Other than the receipt of a small honorarium, you will not directly benefit from your participation. Information gathered in this research will help us improve existingeducational technologies and develop new ones that could benefit future students.
            </p>

            <h3 className=" text-xl font-bold underline">2. Risk:</h3>
            <p>
                While complete anonymity cannot be guaranteed, we will remove all identifying 
                details before analyzing the data to minimize the possibility of participant 
                identification. There are no foreseeable risks associated with participation. 
                If any new risks arise, we will pause the study and notify you immediately. 
                If necessary, the study may be discontinued.
            </p>
            <p>
                There are no other foreseeable risks. If at any time, we become aware of additional risks, we will postpone the study and notify you immediately so that these risks can be minimized before we continue with research activities. If it is necessary, we will stop the study altogether.
            </p>

            <h3 className=" text-xl font-bold underline">3. Remuneration:</h3>
            <p>
                To thank you for your time, we will be pleased to make a summary of the results available to you once they have been compiled. This summary will outline the research and discuss our findings and recommendations. It will be made available through our lab website: https://spaces.facsci.ualberta.ca/edtekla/ We expect this summary to be available in April. 2024. 
            </p>
            <p>
                You are also eligible to receive a gift card for $30
            </p>

            <h3 className=" text-xl font-bold underline">4. Confidentiality & Anonymity:</h3>
            <p>
                No one will be identified in this study and identifying personal information will be removed. Reports and publications detailing the results of this research will describe aggregate data. 
            </p>
            <p>
                All data and documents will be securely kept for a period of at least 5 years after we have finished our research activities. Data may be kept for even longer. If we decide not to keep it after 5 years, it will be destroyed.
            </p>

            <h3 className=" text-xl font-bold underline">5. Voluntary Participation & Freedom to Withdraw:</h3>
            <p>
                You get to choose whether you want to complete study activities. This includes whether you answer specific questions that are part of the study. It is okay if you don't want us to use your data. We can always exclude your data while analyzing that of others. Your participation will in no way affect your course grades. Your instructors will not be told who has or has not participated. You may withdraw at any time. To withdraw, tell us that you would like to leave.
            </p>
            <p>
                If you complete study activities, you can still withdraw later. We will give you a code that you can use to withdraw your data. Make sure that you keep this code because we will not be able to find and destroy your data otherwise. If you withdraw during or after your participation, your remuneration will not be affected.
            </p>
            <p>
                If you do not participate in this study or choose to withdraw from this study, the data that was collected during your participation will be destroyed. Note that you cannot have your data removed if we have already published papers based on that data. The earliest that this is expected to happen will be 3 months after data collection.
            </p>
            
            <h3 className=" text-xl font-bold underline">6. Further Information:</h3>
            <p>
                Please contact Carrie, by email at demmanse@ualberta.ca , or Yalmaz, by email at edtekla@ualberta.ca , if you would like to know more. They are both happy to answer questions about this study and what we are doing. Please contact either of them if you have any questions or concerns. 
            </p>
            <p>
                The plan for this study has been reviewed by a Research Ethics Board at the University of Alberta (Pro00115709). If you have questions about your rights or how research should be conducted, you can call (780) 492-2615.  This office is independent of the researchers.
            </p>
            </div>
            </div>
            </div>
            
            <p className="pt-3 "> By clicking the <b>"Start"</b> button you agree that you have read this form, been told whom to contact if you have questions, and are able to save a copy of this consent form for yourself. 
            </p>

            <Link to="/baseline">
            <button type="baseline" className="px-10 py-2 bg-black text-white text-lg hover:underline">
                Start
            </button>
            </Link>
        </div>
    );
}