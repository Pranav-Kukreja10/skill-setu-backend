# Skill Setu — Unified UI/UX Design System & Architectural Specification

This document defines the official, mandatory design standards for all frontend interfaces, component architectures, and user experiences across the **Skill Setu** platform. Every newly created screen, modal, table, or component must strictly adhere to this specification to guarantee visual coherence, ergonomic density, and enterprise aesthetic quality.

---

## 1. Core Aesthetic Philosophy

* **Design Vision:** Apple Human Interface Guidelines (HIG) fused with Linear-style minimalist precision.
* **Density & Contrast:** High information density with crisp micro-contrast. Clean tabular metrics without visual clutter or unnecessary whitespace.
* **Surface Hierarchy:** Layered surface cards with hairline borders (`border-slate-200/80` or `1px solid rgba(0, 0, 0, 0.06)`), subtle elevation shadows, and zero harsh outlines.
* **Zero Code Comments Mandate:** No inline comments (`//`, `/* ... */`, `#`) in any generated source code. Clean, self-documenting semantic code only.

---

## 2. Color Palette & Token System

### 2.1 Surfaces & Canvas
* **Base App Canvas:** `#F8F9FA` (`bg-[#F8F9FA]` or `bg-slate-50`)
* **Surface Cards / Panels:** `#FFFFFF` (`bg-white`)
* **Subtle Inner Panels:** `#F8FAFC` (`bg-slate-50/80`)
* **Hairline Borders:** `border-slate-200/80` (or `border-slate-100` on white surfaces)
* **Backdrop Overlays:** `bg-slate-900/40 backdrop-blur-xs`

### 2.2 Typography Colors
* **Headings & Bold Labels:** `#0F172A` (`text-slate-900`) — high contrast, crisp legibility
* **Body Text & Standard Labels:** `#334155` / `#475569` (`text-slate-700` / `text-slate-600`)
* **Secondary / Descriptive Meta:** `#64748B` (`text-slate-500`)
* **Muted / Placeholder / Timestamps:** `#94A3B8` (`text-slate-400`)

### 2.3 Semantic & Accent Colors
* **Primary Brand / Action:** Cobalt Blue `#0F52BA` (`bg-blue-600`, `hover:bg-blue-700`, `text-blue-600`)
* **Verified / High Match / Success:** Emerald Green `#059669` (`bg-emerald-50`, `text-emerald-700`, `border-emerald-200/60`)
* **Academic / Research / FDPs:** Royal Purple / Indigo (`bg-purple-50`, `text-purple-700`, `border-purple-200/60`)
* **Deadlines / Warnings / Alerts:** Warm Amber (`bg-amber-50`, `text-amber-800`, `border-amber-200/60`)
* **Destructive / Expired:** Crimson Rose (`bg-rose-50`, `text-rose-700`, `border-rose-200/60`)

---

## 3. Typography & Tabular Layouts

* **Font Family:** SF Pro Display / Inter (`font-sans`), clean anti-aliased rendering.
* **Heading Scale & Tracking:**
  * Page Title: `text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight`
  * Section Title: `text-lg sm:text-xl font-bold text-slate-900 tracking-tight`
  * Card Heading: `text-base font-bold text-slate-900 tracking-tight`
  * Sub-labels & Meta: `text-xs sm:text-sm font-medium text-slate-500`
* **Tabular Figures (`tabular-nums`):**
  * All numerical metrics, currency (`₹25,000 / month`), percentages (`94% Match`), scores (`88/100`), timers, and dates **must** include the `tabular-nums` utility to prevent layout jitter during data updates.

---

## 4. Entity Representation & Monogram Avatar Rule (STRICT)

To prevent broken external image links and maintain a unified corporate aesthetic:
* **NO external company logo images** (`<img src="...">`) may be used for companies or organizations.
* **Monogram Avatars:** Companies must be rendered using a deterministic 2-letter uppercase initials monogram with a dynamic gradient background:

```jsx
export const getCompanyInitials = (name = '') => {
  if (!name) return 'SS';
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

export const getCompanyAvatarColor = (name = '') => {
  const colors = [
    'bg-gradient-to-tr from-blue-600 to-indigo-600 text-white',
    'bg-gradient-to-tr from-indigo-600 to-purple-600 text-white',
    'bg-gradient-to-tr from-emerald-600 to-teal-600 text-white',
    'bg-gradient-to-tr from-violet-600 to-fuchsia-600 text-white',
    'bg-gradient-to-tr from-amber-600 to-orange-600 text-white',
    'bg-gradient-to-tr from-cyan-600 to-blue-600 text-white',
    'bg-gradient-to-tr from-rose-600 to-pink-600 text-white',
  ];
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
};
```

