import React, { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import axios from "axios";
import {Reorder} from "framer-motion"
import KeyboardVisNoInteract from "../components/KeyboardVisNoInteract";
import {QWERTY_LAYOUT, WINDOWS_LAYOUT, CRULP_LAYOUT} from "../assets/layouts"
import { useNavigate } from "react-router-dom";
import { endpoint_live } from "../api";

// Validation schema with required Likert questions
const schema = z.object({
  ranking: z.array(z.string()).length(3, "Please rank all three input systems"),
  rankingReason: z.string().min(1, "This field is required"),
  romanUrduUsage: z.string().min(1, "Please select an option"),
  urduScriptUsage: z.string().min(1, "Please select an option"),
  urduContexts: z.string().min(1, "This field is required"),
  otherCommunication: z.string().min(1, "This field is required"),
  accessDifficulty: z.string().min(1, "Please select a rating"),
  urduContent: z.string().min(1, "This field is required"),
  langaugeUse: z.string().min(1, "This field is required"),
  langaugeAcq: z.string().min(1, "This field is required"),
  birthYear: z.string().min(4, "Enter a valid year"),
  gender: z.string().min(1, "This field is required"),
  feedback: z.string().optional(),
});

// Urdu Input Systems for Ranking

const urduSystems = ["CRULP", "IME", "WINDOWS"];
export default function Questionnaire() {
    const [ranking, setRanking] = useState(urduSystems);
    const [submissionAttempted, setSubmissionAttempted] = useState(false);
    const navigate = useNavigate();

    const {
    register,
    handleSubmit,
    control,
    setValue,
    watch,
    formState: { errors},
    } = useForm({
        resolver: zodResolver(schema),
        defaultValues: { ranking: ranking },
    });

    const [boards,setBoards] = useState([
      {id:"CRULP", text:"phonetic keybaord", body:<KeyboardVisNoInteract layout={CRULP_LAYOUT}/>},
      {id:"IME", text:"roman urdu input",  body:<KeyboardVisNoInteract layout={QWERTY_LAYOUT}/>},
      {id:"WINDOWS", text:"frequency keybaord", body:<KeyboardVisNoInteract layout={WINDOWS_LAYOUT}/>},
    ]);

    const onDragEnd = (newOrder) =>{
      setBoards(newOrder);
      setValue("ranking", newOrder.map((board) => board.id));
      console.log("Updated Ranking:", newOrder.map((board) => board.id));
    }
  
    const onSubmit = async (data) => {
      
      console.log("Survey Data:", data);
      try {
        const uid = localStorage.getItem("uid")
        const response = await axios.post(`${endpoint_live}submit?uid=${uid}`, data);
        console.log("Success:", response.data);
      } catch (error) {
        console.error("Error:", error.response?.data?.detail || "Unknown error");
      }finally {
        console.log("Form submitted");
        navigate("/exit");
      }
    };

  return (
    
    <div className="p-6 px-[10vw] flex-col space-y-3">
      <div>
          <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
          <h3 className="text-2xl font-bold">Questionnaire</h3>
      </div>
      
      <h3 className="px-3 bg-black text-white text-2xl">All the conditions are now complete!</h3>

      <p>Please carefully read and fill out the following questionnaire and answer to the best of your ability.</p>

      <hr></hr>

      <form onSubmit={handleSubmit(onSubmit, () => setSubmissionAttempted(true))} className="space-y-6 text-xl">
        
        {/* Ranking Question */}
        <div>
          <label className="block mb-2">
            <span className="font-bold text-xl bg-black text-white px-1">Q1:</span> Please rank the three Urdu text input systems in order of preference, with top being your most preferred and bottom being your least preferred.
          </label>
          <Reorder.Group values={boards} onReorder={onDragEnd}>
            {boards.map((board)=>(
              <Reorder.Item value={board} key={board.id} _dragX={false} className="my-5 bg-gray border-3 rounded-md">
              <p className="mx-3 pb-2 text-xl"><span className="font-bold">{board.id}</span>{": "+ board.text}</p>
              {board.body}
              </Reorder.Item>
            ))}
          </Reorder.Group>
        </div>

        {/* Ranking Reason */}
        <div>
          <label className="block font-medium pb-1">
          <span className="font-bold text-xl bg-black text-white px-1">Q2:</span> What influenced your ranking choices for the three input systems? Please explain.
          </label>
          <textarea {...register("rankingReason")} className="w-full h-30 text-base border-3 p-2 rounded focus:outline-none focus:ring-0 focus:border-deep-blue" />
          {errors.rankingReason && <p className="text-error font-bold text-sm">{errors.rankingReason.message}</p>}
        </div>

        {/* Urdu Input */}
        {[
          { id:"3", name: "romanUrduUsage", label: " How often do you type in Roman Urdu?" },
          { id:"4",name: "urduScriptUsage", label: " How often do you type in Urdu using the Urdu script (nastaliq, nakhs)?" },
        ].map(({ id, name, label }) => (
          <div key={name}>
            <label className="block mb-2">
              <span className="font-bold text-xl bg-black text-white px-1">{"Q"+id}:</span>{label}
            </label>
            <span className="mx-8">
            {["Always", "Very Often", "Sometimes", "Rarely", "Never"].map((option) => (
              <label key={option} className="inline-flex items-center space-x-2 mr-4 ">
                <input type="radio" {...register(name)} value={option} className="mr-1" />
                {option}
              </label>
            ))}
            </span>
            {errors[name] && <p className="text-error font-bold text-sm">{"Please select an option"}</p>}
          </div>
        ))}

        {/* Urdu Input Open */}
        {[
          { id:"5",name: "urduContexts", label: "If you type in Urdu (either in Roman Urdu or Urdu script), what platforms or contexts do you use it for? (e.g., WhatsApp messages, Twitter posts, emails, blogs etc.)" },
          { id:"6",name: "otherCommunication", label: "Besides text input, do you communicate in Urdu through other means? (voice messages etc.)" },
        ].map(({ id, name, label }) => (
          <div key={name}>
            <label className="block font-medium">
            <span className="font-bold text-xl bg-black text-white px-1">{"Q"+id}:</span> {label}
            </label>
            <textarea {...register(name)} className="w-full h-30 text-base border-3 p-2 rounded focus:outline-none focus:ring-0 focus:border-deep-blue" />
            {errors[name] && <p className="text-error font-bold text-sm">{errors[name].message}</p>}
          </div>
        ))}

        {/* Urdu Access */}
        <div>
          <label className="block font-medium">
          <span className="font-bold text-xl bg-black text-white px-1">Q7:</span> Please rate how strongly you agree or disagree with the following statement: "I can easily access digital content in Urdu (in the Urdu script)"
          </label>
          <span className="mx-8">
          {["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"].map((num) => (
            <label key={num} className="inline-flex items-center space-x-2 mr-4">
              <input type="radio" {...register("accessDifficulty")} value={num} className="mr-1" />
              {num}
            </label>
          ))}
          {errors.accessDifficulty && <p className="text-error font-bold text-sm">{"Please select an option"}</p>}
          </span>
        </div>


        {[
          { id:"8",name: "urduContent", label: "What types of digital Urdu content do you engage with? (e.g., newspapers, social media posts, digital books, online articles, YouTube videos, etc.)" },
          { id:"9",name: "langaugeUse", label: "Please list all the languages you know in order of usage with the most used first. Feel free to provide additional information about your language usage if you like." },
          { id:"10",name: "langaugeAcq", label: "Please list all the languages you know in order of acquisition with your mother tongue first. Feel free to provide additional information about your language acquisition if you like." },
        ].map(({ id, name, label }) => (
          <div key={name}>
            <label className="block font-medium">
            <span className="font-bold text-xl bg-black text-white px-1">{"Q"+id}:</span> {label}
            </label>
            <textarea {...register(name)} className="w-full h-30 text-base border-3 p-2 rounded focus:outline-none focus:ring-0 focus:border-deep-blue" />
            {errors[name] && <p className="text-error font-bold text-sm">{errors[name].message}</p>}
          </div>
        ))}

        {/* Demo */}
        <div>
          <label className="block font-medium">
          <span className="font-bold text-xl bg-black text-white px-1">Q11:</span> Year of birth</label>
          <input {...register("birthYear")} type="number" className="w-full text-base border-3 p-2 rounded focus:outline-none focus:ring-0 focus:border-deep-blue" defaultValue="2000"/>
          {errors.birthYear && <p className="text-error font-bold text-sm">{errors.birthYear.message}</p>}
        </div>

        <div>
          <label className="block font-medium">
          <span className="font-bold text-xl bg-black text-white px-1">Q12:</span> Gender</label>
          <input {...register("gender")} className="w-full text-base border-3 p-2 rounded focus:outline-none focus:ring-0 focus:border-deep-blue" />
            {errors.gender && <p className="text-error font-bold text-sm">{errors.gender.message}</p>}
        </div>

        <div>
          <label className="block font-medium">
          <span className="font-bold text-xl bg-black text-white px-1">Q13:</span> If there were any issues while completing the experiment please use this space to let us know.</label>
          <textarea {...register("feedback")} className="w-full h-30 text-base border-3 p-2 rounded focus:outline-none focus:ring-0 focus:border-deep-blue" placeholder="Optional"/>
        </div>

        {/* Submit Button */}
        <div>
        <button 
          type="submit" 
          className={`px-10 mt-3 py-2 text-lg bg-black text-white hover:underline`} 
        >
          Submit
        </button>
        {submissionAttempted && Object.keys(errors).length > 0 && (
          <p className="text-error font-bold text-sm">Please complete all required fields before submitting.</p>
        )}
        </div>
      </form>
    </div>
  );
}
