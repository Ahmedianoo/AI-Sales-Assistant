// src/app/components/TextLogo.js
import React from 'react';
import Link from "next/link";

export default function TextLogo() {
  return (
    <Link 
      href={'/'}
      style={{
        fontWeight: "bold",
        color: "var(--accent-color)",
        fontSize: "1.45rem",
        maxWidth: "200px"
      }}
    >
      AI Sales Assistant
    </Link>
  );
}