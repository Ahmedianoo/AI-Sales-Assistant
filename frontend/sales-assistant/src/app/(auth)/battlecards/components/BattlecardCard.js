"use client";

import { motion } from "framer-motion";
import { Eye, Trash2 } from "lucide-react";
import { useState } from "react";

export default function BattlecardCard({ battlecard, onView, onEdit, onDelete }) {
  const [hovered, setHovered] = useState(false);

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div
        className="relative rounded-2xl shadow-lg border 
        border-[var(--accent-color)]/40 p-6 
        bg-[var(--primary-bg)]/95 text-[var(--card-foreground)] 
        transition-colors duration-200"
      >
        {/* Header */}
        <div className="mb-3">
          <h3 className="text-xl font-bold font-[var(--font-family-sans)] text-[var(--secondary-color)] truncate">
            {battlecard.title || "Untitled Battlecard"}
          </h3>
        </div>

        {/* Content */}
        <div className="space-y-2 font-[var(--font-family-sans)]">
          <p className="text-sm">
            Competitor:{" "}
            <span className="font-semibold text-[var(--accent-color)]">
              {battlecard.competitor_name || "Unknown"}
            </span>
          </p>
          <p className="text-sm text-[var(--foreground)]/70">
            Created:{" "}
            {battlecard.created_at
              ? new Date(battlecard.created_at).toLocaleDateString()
              : "N/A"}
          </p>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mt-3">
            {battlecard.content &&
              Object.keys(battlecard.content).map((tag, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 text-xs rounded-full 
                  bg-[var(--secondary-color)]/10 
                  text-[var(--secondary-color)] 
                  font-medium border border-[var(--secondary-color)]/30"
                >
                  {tag}
                </span>
              ))}
          </div>
        </div>

        {/* Footer (Actions) */}
        <div className="mt-4">
          {hovered && (
            <motion.div
              className="flex gap-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              transition={{ duration: 0.2 }}
            >
              <button
                onClick={() => onView?.(battlecard)}
                className="flex items-center gap-1 px-3 py-1.5 text-sm rounded-lg 
                bg-[var(--secondary-color)] text-white 
                shadow-sm hover:brightness-95 transition"
              >
                <Eye className="w-4 h-4" /> View
              </button>

              <button
                onClick={() => onDelete?.(battlecard)}
                className="flex items-center gap-1 px-3 py-1.5 text-sm rounded-lg 
                bg-red-500 text-white shadow-sm 
                hover:bg-red-600 transition"
              >
                <Trash2 className="w-4 h-4" /> Delete
              </button>
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
