"use client";
import { useState, useEffect } from "react";
import { createBattlecard, fetchCompetitors } from "../../../actions/battlecards";

export default function GenerateBattlecardForm({ onCreated, open, setOpen }) {
  const [competitors, setCompetitors] = useState([]);
  const [userCompId, setuserCompId] = useState("");
  const [title, setTitle] = useState("");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);


  useEffect(() => {
    async function load() {
      const data = await fetchCompetitors();
      setCompetitors(data);
    }
    if (open) {
      load();
    } else {
      setTitle("");
      setuserCompId("");
    }
  }, [open]);


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !userCompId) return;
    setLoading(true);

    const newCard = await createBattlecard({
      title,
      user_comp_id: parseInt(userCompId),
      content: {
        strengths: "Faster than competitors",
        weaknesses: "Higher cost",
        opportunities: "Expanding into EU market",
        threats: "New entrants with lower pricing",
      },
      auto_release: false,
    });
    onCreated(newCard);
    setOpen(false);
    setTitle("");
    setuserCompId("");
    setLoading(false);
  };

  return (
    <>
      {open && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
          {/* Animated Card */}
          <div className="bg-[var(--primary-bg)]/95 backdrop-blur-lg rounded-2xl p-8 w-[420px] shadow-2xl transform transition-all duration-300 scale-95 animate-fadeIn relative">

            {loading && (
              <div className="absolute inset-0 flex items-center justify-center bg-white/60 backdrop-blur-sm rounded-2xl z-10">
                <div className="animate-spin rounded-full h-10 w-10 border-4 border-[var(--secondary-color)] border-t-transparent"></div>
              </div>
            )}            

            <h2
              className="text-2xl font-extrabold text-[var(--secondary-color)] mb-6 text-center font-[var(--font-family-serif)]"
            >
              New Battlecard
            </h2>

            <form onSubmit={handleSubmit} className="flex flex-col gap-5">
              {/* Input */}
              <input
                type="text"
                placeholder="Enter battlecard title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="border rounded-xl px-4 py-3 bg-white/70 focus:ring-2 focus:ring-[var(--secondary-color)] focus:outline-none transition-all"
              />

              <input 
                type="text"
                placeholder="Enter specific query (optional)"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="border rounded-xl px-4 py-3 bg-white/70 focus:ring-2 focus:ring-[var(--secondary-color)] focus:outline-none transition-all"
               />

              {/* Select */}
              <select
                value={userCompId}
                onChange={(e) => setuserCompId(e.target.value)}
                className="border rounded-xl px-4 py-3 bg-white/70 focus:ring-2 focus:ring-[var(--secondary-color)] focus:outline-none transition-all"
              >
                <option value="">Select competitor</option>
                {competitors.map((c) => (
                  <option key={c.user_comp_id} value={c.user_comp_id}>
                    {c.competitor.name}
                  </option>
                ))}
              </select>

              {/* Buttons */}
              <div className="flex justify-end gap-3 mt-4">
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  className="px-5 py-2.5 rounded-xl bg-[var(--card)] text-[var(--foreground)] hover:bg-[var(--accent-color)]/30 transition shadow-sm"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-[var(--secondary-color)] text-white font-semibold hover:opacity-90 hover:scale-105 active:scale-95 transition shadow-md"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
