"use client";

import api from "@/utils/axios"; // axios instance with JWT interceptor

// Fetch all search history
export async function fetchSearchHistory() {
  try {
    const res = await api.get("/search_history/");
    // Map backend data to frontend format
    return res.data.map((item) => ({
      id: item.search_id,
      title: item.query.length > 50 ? item.query.slice(0, 50) + "..." : item.query,
      messages: [
        {
          id: item.search_id,
          text: item.query,
          isUser: true,
          timestamp: new Date(item.searched_at),
        },
      ],
    }));
  } catch (err) {
    console.error("Failed to fetch search history:", err);
    throw err;
  }
}

// Save a new search query
export async function saveSearchQuery(query) {
  try {
    const res = await api.post("/search_history/", { query });
    return res.data; // {search_id, query, searched_at}
  } catch (err) {
    console.error("Failed to save search query:", err);
    throw err;
  }
}
