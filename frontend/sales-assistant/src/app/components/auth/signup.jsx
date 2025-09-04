"use client";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation"; // ✅ useRouter instead of redirect

export default function SignupPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      await axios.post("http://localhost:8000/users/signup", form);
      // ✅ Redirect to home page on success
      router.push("/");
    } catch (err) {
      setMessage("❌ " + (err.response?.data?.detail || "Signup failed."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#FAE9C2] p-4">
      <div className="w-full max-w-md bg-white shadow-lg rounded-2xl p-8">
        <h1 className="text-3xl font-bold text-[#B8751C] text-center mb-6">
          SalesAI - Sign Up
        </h1>

        {message && (
          <div className="mb-4 text-center text-sm text-green-700 bg-green-100 p-2 rounded">
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-[#386641] font-medium mb-1">
              Username
            </label>
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-[#386641] text-black"
              required
            />
          </div>

          <div>
            <label className="block text-[#386641] font-medium mb-1">
              Email
            </label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-[#386641] text-black"
              required
            />
          </div>

          <div>
            <label className="block text-[#386641] font-medium mb-1">
              Password
            </label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-[#386641] text-black"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#B8751C] text-white py-2 rounded-lg hover:bg-[#a16214] transition"
          >
            {loading ? "Signing up..." : "Sign Up"}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{" "}
          <a href="/login" className="text-[#386641] font-medium">
            Sign in
          </a>
        </p>
      </div>
    </div>
  );
}
