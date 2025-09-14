import { useState } from "react";

export default function ConfirmDialog({ isOpen, onCancel, onConfirm, message }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
      <div className="bg-white rounded-xl shadow-lg p-6 w-[400px] text-center">
        <h2 className="text-xl font-bold mb-4 text-[var(--secondary-color)]">
          Confirm Deletion
        </h2>
        <p className="text-gray-700 mb-6">{message}</p>

        <div className="flex justify-center gap-4">
          <button
            onClick={onCancel}
            className="px-4 py-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 transition"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

