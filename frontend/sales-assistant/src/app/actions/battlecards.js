"use client";
import api from "@/utils/axios";

export async function fetchBattlecardsforCompetitor(user_comp_id) {
  const res = await api.get(`/battlecards/competitor/${user_comp_id}`);
  return res.data;
}

export async function fetchBattlecardsForUser() {
  const res = await api.get(`/battlecards/`);
  return res.data;
}


export async function fetchCompetitors() {
  const res = await api.get(`/battlecards/user/`);
  return res.data;
}


export async function createBattlecard({ title, user_comp_id, query, auto_release }) {
  const res = await api.post(`/battlecards/`, {
    title,
    user_comp_id,
    query,
    auto_release,
  });
  return res.data;
}


export async function updateBattlecard(battlecardId, updatedData) {
  const res = await api.put(`/battlecards/${battlecardId}`, updatedData);
  return res.data;
}



export async function deleteBattlecard(battlecardId) {
  await api.delete(`/battlecards/${battlecardId}`);
  return true;
}


