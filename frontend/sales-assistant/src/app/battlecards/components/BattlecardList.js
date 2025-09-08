"use client";

import BattlecardCard from "./BattlecardCard";

export default function BattlecardList({ battlecards, onView, onEdit, onDelete }) {
  if (!battlecards || battlecards.length === 0) {
    return (
      <p className="text-gray-500 text-center mt-4">
        No battlecards available yet.
      </p>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
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
