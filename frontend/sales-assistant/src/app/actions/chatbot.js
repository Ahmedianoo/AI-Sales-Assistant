"use client";

import api from "@/utils/axios"; // axios instance with JWT interceptor

export async function call_to_chatbot(query) {
  try{
      const res = await api.post("/ai_chat/", { query });      
      return res.data.response;
  }
  catch{
    console.error("failed to call chatbot endpoint", err);
  }
}
