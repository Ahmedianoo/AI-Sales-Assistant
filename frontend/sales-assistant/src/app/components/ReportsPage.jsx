"use client";

import React, { useEffect, useState } from "react";
import "./reports.css";

export default function ReportsPage() {
  const [reports, setReports] = useState([]);
  const [competitors, setCompetitors] = useState([]);
  const [selectedCompetitor, setSelectedCompetitor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("jwt");
        if (!token) {
          setError("No token found. Please log in.");
          setLoading(false);
          return;
        }

        // Fetch competitors (includes both user_comp_id and competitor_id)
        const compRes = await fetch("https://ahmedianoo-ai-sales-assistant-backend.hf.space/competitors/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!compRes.ok) throw new Error("Failed to fetch competitors");
        const compData = await compRes.json();
        setCompetitors(compData);

        // Fetch reports
        const repRes = await fetch("https://ahmedianoo-ai-sales-assistant-backend.hf.space/reports/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!repRes.ok) throw new Error("Failed to fetch reports");
        const repData = await repRes.json();
        setReports(repData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatReportText = (text) => {
    if (!text) return "";

    // Escape HTML
    let escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Bold (**bold**)
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // Convert numbered lists
    escaped = escaped.replace(/^(\d+)\.\s+(.*)$/gm, "<li>$2</li>");
    // Wrap <li> elements in <ol>
    if (escaped.includes("<li>")) {
      escaped = `<ol>${escaped}</ol>`;
    }

    // Convert line breaks to <br/>
    escaped = escaped.replace(/\n/g, "<br/>");

    return escaped;
  };


  const handleGenerateReport = async () => {
    try {
      const token = localStorage.getItem("jwt");
      if (!selectedCompetitor) {
        alert("Please select a competitor first");
        return;
      }

      setGenerating(true);

      const body = {
        user_comp_id: selectedCompetitor.user_comp_id,
        competitor_id: selectedCompetitor.competitor_id,
      };

      console.log("Sending body:", body);

      const response = await fetch("https://ahmedianoo-ai-sales-assistant-backend.hf.space/reports/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error(`Failed to generate report. Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Generated report:", data);
      alert("✅ Report generated successfully!");
    } catch (err) {
      console.error("Error generating report:", err.message);
      alert("Error generating report: " + err.message);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return <div className="loading">Loading reports...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="reports-page" style={{ marginTop: "30px" }}>
      <div className="card">
        <h2 className="title">📑 Reports</h2>

        {/* Report Generator Section */}
        <div className="generator">
          <label htmlFor="competitor-select">Select Competitor</label>
          <select
            id="competitor-select"
            className="dropdown"
            value={selectedCompetitor?.user_comp_id || ""}
            onChange={(e) => {
              const val = parseInt(e.target.value); // convert to number
              const selected = competitors.find(
                (comp) => comp.user_comp_id === val
              );
              setSelectedCompetitor(selected || null);
            }}
          >
            <option value="">-- Choose Competitor --</option>
            {competitors.map((comp) => (
              <option
                key={comp.user_comp_id}
                value={comp.user_comp_id}
              >
                {comp.name ?? "Unnamed Competitor"} {/* fallback */}
              </option>
            ))}
          </select>




          <button
            className="btn-generate"
            onClick={handleGenerateReport}
            disabled={generating}
          >
            {generating ? "Generating..." : "Generate Report"}
          </button>
        </div>

        {/* Reports Display Section */}
        {reports.length === 0 ? (
          <p className="no-reports">No reports available.</p>
        ) : (
          <div className="reports-list">
            {reports.map((report) => {
              const reportText = report.metrics?.report_text || "No content available.";
              return (
                <div key={report.report_id} className="report-item">
                  <h3 className="report-type">{report.report_type}</h3>
                  <div
                    className="report-text"
                    dangerouslySetInnerHTML={{ __html: formatReportText(reportText) }}
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
