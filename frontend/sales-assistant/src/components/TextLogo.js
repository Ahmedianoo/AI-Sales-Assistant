// src/app/components/TextLogo.js
import Link from 'next/link';
import React from 'react';

export default function TextLogo() {
  return (
    <div>
    <Link 
      href="/"
      style={{
        fontWeight: "bold",
        color: "var(--accent-color)",
        fontSize: "1.45rem",
        maxWidth: "200px"
      }}
    >
      AI Sales Assistant
    </Link>
    </div>
  );
}