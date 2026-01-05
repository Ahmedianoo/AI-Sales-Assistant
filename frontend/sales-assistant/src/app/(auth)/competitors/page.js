"use client";
import { useEffect, useState } from "react";
// import { api } from "../../../lib/api";
import { fetchCompetitors, createCompetitor, updateCompetitor, deleteCompetitor } from "../../actions//competitors";


export default function CompetitorsPage() {
  const [competitors, setCompetitors] = useState([]);
  const [loading, setLoading] = useState(true);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [currentEditId, setCurrentEditId] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    website_url: "",
    industry: "",
    report_frequency: "",
    battlecard_frequency: "",
  });

  const [errors, setErrors] = useState({});

  const [isReportsOpen, setIsReportsOpen] = useState(false);
  const [isBattlecardsOpen, setIsBattlecardsOpen] = useState(false);
  const [selectedCompetitor, setSelectedCompetitor] = useState(null);

  const loadData = async () => {
    try {
      const data = await fetchCompetitors(); 
      setCompetitors(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    loadData();
  }, []);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) newErrors.name = "Name is required";
    if (!formData.website_url.trim()) {
      newErrors.website_url = "Website URL is required";
    } else if (!/^https?:\/\/.+/.test(formData.website_url)) {
      newErrors.website_url = "Website must be a valid URL (http/https)";
    }

    if (!formData.industry.trim()) newErrors.industry = "Industry is required";
    if (!formData.report_frequency)
      newErrors.report_frequency = "Select a report frequency";
    if (!formData.battlecard_frequency)
      newErrors.battlecard_frequency = "Select a battlecard frequency";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    try {
      if (isEditMode && currentEditId) {
        await updateCompetitor(currentEditId, formData); 
      } else {
        await createCompetitor(formData); 
      }

      setIsModalOpen(false);
      setIsEditMode(false);
      setFormData({
        name: "",
        website_url: "",
        industry: "",
        report_frequency: "",
        battlecard_frequency: "",
      });
      setErrors({});
      await loadData();
    } catch (e) {
      alert("Error: " + e.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteCompetitor(id);
      await loadData();
    } catch (e) {
      alert("Error: " + e.message);
    }
  };

  const renderBadge = (value, type) => {
    let color = "bg-gray-200 text-gray-800";

    if (type === "report") {
      color =
        value === "weekly"
          ? "bg-green-100 text-green-700"
          : "bg-blue-100 text-blue-700";
    }

    if (type === "battlecard") {
      color =
        value === "weekly"
          ? "bg-purple-100 text-purple-700"
          : "bg-orange-100 text-orange-700";
    }

    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${color}`}>
        {value || "-"}
      </span>
    );
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* <div className="absolute top-4 left-4 text-xl font-bold text-gray-800">
        NTG_SalesAI
      </div> */}

      <div className="p-6 max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">My Competitors</h1>

        <div className="mb-4 flex items-center space-x-4">
          <button
            onClick={() => {
              setFormData({
                name: "",
                website_url: "",
                industry: "",
                report_frequency: "",
                battlecard_frequency: "",
              });
              setErrors({});
              setIsModalOpen(true);
              setIsEditMode(false);
            }}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
          >
            + Add Competitor
          </button>
        </div>

        {loading ? (
          <p>Loading competitors...</p>
        ) : (
          <div className="overflow-x-auto shadow-md rounded-2xl">
            <table className="min-w-full border border-gray-200 bg-white rounded-lg">
              <thead className="bg-gray-100 text-gray-700">
                <tr>
                  <th className="px-4 py-2 text-left">Name</th>
                  <th className="px-4 py-2 text-left">Website</th>
                  <th className="px-4 py-2 text-left">Industry</th>
                  <th className="px-4 py-2 text-left">Report Frequency</th>
                  <th className="px-4 py-2 text-left">
                    Battlecard Frequency
                  </th>
                  <th className="px-4 py-2 text-center">Actions</th>
                </tr>
              </thead>

              <tbody>
                {competitors.map((c) => (
                  <tr
                    key={c.competitor_id}
                    className="border-t hover:bg-gray-50 transition"
                  >
                    <td className="px-4 py-2 font-medium">{c.name}</td>

                    <td className="px-4 py-2 text-blue-600 underline">
                      <a href={c.website_url} target="_blank" rel="noreferrer">
                        {c.website_url}
                      </a>
                    </td>

                    <td>
                      <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                        {c.industry}
                      </span>
                    </td>

                    <td className="px-4 py-2">
                      {renderBadge(c.report_frequency, "report")}
                    </td>

                    <td className="px-4 py-2">
                      {renderBadge(c.battlecard_frequency, "battlecard")}
                    </td>

                    <td className="px-4 py-2 text-center space-x-2">
                      <button
                        onClick={() => {
                          setSelectedCompetitor(c);
                          setIsReportsOpen(true);
                        }}
                        className="px-3 py-1 bg-purple-500 text-white rounded-lg text-sm hover:bg-purple-600"
                      >
                        Reports
                      </button>

                      <button
                        onClick={() => {
                          setSelectedCompetitor(c);
                          setIsBattlecardsOpen(true);
                        }}
                        className="px-3 py-1 bg-indigo-500 text-white rounded-lg text-sm hover:bg-indigo-600"
                      >
                        Battlecards
                      </button>

                      <button
                        onClick={() => {
                          setFormData({ ...c });
                          setCurrentEditId(c.competitor_id);
                          setIsEditMode(true);
                          setIsModalOpen(true);
                        }}
                        className="px-3 py-1 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600"
                      >
                        Edit
                      </button>

                      <button
                        onClick={() => handleDelete(c.competitor_id)}
                        className="px-3 py-1 bg-red-500 text-white rounded-lg text-sm hover:bg-red-600"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}

                {competitors.length === 0 && (
                  <tr>
                    <td
                      colSpan={6}
                      className="text-center py-4 text-gray-500"
                    >
                      No competitors found. Add one!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}

        {/* Modal Add/Edit */}
        {isModalOpen && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-6 rounded-2xl w-96 shadow-lg">
              <h2 className="text-xl font-semibold mb-4">
                {isEditMode ? "Edit Competitor" : "Add Competitor"}
              </h2>

              <input
                type="text"
                placeholder="Name"
                className={`w-full border p-2 rounded mb-1 ${
                  errors.name ? "border-red-500" : ""
                }`}
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
              />
              {errors.name && (
                <p className="text-red-500 text-sm mb-2">{errors.name}</p>
              )}

              <input
                type="text"
                placeholder="Website URL"
                className={`w-full border p-2 rounded mb-1 ${
                  errors.website_url ? "border-red-500" : ""
                }`}
                value={formData.website_url}
                onChange={(e) =>
                  setFormData({ ...formData, website_url: e.target.value })
                }
              />
              {errors.website_url && (
                <p className="text-red-500 text-sm mb-2">
                  {errors.website_url}
                </p>
              )}

              <input
                type="text"
                placeholder="Industry"
                className={`w-full border p-2 rounded mb-1 ${
                  errors.industry ? "border-red-500" : ""
                }`}
                value={formData.industry || ""}
                onChange={(e) =>
                  setFormData({ ...formData, industry: e.target.value })
                }
              />
              {errors.industry && (
                <p className="text-red-500 text-sm mb-2">{errors.industry}</p>
              )}

              <select
                className={`w-full border p-2 rounded mb-1 ${
                  errors.report_frequency ? "border-red-500" : ""
                }`}
                value={formData.report_frequency}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    report_frequency: e.target.value,
                  })
                }
              >
                <option value="">Select Report Frequency</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
              {errors.report_frequency && (
                <p className="text-red-500 text-sm mb-2">
                  {errors.report_frequency}
                </p>
              )}

              <select
                className={`w-full border p-2 rounded mb-1 ${
                  errors.battlecard_frequency ? "border-red-500" : ""
                }`}
                value={formData.battlecard_frequency}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    battlecard_frequency: e.target.value,
                  })
                }
              >
                <option value="">Select Battlecard Frequency</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
              {errors.battlecard_frequency && (
                <p className="text-red-500 text-sm mb-2">
                  {errors.battlecard_frequency}
                </p>
              )}

              <div className="flex justify-end space-x-2 mt-4">
                <button
                  onClick={() => {
                    setIsModalOpen(false);
                    setIsEditMode(false);
                    setFormData({
                      name: "",
                      website_url: "",
                      industry: "",
                      report_frequency: "",
                      battlecard_frequency: "",
                    });
                    setErrors({});
                  }}
                  className="px-3 py-1 rounded bg-gray-300"
                >
                  Cancel
                </button>

                <button
                  onClick={handleSubmit}
                  className="px-3 py-1 rounded bg-green-500 text-white"
                >
                  {isEditMode ? "Update" : "Save"}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Reports Modal */}
        {isReportsOpen && selectedCompetitor && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-6 rounded-2xl w-96 shadow-lg">
              <h2 className="text-xl font-semibold mb-4">
                Reports - {selectedCompetitor.name}
              </h2>

              {selectedCompetitor.reports &&
              selectedCompetitor.reports.length > 0 ? (
                <ul className="list-disc pl-5 space-y-1">
                  {selectedCompetitor.reports.map((r, idx) => (
                    <li key={idx} className="text-sm">
                      {r.title} ({r.date})
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 text-sm">
                  No Reports Available Right Now
                </p>
              )}

              <div className="flex justify-end mt-4">
                <button
                  onClick={() => {
                    setIsReportsOpen(false);
                    setSelectedCompetitor(null);
                  }}
                  className="px-3 py-1 rounded bg-gray-300"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Battlecards Modal */}
        {isBattlecardsOpen && selectedCompetitor && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-6 rounded-2xl w-96 shadow-lg">
              <h2 className="text-xl font-semibold mb-4">
                Battlecards - {selectedCompetitor.name}
              </h2>

              {selectedCompetitor.battlecards &&
              selectedCompetitor.battlecards.length > 0 ? (
                <ul className="list-disc pl-5 space-y-1">
                  {selectedCompetitor.battlecards.map((b, idx) => (
                    <li key={idx} className="text-sm">
                      {b.title}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 text-sm">
                  No Battlecards Available Right Now
                </p>
              )}

              <div className="flex justify-end mt-4">
                <button
                  onClick={() => {
                    setIsBattlecardsOpen(false);
                    setSelectedCompetitor(null);
                  }}
                  className="px-3 py-1 rounded bg-gray-300"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
