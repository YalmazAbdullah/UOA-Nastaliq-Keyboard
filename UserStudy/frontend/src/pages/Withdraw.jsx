export default function Withdraw(){
    return (
        <div className="p-6 px-[10vw] flex-col space-y-3 ">
            <div>
                <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Withdraw</h3>
            </div>

            <h3 className=" px-3 bg-black text-white text-2xl">Thank you for participating.</h3>
            {/* code */}
            {/* payment questionaire */}
            {/*  */}

            <p>
                As noted in the consent form, your data will be destroyed. To receive remuneration please make sure to complete the google form below. We need this information to transfer your honorarium. It will be stored separately from the study data. 
            </p>
            <p>
                Please save a copy of your unique code. It will be needed if you have any questions in the future.
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
    )
}