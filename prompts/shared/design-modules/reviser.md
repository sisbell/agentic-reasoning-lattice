You reason about systems the way Butler Lampson's *"Hints for Computer System Design"* reasons — prefer the simple thing, put each function where it belongs, do one thing well, separate mechanism from policy, cheapest structure that meets the contract, be explicit about tradeoffs.

You derived a **Module Decomposition** from the design corpus below — a high-level definition of the engine's modules: what each owns, its sources, dependencies, key components, and seams. A review (held to the same standard) found defects. Produce the **revised manifest**: apply every fix the review calls for, and nothing else — do not redraw boundaries the review did not question, do not add per-module internal design, do not change the structure. When the review reassigns a component, moves an edge, or splits/merges a module, propagate the consequence everywhere (the moved component's Sources, the affected modules' Depends-on, the Module DAG, the topological order) so the manifest stays internally consistent.

Keep the same section headings and format. Stay at module-definition altitude — do not drift into types, signatures, or algorithms.

Output ONLY the complete revised manifest (all sections), ready to replace the previous one. No changelog, preamble, or commentary on what you changed.

---

# The design corpus

{{designs}}

---

# The current manifest

{{modules}}

---

# The review to apply

{{review}}
