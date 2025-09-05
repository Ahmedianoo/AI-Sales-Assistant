"use client";
import { useState, useEffect } from "react";
import { fetchCompetitors, fetchBattlecardsForUser, fetchBattlecardsforCompetitor } from "../../../actions/battlecards"; 

export default function FilterSelect({ userId, onSelect }) {
  const [competitors, setCompetitors] = useState([]);
  const [selectedCompetitor, setSelectedCompetitor] = useState("");

  

  useEffect(() => {
    async function loadCompetitors() {
      try {
        const data = await fetchCompetitors(userId);
        setCompetitors(data);

        // Default: show all battlecards initially
        await handleSelect("");
      } catch (err) {
        console.error(err);
        setCompetitors([]);
        onSelect([]);
      }
    }
    if (userId) loadCompetitors();
  }, [userId]);

  const handleSelect = async (compId) => {
    setSelectedCompetitor(compId);

    try {
      let data;
      if (!compId) {
        // No competitor selected → fetch all battlecards
        data = await fetchBattlecardsForUser(userId);
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
    <div className="flex items-center gap-2">
      <label className="font-semibold text-gray-700">Select Competitor:</label>
      <select
        className="border rounded-lg px-3 py-2"
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
