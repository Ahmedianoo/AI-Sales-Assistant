"use client";

import api from "@/utils/axios"; // axios instance with JWT interceptor

// Fetch conversations for displaying in sidebar
export async function fetchConversations() {
  try {
    const res = await api.get("/search_history/");
    // res: {id, query, created_at}
    
    // Map backend data to frontend format
    return res.data.map((item) => ({
      id: item.id,
      title: item.query.length > 50 ? item.query.slice(0, 50) + "..." : item.query,
      // messages: [
      //   {
      //     id: item.id,
      //     text: item.query,
      //     isUser: true,
      //     timestamp: new Date(item.created_at),
      //   },
      // ],
    }));
  } catch (err) {
    console.error("Failed to fetch search history:", err);
    throw err;
  }
}

export async function fetchChatMessages(threadId) {
  try {
    const response = await api.get(`/search_history/messages`, {
      params: { thread_id: threadId }
    });

    // Correctly return the array of messages
    return response.data?.messages ?? [];
  } catch (err) {
    console.error("Error fetching chat messages:", err);
    return [];
  }
}

// // Save a new search query
// export async function saveSearchQuery(query) {
//   try {
//     const res = await api.post("/search_history/", { query });
//     //thread_id, list of message objects {id, text, isUser, timestamp}
//     return res.data; // {search_id, query, searched_at}
//   } catch (err) {
//     console.error("Failed to save search query:", err);
//     throw err;
//   }
// }

