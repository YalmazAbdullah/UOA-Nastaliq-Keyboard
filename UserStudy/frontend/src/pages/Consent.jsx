import React from "react";
import ButtonStartStudy from "../components/ButtonStartStudy";
import uaLogo from '../assets/ua_logo.svg' 

// Home page. Requests user consent.
export default function Consent() {
    return (
        <div className="p-6 px-[10vw] flex-col space-y-3 ">
            <div>
                <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Informed Consent</h3>
            </div>

            <h3 className=" px-3 bg-black text-white text-2xl">Hello! and thank you for participating.</h3>

            {/* PREAMBLE */}
            <p>
                The purpose of this project is to improve Urdu text entry tools by evaluating currently available options and identifying their limitations. To do this, you will be asked to interact with three different Urdu text entry tools and answer a questionnaire afterwards. Your participation should take around 40-45 minutes. Specific study activities include:
            </p>
            <span>
                <ul className="list-disc px-10">
                    <li>Type a series of pseudoword sentences using standard QWERTY input to obtain a baseline of your typing speed</li>
                    <li>Type a series of Urdu sentences using three different text entry options (CRULP, Windows, IME).</li>
                    <li>Complete a questionnaire about your experience with the tools and digital Urdu.</li>
                </ul>
            </span>
            <p className="pt-5">
            To ensure the integrity of the experiment we request that you complete this in <b>one sitting, and <span className="bg-error border-1">do not participate multiple times</span></b>. Before we begin, we would like you to read the following consent form carefully.
            </p>

            {/* CONSENT FORM */}
            <div className="bg-white border-4">
            <h3 className="text-3xl p-3 font-bold bg-black text-white">Consent Form.</h3>
            <div className="h-100 overflow-y-scroll scrollbar-visible">
            <div className="flex-col space-y-2  p-3">
            <div className="flex place-content-between">
                <img src={uaLogo} alt="University of Alberta logo" />
                <div className="p0 m0">
                    <p className="font-bold">DEPARTMENT OF COMPUTING SCIENCE</p>
                    <p>Athabasca Hall 2-52D</p>
                    <p>Edmonton, Alberta, Canada T6G 2E8</p>
                    <p>cdemmansepp@ualberta.ca</p>
                </div>
            </div>
            <hr></hr>
            <p>
                The data collected from this study will be used in articles for publication in journals and conference proceedings. Any write-ups of the data will not include information that can be linked directly to you.
            </p>

            <h3 className=" text-xl font-bold underline">1. Benefits:</h3>
            <p>
                Other than the receipt of a small honorarium, you will not directly benefit from your participation. Information gathered in this research will help us improve existing Urdu language technologies and develop new ones that could benefit future users.
            </p>

            <h3 className=" text-xl font-bold underline">2. Risk:</h3>
            <p>
                While it is always possible that someone can figure out who participated in a study, we will remove all identifying information from your data before analyzing it in order to make it harder for people to tell who has participated. 
            </p>
            <p>
                There are no other foreseeable risks. If at any time, we become aware of additional risks, we will postpone the study and notify you immediately so that these risks can be minimized before we continue with research activities. If it is necessary, we will stop the study altogether.
            </p>

            <h3 className=" text-xl font-bold underline">3. Remuneration:</h3>
            <p>
                To thank you for your time, we will be pleased to make a summary of the results available to you once they have been compiled. This summary will outline the research and discuss our findings and recommendations. It will be made available through our lab <a className="text-blue-700 text-bold hover:underline after:content-['_↗']" href = "https://spaces.facsci.ualberta.ca/edtekla/publications/" target="_blank">website</a>. We expect this summary to be available in May. 2025.
            </p>
            <p>
                You are also eligible to receive an honorarium worth $15 If you are in Canada this will be e-transferred to you. For participants in Pakistan, the remuneration will be transferred through Remitly via Easypaisa. In both cases the information required to complete this transfer will be collected at the end of the study or upon clicking the withdraw button. This information will be stored separately from your data collected as part of the study.  
            </p>

            <h3 className=" text-xl font-bold underline">4. Confidentiality & Anonymity:</h3>
            <p>
                No one will be identified in this study and identifying personal information will be removed. Reports and publications detailing the results of this research will describe aggregate data. Where quotes are included, we will take care to select quotes that will not identify the speaker.
            </p>
            <p>
                All data and documents will be securely kept for a period of at least 5 years after we have finished our research activities. Data may be kept for even longer. If we decide not to keep it after 5 years, it will be destroyed.
            </p>

            <h3 className=" text-xl font-bold underline">5. Voluntary Participation & Freedom to Withdraw:</h3>
            <p>
                You get to choose whether you want to complete study activities. It is okay if you don't want us to use your data. We can always exclude your data while analyzing that of others.
            </p>
            <p>
                You may withdraw at any time. To withdraw, please click the withdraw button. Closing the webpage is another way to withdraw but will not allow us to collect the information needed to remunerate you. 
            </p>
            <p>
                If you complete study activities, you can still withdraw later. We will give you a code that you can use to withdraw your data. Make sure that you keep this code because we will not be able to find and destroy your data otherwise. 
            </p>
            <p>
                If you choose to withdraw from this study, the data that was collected during your participation will be destroyed. Note that you cannot have your data removed if we have already published papers based on that data. The earliest that this is expected to happen will be 3 months after data collection
            </p>
            
            <h3 className=" text-xl font-bold underline">6. Further Information:</h3>
            <p>
                Please contact <a className="text-blue-700 text-bold hover:underline after:content-['_↗']" href = "mailto:demmanse@ualberta.ca" target="_blank">Carrie Demmans Epp</a>, or <a className="text-blue-700 text-bold hover:underline after:content-['_↗']" href = "mailto:edtekla@ualberta.ca" target="_blank">Yalmaz Ali Abdullah</a> with <b>Urdu Keyboard Study</b> in the subject line, if you would like to know more. They are both happy to answer questions about this study and what we are doing. Please contact either of them if you have any questions or concerns.The plan for this study has been reviewed by a Research Ethics Board at the University of Alberta (Pro00082188). If you have questions about your rights or how research should be conducted, you can call (780) 492-2615.  This office is independent of the researchers.
            </p>

            <p>
                A PDF copy of consent form is available <a className="text-blue-700 text-bold hover:underline after:content-['_↗']" href = "/Consent Form.pdf" target="_blank" download="Consent Form.pdf">here</a>.
            </p>
            </div>
            </div>
            </div>
            
            {/* AGREEMENT */}
            <div>
            <p> By clicking the <b>"Start"</b> button you agree that: </p>
            <ol className="list-disc px-10">
                <li>You have read the consent form.</li>
                <li>You have been told whom to contact if you have questions.</li>
                <li>You are able to save a copy of this consent form for yourself.</li>
            </ol>
            </div>

            <ButtonStartStudy/>
        </div>
    );
}