import React, { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
import KeyboardVisNoInteract from "../components/KeyboardVisNoInteract";
import {QWERTY_LAYOUT, WINDOWS_LAYOUT, CRULP_LAYOUT} from "../assets/layouts"

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
  languageDominance: z.string().min(1, "This field is required"),
  languageAcquisition: z.string().min(1, "This field is required"),
  birthYear: z.string().min(4, "Enter a valid year"),
  gender: z.string().min(1, "Please select a gender"),
  otherGender: z.string().optional(),
});

// Urdu Input Systems for Ranking

const urduSystems = ["SystemA", "SystemB", "SystemC"];
export default function Questionnaire() {
    const [ranking, setRanking] = useState(urduSystems);

    const {
    register,
    handleSubmit,
    control,
    setValue,
    watch,
    formState: { errors },
    } = useForm({
        resolver: zodResolver(schema),
        defaultValues: { ranking: ranking },
    });

    const [gender, setGender] = useState("");

    // Handle Drag and Drop
    const onDragEnd = (result) => {
        if (!result.destination) return;
        const items = [...watch("ranking")]; // ✅ Use watch("ranking")
        console.log("Before reorder:", items);
        const [reorderedItem] = items.splice(result.source.index, 1);
        items.splice(result.destination.index, 0, reorderedItem);

        console.log("After reorder:", items);

        setRanking(items); // Update local state
        setValue("ranking", items); // Update form state
    };

    const onSubmit = (data) => {
        console.log("Survey Data:", data);
    };

    const boards = {
        "SystemA": {text:"roman text input",  body:<KeyboardVisNoInteract layout={QWERTY_LAYOUT}/>},
        "SystemB": {text:"phonetic keybaord", body:<KeyboardVisNoInteract layout={CRULP_LAYOUT}/>},
        "SystemC": {text:"frequency keybaord", body:<KeyboardVisNoInteract layout={WINDOWS_LAYOUT}/>}
    }

  return (
    
    <div className="p-6 px-[10vw] flex-col space-y-3">
        <div>
            <h1 className="text-7xl font-black ">Evaluation of Urdu Text Input Options.</h1>
            <h3 className="text-2xl font-bold">Questionnaire</h3>
        </div>
        <h3 className="px-3 bg-black text-white text-2xl">All the conditions are now complete!</h3>

        <p>Please carefully read and fill out the forllowing questionnaire.</p>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Ranking Question */}
        <div>
          <label className="block font-medium mb-2">
            <span className="font-bold text-xl bg-black text-white px-1">Q1:</span> Please rank the three Urdu text input systems in order of preference:
          </label>
          <DragDropContext onDragEnd={onDragEnd}>
          <Droppable droppableId="ranking"  isDropDisabled={false} isCombineEnabled={false} ignoreContainerClipping={false}>
            {(provided) => (
                <ul
                {...provided.droppableProps}
                ref={provided.innerRef}
                className="space-y-2"
                >
                {watch("ranking").map((system, index) => (
                    <Draggable key={system} draggableId={system} index={index}>
                    {(provided) => (
                        <li
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        className="p-1 bg-gray border-3 rounded-md"
                        >
                        {index + 1}. {system}
                        {boards[system].body}
                        </li>
                    )}
                    </Draggable>
                ))}
                {provided.placeholder}
                </ul>
            )}
            </Droppable>
          </DragDropContext>
        </div>

        {/* Open-ended Question */}
        <div>
          <label className="block font-medium">What influenced your ranking choices?</label>
          <textarea {...register("rankingReason")} className="w-full border p-2 rounded" />
          {errors.rankingReason && <p className="text-red-500 text-sm">{errors.rankingReason.message}</p>}
        </div>

        {/* Likert Scale Questions (Required) */}
        {[
          { name: "romanUrduUsage", label: "How often do you type in Roman Urdu?" },
          { name: "urduScriptUsage", label: "How often do you type in Urdu script?" },
        ].map(({ name, label }) => (
          <div key={name}>
            <label className="block font-medium">{label}</label>
            {["Always", "Very Often", "Sometimes", "Rarely", "Never"].map((option) => (
              <label key={option} className="inline-flex items-center space-x-2 mr-4">
                <input type="radio" {...register(name)} value={option} className="mr-1" />
                {option}
              </label>
            ))}
            {errors[name] && <p className="text-red-500 text-sm">{"Please select an option"}</p>}
          </div>
        ))}

        {/* Open-ended Questions */}
        {[
          { name: "urduContexts", label: "If you type in Urdu (either in Roman Urdu or Urdu script), what platforms or contexts do you use it for? (e.g., WhatsApp messages, Twitter posts, emails, blogs etc.)" },
          { name: "otherCommunication", label: "Besides text input, do you communicate in Urdu through other means?" },
          { name: "urduContent", label: "What types of digital Urdu content do you engage with? (e.g., newspapers, social media posts, digital books, online articles, YouTube videos, etc.)" },
        ].map(({ name, label }) => (
          <div key={name}>
            <label className="block font-medium">{label}</label>
            <textarea {...register(name)} className="w-full border p-2 rounded" />
            {errors[name] && <p className="text-red-500 text-sm">{errors[name].message}</p>}
          </div>
        ))}

        {/* Likert Scale Question (1-5) */}
        <div>
          <label className="block font-medium">
            On a scale of 1 to 5, how much do you agree: "I can easily access digital content in Urdu (Urdu script)."
          </label>
          {[1, 2, 3, 4, 5].map((num) => (
            <label key={num} className="inline-flex items-center space-x-2 mr-4">
              <input type="radio" {...register("accessDifficulty")} value={num} className="mr-1" />
              {num}
            </label>
          ))}
          {errors.accessDifficulty && <p className="text-red-500 text-sm">{errors.accessDifficulty.message}</p>}
        </div>

        {/* Birth Year */}
        <div>
          <label className="block font-medium">Year of birth</label>
          <input {...register("birthYear")} type="number" className="w-full border p-2 rounded" />
          {errors.birthYear && <p className="text-red-500 text-sm">{errors.birthYear.message}</p>}
        </div>

        {/* Gender Dropdown with "Other" Input */}
        <div>
          <label className="block font-medium">Gender</label>
          <select
            {...register("gender")}
            className="w-full border p-2 rounded"
            onChange={(e) => setGender(e.target.value)}
          >
            <option value="">Select...</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
          {gender === "Other" && (
            <input {...register("otherGender")} className="w-full border p-2 rounded mt-2" placeholder="Please specify" />
          )}
          {errors.gender && <p className="text-red-500 text-sm">{errors.gender.message}</p>}
        </div>

        {/* Submit Button */}
        <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
          Submit
        </button>
      </form>

      
    </div>
  );
}
