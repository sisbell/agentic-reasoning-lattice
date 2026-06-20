# Decompose Module Design into Per-Method Units

You are analyzing a converged module design and decomposing it into one
self-contained unit per public method. Each unit is the *only* thing a later
stage will read to derive that method's formal contract — so it must gather,
from across the whole design, everything about that method and nothing about any
other. Output ONLY valid YAML. No commentary, no code fences, no explanation.

## What to extract, per method

For every public method/function in the design's Public Interface (every `pub fn`
/ trait method / associated function — including constructors and accessors),
produce one entry with:

- **label** — the method's idiomatic name exactly as declared (`inc`, `from_endpoints`,
  `same_account`). For a method on a type, use the bare method name.
- **signature** — the Rust signature VERBATIM from the Public Interface (do not
  retype, rename, or normalize types). One line.
- **algorithm** — the design's prose describing HOW this method computes, gathered
  from the Internal Design sections (and any algorithm shown inline in the
  interface). Quote the relevant text faithfully; do not summarize away bounds,
  cases, or conditions. If the design gives no algorithm beyond the signature
  doc-comment, include that doc-comment.
- **invariants** — the specific invariants this method establishes or preserves,
  pulled from the Invariants/Contracts section (e.g. "preserves carrier InT but
  not T4 validity"; "every result Run has width ≥ 1"). Only the ones that touch
  this method; omit the rest.
- **calls** — the OTHER methods in THIS design that this method's algorithm
  invokes (intra-module callees, by their `label`). These fix the derivation
  order and are the preconditions the contract must discharge. Empty list for a
  leaf. Do NOT list upstream-module calls (those are external), only same-module.

## YAML structure

```yaml
module: <module id, e.g. M1>
methods:
  - label: <method name>
    signature: <verbatim Rust signature, one line>
    algorithm: |
      <faithful prose / pseudo-code from the Internal Design for this method>
    invariants: |
      <the invariants this method establishes or preserves; omit if none stated>
    calls: [<intra-module callee labels>]
```

## Rules

1. One entry per public method. Do not invent methods not in the interface; do not
   merge two methods into one entry.
2. Quote faithfully — preserve exact bounds, quantifiers, case splits, error
   conditions. A later stage derives a CONTRACT from this; vagueness loses rigor.
3. `calls` lists only same-module callees, by their method label. If the algorithm
   says "via `sub`" or "= from_endpoints(p, shift(p,1))", list `sub` /
   `from_endpoints` / `shift`. Resolve to the bare method name.
4. Gather each method's material from WHEREVER it appears in the design — the
   signature from the interface, the algorithm from Internal Design, the invariant
   from the Invariants section. The unit must stand alone.
5. Preserve the original wording in algorithm/invariants; do not rewrite or
   editorialize.

## Module design to decompose

Module: **{{module_id}}**

{{design}}
