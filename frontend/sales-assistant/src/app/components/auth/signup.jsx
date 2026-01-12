"use client";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation"; 
import "./signup.css"; // ✅ Import CSS file

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
      const res = await axios.post("https://ahmedianoo-ai-sales-assistant-backend.hf.space/users/signup", form);
      localStorage.setItem("jwt", res.data.token);
      router.push("/home");

    } catch (err) {
      setMessage("❌ " + (err.response?.data?.detail || "Signup failed."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-card">
        <h1>SalesAI - Sign Up</h1>

        {message && <div className="signup-message">{message}</div>}

        <form onSubmit={handleSubmit} className="signup-form">
          <div>
            <label>Username</label>
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Signing up..." : "Sign Up"}
          </button>
        </form>

        <p className="signup-footer">
          Already have an account?{" "}
          <a href="/login">Sign in</a>
        </p>
      </div>
    </div>
  );
}
