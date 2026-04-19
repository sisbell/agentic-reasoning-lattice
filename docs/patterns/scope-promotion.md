# Scope Promotion

## Pattern

An agent investigating one topic encounters something related but outside the current scope. Including it would make the investigation unfocused. Ignoring it would lose a genuine discovery. The agent marks it as out of scope — a boundary observation that acknowledges the finding without expanding the current work.

The out-of-scope item sits at the edge of the investigation until something promotes it: a new investigation is created with its own scope, its own authority, and its own place in the lattice. What was a marginal note becomes a first-class node.

This is how the lattice grows outward. Not by expanding existing documents, but by spawning new ones from the boundaries of what exists.

## Forces

- **Investigation has natural boundaries.** An agent focused on the state model encounters allocation discipline. An agent focused on baptism encounters conformance to external claims. Following every thread makes the investigation unbounded.
- **LLMs self-narrow.** When an agent marks something out of scope, it is constraining itself — keeping focus on its assigned topic while preserving the finding for the system. This is productive self-discipline, not a limitation.
- **Out-of-scope findings are real discoveries.** They represent topics the lattice doesn't cover yet. Each one is a signal that the lattice has a gap at its edge.
- **Ignoring boundaries loses growth.** If out-of-scope items aren't captured, the lattice only grows through deliberate planning. Promotion lets it grow organically from what investigation reveals.

## Structure

```
investigation of topic A
  │
  ├── finding 1 (in scope) → refine A
  ├── finding 2 (in scope) → refine A
  └── finding 3 (out of scope) → mark as boundary observation
                                    │
                              scope promotion
                                    │
                              new investigation B
                                    │
                              B enters the lattice
```

The boundary observation captures enough context to seed the new investigation: what was found, why it matters, what it connects to. The promotion step turns this seed into a scoped inquiry with its own authority channels.

## When it works

- The out-of-scope finding is specific enough to define a new investigation's scope
- The connection to the existing lattice is clear (the new node depends on or is depended upon by existing nodes)
- The system has a mechanism to capture and act on boundary observations rather than discarding them

## When it fails

- Out-of-scope items are too vague to seed a real investigation ("future work" with no specifics)
- Promotion happens too eagerly — every tangential observation becomes a new node, fragmenting the lattice
- No one reviews the out-of-scope items — they accumulate as dead notes

## Leads to

[Reasoning lattice](reasoning-lattice.md) — scope promotion is how the lattice grows outward. Extract/absorb grows it downward (shared concepts sink). Scope promotion grows it at the edges (boundary discoveries become new nodes).

[Scoped inquiry](scoped-inquiry.md) — the promoted item becomes the seed for a new scoped inquiry. The boundary observation defines the question; scoped inquiry decomposes it for the authority channels.

## Applications

### ASN-0040 T10a conformance

During full-review of ASN-0040 (Tumbler Baptism), the reviewer found:

> "Stating 'baptism conforms to T10a' as a formal claim would close the bridge between the algebraic and set-theoretic developments, but this is a future convenience, not an error in this ASN."

This is a boundary observation — T10a conformance is real, relevant, and outside ASN-0040's scope. Promoting it would create a new ASN (or a new claim in an existing ASN) that formally establishes the bridge between baptism and allocator discipline.

### Integration issues as scope promotions

The integration issues found during discovery runs — T10a conformance, S7c analogs, GlobalUniqueness citation, backward shift, state model overlap, δ=1 edge case — are all out-of-scope findings from individual ASN investigations. Each one is a candidate for scope promotion: a gap at the edge of the lattice that a new investigation could fill.

### Open questions sections

Each ASN's `_open-questions.md` file captures boundary observations from discovery and formalization. These are the raw material for scope promotion — findings that the current investigation acknowledged but didn't pursue. The lattice grows when these are promoted to their own investigations.

## Origin

Observed from the first discovery runs. ASN reviews consistently produced findings marked as out of scope — topics related to the ASN but beyond its boundaries. Initially these were captured in open-questions files and forgotten. The pattern was recognized when the same out-of-scope item appeared in multiple ASN reviews — a signal that the lattice had a real gap that no single ASN would fill. Promoting these items to their own investigations became the primary mechanism for lattice growth.
