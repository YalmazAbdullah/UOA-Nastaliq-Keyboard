export default function End(){
    return (
        <div className="p-6 px-[10vw] flex-col space-y-3 ">
            <div>
                <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
                <h3 className="text-2xl font-bold">Study Complete or Paused</h3>
            </div>

            <h3 className=" px-3 bg-black text-white text-2xl">No longer accepting participants. Thank you for intreset.</h3>

            <div>
            <p>
                Thank you for your interest in our study however at the moment we are no longer accepting participants. This is either because we have completed data collection or the study is temporarily on hold. For further details please reach out to <a className="text-blue-700 text-bold hover:underline after:content-['_↗']" href = "mailto:demmanse@ualberta.ca">Carrie Demmans Epp</a>, or <a className="text-blue-700 text-bold hover:underline after:content-['_↗']" href = "mailto:edtekla@ualberta.ca">Yalmaz Ali Abdullah</a> with <b>Urdu Keyboard Study</b> in the subject line
            </p>
            </div>

            <p className="mb-5 text-2xl font-bold">Your Uniqe Code is: <span className="font-normal underline">{localStorage.getItem("code")}</span></p>
        </div>
    )
}