// src/app/components/Navbar.js
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import ProfileIcon from "./icons/ProfileIcon";
import TextLogo from "./TextLogo";

export default function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { name: "AI Chat", path: "/home" },
    { name: "Reports", path: "/reports" },
    { name: "Battlecards", path: "/battlecards" },
    { name: "Competitors", path: "/competitors" },
    //{ name: "Profile", path: "/profile"},
    { name: "Profile", path: "/profile", isIcon: true },
  ];

  const pageBackgrounds = {
    "/": "beige",
    "/reports": "beige",
    "/battlecards": "beige",
    "/competitors": "beige",
    "/profile": "beige",
    "/login": "green",
    "/signup": "green",
  };

  const currentPageBg = pageBackgrounds[pathname] || "beige";
  const linkColor = currentPageBg === "beige" ? "var(--secondary-color)" : "var(--primary-bg)";

  return (
    <nav
      aria-label="Main navigation"
      style={{
        backgroundColor: "white",
        padding: "1rem",
        display: "flex",
        alignItems: "center",
        //justifyContent: "space-between",
        borderBottom: "1px solid #ddd",
        position: "fixed",
        top: 0,
        width: "100%",
        zIndex: 1000,
        boxSizing: "border-box"
      }}
    >
      <TextLogo />

      <ul style={{ listStyle: "none", 
          display: "flex", 
          gap: "1.5rem", 
          margin: 0, 
          padding: 0, 
          flexGrow: 1, // Takes up all available space
          justifyContent: "flex-end",
          flexShrink: 1, // allows it to shrink
          minWidth: 0,    // crucial for flexbox to allow shrinking
        }}>

        {navItems.map((item) => (
          <li key={item.path}>
            <Link
              href={item.path}
              style={{
                color: linkColor,
                textDecoration: "none",
                fontSize: "1.15rem"
              }}
            >
              {item.isIcon ? (
                <ProfileIcon style={{ width: "1.5rem", height: "1.5rem" }} />
              ) : (
                item.name
              )}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}