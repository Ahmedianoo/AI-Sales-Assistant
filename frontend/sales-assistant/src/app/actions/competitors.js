import api from "@/utils/axios";

export async function fetchCompetitors() {
  const res = await api.get("/competitors/");
  return res.data;
}

export async function createCompetitor(data) {
  const res = await api.post("/competitors/", data);
  return res.data;
}

export async function updateCompetitor(id, data) {
  const res = await api.put(`/competitors/${id}`, data);
  return res.data;
}

export async function deleteCompetitor(id) {
  await api.delete(`/competitors/${id}`);
  return true;
}
