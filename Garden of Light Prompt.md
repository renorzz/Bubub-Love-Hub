# 🌸 Garden of Light — Web Prompt

## Overview

Create a stunning interactive flower showcase website with a dark, cinematic aesthetic.
The page displays **3 bouquet clusters** — each containing many loose, layered flowers
of one species: **Lily**, **Peony**, and **Tulip**.

The flowers are **unwrapped and free-form** — no vase, no ribbon, no wrapper.
They are scattered and layered naturally on top of each other like flowers
tossed gently onto a dark surface, overlapping at various angles and depths.

---

## Flower Arrangement

- Each bouquet cluster contains **8–12 flowers** of the same species
- Flowers within a cluster are arranged at **random angles and slight offsets**,
  overlapping each other organically — some in front, some behind
- Use **z-index layering** and **size variation** (near flowers larger, far flowers smaller)
  to give a convincing sense of depth
- No vase, no wrap, no ribbon — just the **bare stems and blooms** loose on the black canvas
- Each cluster occupies roughly one third of the screen width
- Stems are **visible and natural**, crossing each other slightly within the cluster

---

## SVG Flower Design

- Each flower is a **detailed, multi-layered SVG** with realistic petal shapes
- Use **radial and linear gradients** inside petals for depth (light center fading to
  rich color at edges, or vice versa depending on species)
- **Lily**: long, curved trumpet petals with stamen detail, warm white to blush pink
- **Peony**: densely layered ruffled petals, deep rose pink with pale inner petals
- **Tulip**: smooth cupped petals, bold red/purple/orange with subtle sheen
- Leaves and stems rendered with natural curves and vein detail

---

## Lighting & Atmosphere

- **Pure black background** (`#000000`)
- Each cluster is lit by a **dramatic spotlight** — a soft radial gradient cone of
  warm white/golden light descending from above, hitting the topmost flowers
  and falling into shadow at the edges
- Flowers deeper in the cluster receive **less light** (darker fill, higher shadow opacity)
  to enhance the 3D bouquet feel
- A faint **bokeh particle field** floats across the entire background —
  small, softly blurred circles of light drifting slowly at different speeds and opacities
- Each cluster emits a very subtle **ambient bloom glow** around it

---

## Alive / Breathing Animation

- Every flower in the cluster **breathes independently** — petals slowly expand
  and contract on slightly offset timers using a smooth sine easing,
  so the whole bouquet ripples like it's alive
- The entire cluster **sways gently** as a unit — a slow drift left and right
  as if caught in a soft breeze, with each flower's sway offset slightly
  from its neighbors
- Petals have **micro-flutter**: individual petals rotate a tiny amount on their own
  timer, giving an organic, non-mechanical feel
- Stems **bend and recover** subtly in sync with the sway

---

## Interactivity — Click to Shake

- When the user **clicks or taps anywhere on a cluster**, all flowers in that cluster
  **burst and spring**: petals fan outward, then snap back with bouncy spring physics
  (`velocity`, `damping`, `stiffness` — tune for a satisfying elastic snap)
- The **spotlight flickers** briefly on click — a fast pulse of brightness then settles
- A burst of **light particles** (small glowing dots) explodes outward from the click point
  and fades out
- **Magnetic hover**: as the cursor approaches a cluster, the flowers nearest the cursor
  **lean slightly toward it**, creating a living, reactive field

---

## Layout & Typography

- Three clusters displayed **side by side** in a row on desktop, centered vertically
- On mobile, clusters **stack vertically** with proper spacing
- Below each cluster, an **elegant label** in serif font: *Lily*, *Peony*, *Tulip* —
  white, slightly transparent, softly glowing
- Page heading at top: **"Garden of Light"** — large, cinematic, letter-spaced,
  in a thin serif font with a subtle white glow text-shadow

---

## Technical Requirements

- **Pure HTML + CSS + JS** — no external libraries or frameworks
- SVG flowers written **inline** in the HTML with full gradient and shape detail
- Animation loop via `requestAnimationFrame` at smooth **60 fps**
- Spring physics implemented manually for the shake interaction
- **Responsive** layout using CSS Flexbox or Grid
- All interactivity handled with vanilla JS `click` and `mousemove` event listeners
