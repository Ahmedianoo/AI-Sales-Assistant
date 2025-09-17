"use client";

import BattlecardCard from "./BattlecardCard";

export default function BattlecardList({ battlecards, onView, onEdit, onDelete, loading }) {

  if (loading) {
    return (
      <p className="text-[var(--foreground)]/60 text-center mt-6 font-[var(--font-family-sans)] italic">
        Loading...
      </p>
    );
  }

  if (!battlecards || battlecards.length === 0) {
    return (
      <p className="text-[var(--foreground)]/60 text-center mt-6 font-[var(--font-family-sans)] italic">
        No battlecards available yet.
      </p>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {battlecards.map((battlecard) => (
        <BattlecardCard
          key={battlecard.battlecard_id}
          battlecard={battlecard}
          onView={onView}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
