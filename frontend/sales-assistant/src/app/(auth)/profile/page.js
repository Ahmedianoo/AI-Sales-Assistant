"use client";
import { useEffect, useState } from "react";
import { fetchUserProfile } from "@/app/actions/profile";
import { logout } from "@/services/auth";
import { useRouter } from "next/navigation";
import { User, Mail, Crown, LogOut } from "lucide-react"; // small icons

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await fetchUserProfile();
        setUser(data.user);
        setStats(data.stats);
      } catch (err) {
        console.error("Error fetching profile:", err);
      } finally {
        setLoading(false);
      }
    }
    loadProfile();
  }, []);

  async function handleLogout() {
    try {
      await logout();
      router.push("/login");
    } catch (err) {
      console.error("Logout failed:", err);
    }
  }

  if (loading) return <div className="p-8">Loading...</div>;
  if (!user) return <div className="p-8 text-red-500">Failed to load profile</div>;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 p-8">
      <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-2xl p-8 border border-gray-200">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-center gap-6 mb-8">
          <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-indigo-400 to-blue-500 flex items-center justify-center text-white text-3xl font-bold">
            {user.name?.charAt(0).toUpperCase()}
          </div>
          <div>
            <h1 className="text-3xl font-semibold text-gray-800">{user.name}</h1>
            <div className="mt-1 flex items-center text-gray-600 gap-2">
              <Mail size={18} /> <span>{user.email}</span>
            </div>
            <div className="mt-1 flex items-center text-indigo-600 gap-2">
              <Crown size={18} /> <span className="capitalize">{user.plan_type} plan</span>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
          <div className="bg-gray-50 border border-gray-200 p-5 rounded-xl text-center shadow-sm">
            <p className="text-3xl font-bold text-indigo-600">{stats.battlecards}</p>
            <p className="text-gray-500 text-sm mt-1">Battlecards</p>
          </div>
          <div className="bg-gray-50 border border-gray-200 p-5 rounded-xl text-center shadow-sm">
            <p className="text-3xl font-bold text-indigo-600">{stats.reports}</p>
            <p className="text-gray-500 text-sm mt-1">Reports</p>
          </div>
          <div className="bg-gray-50 border border-gray-200 p-5 rounded-xl text-center shadow-sm">
            <p className="text-3xl font-bold text-indigo-600">{stats.competitors}</p>
            <p className="text-gray-500 text-sm mt-1">Competitors</p>
          </div>
        </div>

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white py-2.5 px-6 rounded-xl transition-all w-full sm:w-auto mx-auto"
        >
          <LogOut size={18} /> Logout
        </button>
      </div>
    </div>
  );
}
