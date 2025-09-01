"use server";

export async function fetchBattlecards(user_comp_id) {
  const res = await fetch(`http://backend:8000/battlecards/competitor/${user_comp_id}`, {
    cache: "no-store",
  });

  if (!res.ok) throw new Error("Failed to fetch battlecards");
  return res.json();
}


export async function fetchCompetitors(user_id) {
  const res = await fetch(`http://backend:8000/battlecards/user/${user_id}`, {
    cache: "no-store",
  });

  if (!res.ok) throw new Error("Failed to fetch competitors");
  return res.json();
}


export async function createBattlecard({ title, user_comp_id, content, auto_release }) {
  const res = await fetch("http://backend:8000/battlecards/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, user_comp_id, content, auto_release }),
  });

  if (!res.ok) throw new Error("Failed to create battlecard");
  return res.json();
}
