"use client";
import api from "@/utils/axios";

export async function fetchUserProfile() {
  const res = await api.get("/profile/");
  return res.data;
}
