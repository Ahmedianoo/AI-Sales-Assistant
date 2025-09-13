"use client";
import { useState, useEffect } from "react";
import {
  fetchCompetitors,
  fetchBattlecardsForUser,
  fetchBattlecardsforCompetitor,
} from "../../../actions/battlecards";

export default function FilterSelect({ onSelect }) {
  const [competitors, setCompetitors] = useState([]);
  const [selectedCompetitor, setSelectedCompetitor] = useState("");

  useEffect(() => {
    async function loadCompetitors() {
      try {
        const data = await fetchCompetitors();
        setCompetitors(data);

        // Default: show all battlecards initially
        await handleSelect("");
      } catch (err) {
        console.error(err);
        setCompetitors([]);
        onSelect([]);
      }
    }
    loadCompetitors();
  }, []);

  const handleSelect = async (compId) => {
    setSelectedCompetitor(compId);

    try {
      let data;
      if (!compId) {
        // No competitor selected → fetch all battlecards
        data = await fetchBattlecardsForUser();
      } else {
        data = await fetchBattlecardsforCompetitor(compId);
      }
      onSelect(data);
    } catch (err) {
      console.error(err);
      onSelect([]);
    }
  };

  return (
    <div className="flex items-center gap-3">
      <label className="font-semibold text-[var(--secondary-color)] font-[var(--font-family-sans)]">
        Select Competitor:
      </label>
      <select
        className="border rounded-xl px-4 py-2 bg-[var(--card)] text-[var(--foreground)] 
                   focus:ring-2 focus:ring-[var(--secondary-color)] focus:outline-none 
                   hover:bg-[var(--accent-color)]/20 transition"
        value={selectedCompetitor}
        onChange={(e) => handleSelect(e.target.value)}
      >
        <option value="">All Competitors</option>
        {competitors.map((c) => (
          <option key={c.user_comp_id} value={c.user_comp_id}>
            {c.competitor.name}
          </option>
        ))}
      </select>
    </div>
  );
}
