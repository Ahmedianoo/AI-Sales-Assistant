import api from "../utils/axios";

//signup
export const signup = async (data) => {
  return await api.post("/users/signup", data);
};

//login
export const login = async (data) => {
  return await api.post("/login", data);
};

// // logout
// export const logout = async () => {
//   return await api.post("/logout");
// };

// logout
export const logout = async () => {
  // Remove JWT from localStorage to "log out" the user
  localStorage.removeItem("jwt");
  return Promise.resolve();
};


// get user info
export const getUser = async () => {
  return await api.get("/me");
};

