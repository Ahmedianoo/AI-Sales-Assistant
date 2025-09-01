"use client";
import { useState, useEffect } from "react";
import GenerateBattlecardForm from "./components/GenerateBattlecardForm";
import { fetchBattlecards } from "../actions/battlecards";

export default function BattlecardsPage() {
  const [battlecards, setBattlecards] = useState([]);
  const[open, setOpen] = useState(false)
  const temp = 888;

  useEffect(() => {
    async function load() {
      const data = await fetchBattlecards(2);
      setBattlecards(data);
    }
    load();
  }, []);

  const addBattlecard = (newCard) => {
    setBattlecards((prev) => [...prev, newCard]);
  };

  return (
    <div className="m-6">
      {/* Hero Section */}
      <div
        className="relative min-h-[40vh] flex items-center justify-center 
        bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white 
        overflow-hidden rounded-2xl shadow-lg"
      >
        {/* Decorative background shapes */}
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="absolute -top-10 -left-10 w-40 h-40 bg-pink-400 rounded-full blur-3xl opacity-30"></div>
        <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-indigo-400 rounded-full blur-3xl opacity-30"></div>

        {/* Content */}
        <div className="relative text-center px-6">
          <h1 className="text-5xl font-extrabold drop-shadow-lg">Battlecards</h1>

          <div className="space-y-4">
            <p className="mt-4 text-lg text-gray-100 max-w-xl mx-auto">
              Generate, customize, and manage competitor battlecards with ease.
              Stay sharp and win every deal!
            </p>

            <button
              onClick={() => setOpen(true)}
              className="px-6 py-3 rounded-xl bg-indigo-700 text-white font-semibold shadow-md hover:scale-105 transition"
              >
              Generate Battlecard
           </button>   
          </div>



       
          

        </div>
      </div>

      {/* Button Section (outside overflow-hidden) */}
      <div className="mt-6 flex justify-center gap-4">
        <GenerateBattlecardForm userId={temp} onCreated={addBattlecard} open={open} setOpen={setOpen}/>
      </div>

      {/* Battlecards List */}
      {/* <div className="mt-8 grid gap-4">
        {battlecards.map((card) => (
          <div
            key={card.battlecard_id}
            className="p-4 rounded-xl shadow bg-white"
          >
            <h3 className="text-lg font-bold">{card.title}</h3>
            <p>
              Competitor:{" "}
              {card.competitor ? card.competitor.name : `#${card.user_comp_id}`}
            </p>
            <p className="text-sm text-gray-500">
              Auto-release: {card.auto_release ? "Yes" : "No"}
            </p>
          </div>
        ))}
      </div> */}
    </div>
  );
}
