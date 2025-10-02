"use client";

import api from "@/utils/axios"; // axios instance with JWT interceptor

export async function call_to_chatbot({query, thread_id}) {
  try{
      const res = await api.post("/ai_chat/", {query, thread_id});      
      return res.data.response;
  }
  catch{
    console.error("failed to call chatbot endpoint", err);
  }
}
