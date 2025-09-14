"use client";
import { useState } from "react";
import GenerateBattlecardForm from "./components/GenerateBattlecardForm";
import FilterSelect from "./components/FilterSelect";
import { deleteBattlecard } from "../../actions/battlecards";
import BattlecardList from "./components/BattlecardList";
import BattlecardModal from "./components/BattlecardModal";

export default function BattlecardsPage() {
  const [battlecards, setBattlecards] = useState([]);
  const [open, setOpen] = useState(false);
  const [selectedCard, setSelectedCard] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  const updateBattlecard = (updated) => {
    setBattlecards((prev) =>
      prev.map((c) =>
        c.battlecard_id === updated.battlecard_id ? updated : c
      )
    );
  };

  const addBattlecard = (newCard) => {
    setBattlecards((prev) => [...prev, newCard]);
  };

  return (
    <div className="m-6">
      {/* Hero Section */}
        <div
          className="relative min-h-[40vh] flex items-center justify-center 
          bg-[#ebb954] text-[var(--foreground)] 
          overflow-hidden rounded-2xl shadow-lg"
        >



        {/* Decorative background shapes */}
        <div className="absolute inset-0 bg-[var(--primary-bg)]/80"></div>
        <div className="absolute -top-10 -left-10 w-40 h-40 bg-[#75684d] rounded-full blur-3xl opacity-40"></div>
        <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-[#6e6045] rounded-full blur-3xl opacity-40"></div>





        {/* Content */}
        <div className="relative text-center px-6">
          <h1 className="text-5xl font-extrabold drop-shadow-lg font-[var(--font-family-serif)] text-[var(--secondary-color)]">
            Battlecards
          </h1>

          <div className="space-y-4">
            <p className="mt-4 text-lg text-[var(--accent-color)] max-w-xl mx-auto">
              Generate, customize, and manage competitor battlecards with ease.
              Stay sharp and win every deal!
            </p>

            <button
              onClick={() => setOpen(true)}
              className="px-6 py-3 rounded-xl bg-[var(--secondary-color)] text-white font-semibold shadow-md hover:scale-105 hover:opacity-90 transition"
            >
              Generate Battlecard
            </button>
          </div>
        </div>
      </div>

      {/* Button Section (outside overflow-hidden) */}
      <div className="mt-6 flex justify-center gap-4">
        <GenerateBattlecardForm
          onCreated={addBattlecard}
          open={open}
          setOpen={setOpen}
        />
      </div>

      <div className="mt-6 flex justify-center">
        <FilterSelect onSelect={setBattlecards} />
      </div>

      {/* Battlecards List */}
      <div className="mt-8">
        <BattlecardList
          battlecards={battlecards}
          onView={(card) => {
            setSelectedCard(card);
            setModalOpen(true);
          }}
          onEdit={(card) => {
            setSelectedCard(card);
            setModalOpen(true);
          }}
          onDelete={async (card) => {
            if (!confirm("Are you sure you want to delete this battlecard?"))
              return;
            const success = await deleteBattlecard(card.battlecard_id);
            if (success) {
              setBattlecards((prev) =>
                prev.filter((c) => c.battlecard_id !== card.battlecard_id)
              );
            }
          }}
        />
      </div>

      {/* Battlecard Detail Modal */}
      <BattlecardModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        battlecard={selectedCard}
        onUpdate={updateBattlecard}
      />
    </div>
  );
}
