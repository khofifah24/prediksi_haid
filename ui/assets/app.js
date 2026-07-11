/* ============================================================
   Layout bersama + helper. Menyuntik sidebar + topbar ke tiap halaman.
   Panggil: layout("Judul", "subjudul", "key-halaman-aktif")
   ============================================================ */

const NAV_ITEMS = [
  { key: "dashboard",  href: "index.html",      label: "Dashboard",       icon: iconGrid() },
  { key: "santriwati", href: "santriwati.html", label: "Data Santriwati", icon: iconUsers() },
  { key: "proses",     href: "proses.html",     label: "Proses D-Tree",   icon: iconCpu() },
  { key: "pengujian",  href: "pengujian.html",  label: "Pengujian",       icon: iconFlask() },
  { key: "evaluasi",   href: "evaluasi.html",   label: "Evaluasi Model",  icon: iconChart() },
];

/* ---- Dark mode: baca preferensi tersimpan sebelum render ---- */
(function initTheme() {
  const saved = localStorage.getItem("ph-theme");
  const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  if (saved === "dark" || (!saved && prefersDark)) document.documentElement.classList.add("dark");
})();

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle("dark");
  localStorage.setItem("ph-theme", isDark ? "dark" : "light");
  document.getElementById("theme-icon").innerHTML = isDark ? iconSun() : iconMoon();
  document.dispatchEvent(new CustomEvent("themechange", { detail: { dark: isDark } }));
}

function layout(pageTitle, subtitle, activeKey) {
  const isDark = document.documentElement.classList.contains("dark");
  const nav = NAV_ITEMS.map((it) => `
    <a href="${it.href}"
       class="nav-link ${it.key === activeKey ? "active" : ""}
              flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[0.9rem]"
       style="color:${it.key === activeKey ? "" : "var(--ink-2)"}">
      <span class="w-5 h-5 shrink-0">${it.icon}</span>${it.label}
    </a>`).join("");

  document.getElementById("app").innerHTML = `
    <div class="flex min-h-screen">
      <!-- SIDEBAR -->
      <aside class="w-[256px] shrink-0 hidden lg:flex flex-col sticky top-0 h-screen"
             style="background:var(--surface);border-right:1px solid var(--line)">
        <div class="h-16 flex items-center gap-2.5 px-5" style="border-bottom:1px solid var(--line)">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center text-white"
               style="background:linear-gradient(135deg,var(--primary),var(--primary-600))">
            <span class="w-5 h-5">${iconPulse()}</span>
          </div>
          <div class="leading-tight">
            <p class="font-bold text-[0.95rem]" style="color:var(--ink)">Prediksi Haid</p>
            <p class="text-[0.7rem]" style="color:var(--muted)">Decision Tree · KDD</p>
          </div>
        </div>
        <nav class="p-3 space-y-1 flex-1 overflow-y-auto">
          <p class="px-3.5 pt-2 pb-1.5 text-[0.68rem] font-semibold tracking-wider" style="color:var(--muted)">MENU</p>
          ${nav}
        </nav>
        <div class="p-3" style="border-top:1px solid var(--line)">
          <a href="login.html" class="nav-link flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-[0.9rem]" style="color:var(--ink-2)">
            <span class="w-5 h-5">${iconLogout()}</span>Keluar
          </a>
          <div class="mt-2 px-3.5 py-2 rounded-xl text-[0.7rem] leading-relaxed"
               style="background:rgb(245 158 11 / 0.10);color:var(--takteratur)">
            ⓘ Prediksi berbasis data, bukan diagnosis medis.
          </div>
        </div>
      </aside>

      <!-- KONTEN -->
      <div class="flex-1 flex flex-col min-w-0">
        <header class="h-16 flex items-center justify-between px-5 sm:px-7 sticky top-0 z-20"
                style="background:color-mix(in srgb, var(--surface) 82%, transparent);
                       backdrop-filter:blur(10px);border-bottom:1px solid var(--line)">
          <div class="min-w-0">
            <h1 class="text-[1.05rem] sm:text-[1.2rem] font-bold truncate" style="color:var(--ink)">${pageTitle}</h1>
            ${subtitle ? `<p class="text-[0.78rem] truncate" style="color:var(--muted)">${subtitle}</p>` : ""}
          </div>
          <div class="flex items-center gap-2">
            <button onclick="toggleTheme()" title="Ganti tema"
                    class="w-9 h-9 rounded-xl flex items-center justify-center btn-ghost">
              <span id="theme-icon" class="w-[18px] h-[18px]">${isDark ? iconSun() : iconMoon()}</span>
            </button>
            <div class="hidden sm:flex items-center gap-2.5 pl-2 pr-1 py-1 rounded-xl" style="border:1px solid var(--line)">
              <div class="w-7 h-7 rounded-lg flex items-center justify-center text-white text-[0.7rem] font-bold"
                   style="background:linear-gradient(135deg,var(--primary),var(--primary-600))">OP</div>
              <span class="text-[0.82rem] font-medium pr-1" style="color:var(--ink-2)">Operator</span>
            </div>
          </div>
        </header>
        <main class="flex-1 p-5 sm:p-7 max-w-[1400px] w-full mx-auto" id="page"></main>
      </div>
    </div>`;
}

/* ---- Data helpers ---- */
async function loadReport(name) {
  try {
    const res = await fetch(`../reports/${name}`, { cache: "no-store" });
    if (!res.ok) return null;
    return await res.json();
  } catch { return null; }
}

function statusBadge(value) {
  const teratur = value === 1 || value === "1" || /^teratur/i.test(String(value));
  return teratur
    ? `<span class="badge badge-teratur"><span class="dot"></span>Teratur</span>`
    : `<span class="badge badge-takteratur"><span class="dot"></span>Tidak Teratur</span>`;
}

function emptyState(title, msg, cta) {
  return `<div class="card p-10 text-center fade-up">
    <div class="w-14 h-14 mx-auto rounded-2xl flex items-center justify-center mb-4"
         style="background:rgb(13 148 136 / 0.10);color:var(--primary)">
      <span class="w-7 h-7 inline-block">${iconInbox()}</span></div>
    <p class="font-semibold text-[1rem]" style="color:var(--ink)">${title}</p>
    <p class="text-[0.85rem] mt-1 mb-4" style="color:var(--muted)">${msg}</p>
    ${cta || ""}
  </div>`;
}

/* ---- Warna dinamis untuk Chart.js (ikut token) ---- */
function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
function chartColors() {
  return {
    teratur: cssVar("--teratur"), takteratur: cssVar("--takteratur"),
    primary: cssVar("--primary"), ink: cssVar("--ink"),
    ink2: cssVar("--ink-2"), muted: cssVar("--muted"), line: cssVar("--line"),
    surface: cssVar("--surface"),
  };
}

/* ---- Ikon SVG (stroke currentColor) ---- */
function svg(p){return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="w-full h-full">${p}</svg>`;}
function iconGrid(){return svg('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>');}
function iconUsers(){return svg('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>');}
function iconCpu(){return svg('<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3"/>');}
function iconFlask(){return svg('<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7 15h10"/>');}
function iconChart(){return svg('<path d="M3 3v18h18"/><rect x="7" y="12" width="3" height="6" rx="1"/><rect x="12" y="8" width="3" height="10" rx="1"/><rect x="17" y="5" width="3" height="13" rx="1"/>');}
function iconPulse(){return svg('<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>');}
function iconLogout(){return svg('<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5M21 12H9"/>');}
function iconMoon(){return svg('<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>');}
function iconSun(){return svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>');}
function iconInbox(){return svg('<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>');}
