/* ============================================================
   Konfigurasi tema Tailwind (Play CDN) — dimuat SETELAH cdn.tailwindcss.com.
   Memusatkan palet & token agar seluruh halaman konsisten.
   ============================================================ */
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Primary — teal kalem (konteks kesehatan & pesantren)
        primary: {
          50: "#f0fdfa", 100: "#ccfbf1", 200: "#99f6e4", 300: "#5eead4",
          400: "#2dd4bf", 500: "#14b8a6", 600: "#0d9488", 700: "#0f766e",
          800: "#115e59", 900: "#134e4a",
        },
        // Semantik kelas — divalidasi CVD-safe (hijau ↔ amber, ΔE 46)
        teratur:    { light: "#10b981", DEFAULT: "#059669", dark: "#047857" },
        takteratur: { light: "#f59e0b", DEFAULT: "#d97706", dark: "#b45309" },
      },
      fontFamily: {
        sans: ["Inter", "Plus Jakarta Sans", "system-ui", "sans-serif"],
      },
      boxShadow: {
        soft: "0 1px 2px 0 rgb(16 24 40 / 0.04), 0 1px 3px 0 rgb(16 24 40 / 0.06)",
        card: "0 1px 3px rgb(16 24 40 / 0.05), 0 8px 24px -12px rgb(16 24 40 / 0.12)",
        pop: "0 12px 32px -8px rgb(13 148 136 / 0.28)",
      },
      borderRadius: { xl: "0.9rem", "2xl": "1.15rem" },
    },
  },
};