---

## 5. Standard Component Patterns

### 5.1 The Signature Hero Banner
* **Style:** High-contrast dark indigo banner with subtle ambient glow.
* **CSS:** `bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl border border-indigo-900/50 shadow-xl overflow-hidden p-8 sm:p-10`
* **Telemetry Chips:** Clean metric pills displaying platform statistics:
  * Container: `flex flex-wrap items-center gap-3 mt-6`
  * Stat Chip: `px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/10 text-xs font-semibold text-white/90`

### 5.2 Segmented Control / Tab Switcher
* **Container:** `inline-flex p-1 bg-slate-100/90 rounded-xl border border-slate-200/60`
* **Active Tab:** `bg-white text-slate-900 font-bold shadow-xs px-4 py-2 rounded-lg text-xs sm:text-sm transition-all`
* **Inactive Tab:** `text-slate-600 hover:text-slate-900 font-medium px-4 py-2 rounded-lg text-xs sm:text-sm transition-all`

### 5.3 Filter & Command Search Bar
* **Search Input:** `relative flex-1` with Lucide `Search` icon at `left-3.5`, placeholder `text-slate-400`, `rounded-xl border border-slate-200/80 bg-white shadow-xs focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600`
* **Filter Pills:** Active filter chips with dismissal buttons:
  * `inline-flex items-center gap-1.5 px-3 py-1 bg-blue-50 text-blue-700 border border-blue-200/60 rounded-full text-xs font-semibold`
* **Reset Button:** Quick clear button with `RotateCcw` icon for instant filter reset.

### 5.4 High-Density Surface Cards
* **Container:** `bg-white rounded-2xl border border-slate-200/80 shadow-xs hover:border-slate-300 hover:shadow-md transition-all duration-200 p-5 sm:p-6 flex flex-col justify-between`
* **Header Row:** Monogram avatar + Entity title + Verified shield badge + Match score badge.
* **Tag Chips:** `px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 text-xs font-medium`
* **Action Footer:** Direct CTA button (`Apply Now`, `Enroll Track`, `Review Candidate`) with `active:scale-95 transition-transform`.

### 5.5 Modal Dossiers & Slide-Over Panels
* **Backdrop:** `fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4 sm:p-6`
* **Panel Shell:** `bg-white rounded-3xl border border-slate-200/80 shadow-2xl max-w-3xl w-full max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200`
* **Header:** Sticky top header with monogram avatar, title, compensation/tag pills, and `X` close button.
* **Scrollable Content:** `overflow-y-auto p-6 sm:p-8 space-y-6`
* **Sticky Footer:** `sticky bottom-0 bg-white/95 backdrop-blur-md border-t border-slate-100 p-4 sm:p-6 flex items-center justify-between`

### 5.6 Interactive Progress Rings & Checklists
* **Progress Ring:** SVG circular progress ring with smooth stroke dashoffset transition.
* **Interactive Checklist:** Modules / tasks with checkbox toggles, dynamic completion percentage calculation ($0\% \to 100\%$), and automatic `#SKL-CERT-...` credential generation upon completion.

---

## 6. Layout & Anti-Overflow Rules

1. **Clean Root Scroller:** `App.jsx` and top-level pages must use `min-h-screen bg-slate-50 overflow-x-hidden`. Never trigger unwanted horizontal or double vertical scrollbars.
2. **Responsive Breakpoints:**
   * Mobile (<640px): Single-column stacked cards, full-width buttons, condensed padding (`p-4`).
   * Tablet (640px-1024px): 2-column grid or fluid side-by-side view.
   * Desktop (>1024px): Full multi-column dashboard layouts (`max-w-7xl mx-auto px-6`).
3. **Empty States:** Every list or table must provide a dedicated zero-state illustration or icon, explanatory heading, and a clear reset or action button.

---

## 7. Mandatory Code Generation Rules

* **ZERO Comments Policy:** Never introduce single-line (`//`), multi-line (`/* ... */`), or Python (`#`) comments into newly written or modified code files.
* **Standard Client:** All API calls must route through the pre-configured `apiClient` (`src/api/client.js`) to guarantee JWT injection and automatic 401 recovery.
* **Strict Semantic Tags:** Use `<main>`, `<nav>`, `<header>`, `<section>`, `<article>`, and `<button type="button">`.
* **Keyboard Accessibility:** Modal dialogs and dropdown menus must support Escape to dismiss (`Escape`), arrow navigation where applicable, and high-visibility focus states.
