export default function Repeat(){
    return (
        <div className="p-6 px-[10vw] flex-col space-y-3 ">
            <div>
                <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Already Complete</h3>
            </div>

            <h3 className=" px-3 bg-black text-white text-2xl">Thank you for intreset however it seems you have already attempted this study.</h3>
            {/* code */}
            {/* payment questionaire */}
            {/*  */}

            <div>
            <p>
                To preserve the integrety of the experiment we request that you <span className="bg-error border-1"><b>only participate in this study once</b></span>. Our records indicate that you have already completed or withdrawn from the study. If you:
            </p>
            <ul className="list-disc px-10">
                <li>belive this is a mistake then please reach out to <a className="text-blue-700 text-bold hover:underline after:content-['_↗']" href = "mailto:edtekla@ualberta.ca">Yalmaz Ali Abdullah</a> with <b>Urdu Keyboard Study</b> in the subject line and your <b>unique code</b>.</li>
                <li>would like to support our work then please share a <a className="text-blue-700 text-bold hover:underline after:content-['_↗']" href = "">link</a> to this study with people that you think would be interested. </li>
            </ul>
            </div>

            <p className="mb-5 text-2xl font-bold">Your Uniqe Code is: <span className="font-normal underline">{localStorage.getItem("code")}</span></p>
        </div>
    )
}