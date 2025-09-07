"use client";

import { motion } from "framer-motion";
import { Eye, Edit, Trash2 } from "lucide-react";
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
      <div className="relative rounded-2xl shadow-2xl border-2 border-indigo-600 p-4 bg-gradient-to-br from-indigo-900 via-purple-900 to-indigo-800 transition">
        {/* Header */}
        <div className="mb-2">
          <h3 className="text-lg font-bold text-white">
            {battlecard.title || "Untitled Battlecard"}
          </h3>
        </div>

        {/* Content */}
        <div className="space-y-1">
          <p className="text-sm text-gray-300">
            Competitor:{" "}
            <span className="font-semibold text-indigo-400">
              {battlecard.competitor_name || "Unknown"}
            </span>
          </p>
          <p className="text-sm text-gray-400">
            Created:{" "}
            {battlecard.created_at
              ? new Date(battlecard.created_at).toLocaleDateString()
              : "N/A"}
          </p>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mt-2">
            {battlecard.content &&
              Object.keys(battlecard.content).map((tag, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 text-xs rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 text-white font-semibold border border-purple-400"
                >
                  {tag}
                </span>
              ))}
          </div>
        </div>

        {/* Footer (Actions) */}
        <div className="mt-3">
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
                className="flex items-center gap-1 px-3 py-1.5 text-sm border rounded-lg bg-indigo-700 hover:bg-indigo-600 text-white transition"
              >
                <Eye className="w-4 h-4" /> View
              </button>

              {/* <button
                onClick={() => onEdit?.(battlecard)}
                className="flex items-center gap-1 px-3 py-1.5 text-sm bg-purple-600 rounded-lg hover:bg-purple-500 text-white transition"
              >
                <Edit className="w-4 h-4" /> Edit
              </button> */}

              <button
                onClick={() => onDelete?.(battlecard)}
                className="flex items-center gap-1 px-3 py-1.5 text-sm bg-red-500 rounded-lg hover:bg-red-600 text-white transition"
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
