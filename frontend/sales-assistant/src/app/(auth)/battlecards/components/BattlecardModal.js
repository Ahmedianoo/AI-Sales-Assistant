"use client";
import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { motion } from "framer-motion";
import { updateBattlecard } from "../../../actions/battlecards";

export default function BattlecardModal({ isOpen, onClose, battlecard, onUpdate }) {
  const [editMode, setEditMode] = useState(false);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState({});
  const [autoRelease, setAutoRelease] = useState(false);

  const [draftTitle, setDraftTitle] = useState("");
  const [draftContent, setDraftContent] = useState({});
  const [draftAutoRelease, setDraftAutoRelease] = useState(false);

  useEffect(() => {
    if (battlecard) {
      setTitle(battlecard.title || "");
      setContent(
        typeof battlecard.content === "string"
          ? JSON.parse(battlecard.content || "{}")
          : battlecard.content || {}
      );
      setAutoRelease(battlecard.auto_release || false);

      setDraftTitle(battlecard.title || "");
      setDraftContent(
        typeof battlecard.content === "string"
          ? JSON.parse(battlecard.content || "{}")
          : battlecard.content || {}
      );
      setDraftAutoRelease(battlecard.auto_release || false);
    }
  }, [battlecard]);

  if (!battlecard) return null;

  const handleSave = async () => {
    try {
      const updatedCard = await updateBattlecard(battlecard.battlecard_id, {
        title: draftTitle,
        content: draftContent,
        auto_release: draftAutoRelease,
      });

      setTitle(draftTitle);
      setContent(draftContent);
      setAutoRelease(draftAutoRelease);

      onUpdate?.(updatedCard);
      setEditMode(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCancel = () => {
    setDraftTitle(title);
    setDraftContent(content);
    setDraftAutoRelease(autoRelease);
    setEditMode(false);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className="max-w-6xl w-full h-[85vh] overflow-y-auto rounded-3xl border 
        border-indigo-300/60 shadow-2xl p-10 
        bg-gradient-to-br from-indigo-50 via-white to-purple-50"
      >
        <DialogHeader className="space-y-2">
          {editMode ? (
            <DialogTitle asChild>
              <Input
                value={draftTitle}
                onChange={(e) => setDraftTitle(e.target.value)}
                className="text-2xl font-bold"
              />
            </DialogTitle>
          ) : (
            <DialogTitle className="text-4xl font-extrabold text-gray-900 tracking-tight">
              {title}
            </DialogTitle>
          )}
          {!editMode && (
            <DialogDescription className="text-lg text-gray-600">
              Competitor:{" "}
              <span className="font-semibold text-indigo-700">
                {battlecard.competitor_name || `#${battlecard.user_comp_id}`}
              </span>
            </DialogDescription>
          )}
        </DialogHeader>

        {/* Content */}
        <motion.div
          layout
          className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-8"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {editMode
            ? Object.entries(draftContent).map(([tag, value], idx) => (
                <motion.div
                  key={idx}
                  className="flex flex-col gap-3 p-6 rounded-2xl border bg-white/70 shadow-sm"
                >
                  <h3 className="text-xl font-semibold text-indigo-700">
                    {tag.toUpperCase()}
                  </h3>
                  <Input
                    value={value}
                    onChange={(e) =>
                      setDraftContent({ ...draftContent, [tag]: e.target.value })
                    }
                  />
                </motion.div>
              ))
            : Object.entries(content).map(([tag, value], idx) => (
                <motion.div
                  key={idx}
                  className="p-6 rounded-2xl border bg-white/70 shadow-sm flex flex-col gap-3"
                >
                  <h3 className="text-xl font-semibold text-indigo-700">
                    {tag.toUpperCase()}
                  </h3>
                  <p className="text-lg text-gray-800 leading-relaxed break-words">
                    {value}
                  </p>
                </motion.div>
              ))}
        </motion.div>

        {/* Auto-release */}
        {editMode && (
          <div className="mt-6 flex items-center gap-2">
            <Checkbox
              checked={draftAutoRelease}
              onCheckedChange={(checked) => setDraftAutoRelease(checked)}
            />
            <span className="text-gray-700 text-sm">Auto-release</span>
          </div>
        )}

        {/* Footer */}
        <DialogFooter className="mt-10 flex justify-end gap-3">
          {editMode ? (
            <>
              <Button variant="outline" onClick={handleCancel}>
                Cancel
              </Button>
              <Button onClick={handleSave} className="bg-indigo-600 text-white">
                Save
              </Button>
            </>
          ) : (
            <>
              <Button variant="outline" onClick={onClose}>
                Close
              </Button>
              <Button
                onClick={() => setEditMode(true)}
                className="bg-indigo-600 text-white"
              >
                Edit
              </Button>
            </>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
