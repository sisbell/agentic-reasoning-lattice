# Review of ASN-0047

## REVISE

### Issue 1: Subspace-position correspondence cited as "S3★ + L0" but actually depends on S3★-aux
**ASN-0047, Notation (Subspace-position correspondence) and §Generalized referential integrity (S3★)**: "For `v ∈ dom(M(d))` with `M(d)(v) = a`, `subspace(v) = subspace_I(a)`; see S3★ + L0" — and the S3★ body: "S3★ alone yields only store *membership*, not equality of subspace identifiers; L0 supplies the second step."

**Problem**: S3★ is *conditional* — it routes the value only on the branches `subspace(v) = s_C` and `subspace(v) = s_L`, and is silent for any other first-component value. The two-step chain (S3★ → store membership → L0 → identifier) establishes `subspace(v) = subspace_I(a)` *within each branch*, but the universally-quantified correspondence over all `v ∈ dom(M(d))` requires that every V-position fall into one of those two branches. That is exactly S3★-aux (SubspaceExhaustiveness), which the citation omits. As stated, "S3★ + L0" is incomplete: "X follows from Y + Z" is a claim, and here the load-bearing third premise (S3★-aux) is missing from the derivation.

**Required**: Cite S3★ + L0 + S3★-aux, and add the one clause to the S3★ derivation noting that S3★-aux supplies the case-exhaustiveness that promotes the per-branch equality to the universal correspondence.

### Issue 2: Use-site inventory + forward deferral + role-clarification in K.μ~ admissibility
**ASN-0047, §Decomposition of K.μ~ (admissibility definition)**: "The enumerated clause-(i) set is the arrangement-*shape* package only; the remaining per-state arrangement invariants on `M'(d)` — S3★, S3★-aux, CL-OWN, CL-UNIQ, S2, and S8★ — are *not* admissibility hypotheses but derived consequences of clause (iv), fixity, and the bijection equation (per the *Composite-boundary verification matrix* below). (S3★-aux at the *pre-state* Σ is a separate matter: it is an inductive hypothesis consumed by Step (A), not a post-state filter on π — see Step (A) below.)"

**Problem**: This is forward-reference accretion of the kind this review mode is tasked to surface. The sentence does not advance the admissibility definition; it (a) inventories which invariants are *not* hypotheses, (b) defers their discharge to the matrix below, and (c) appends a defensive parenthetical preempting a confusion about S3★-aux's two roles with a second forward pointer ("see Step (A) below"). A reader following the admissibility clauses (i)–(iv) must skip past this to continue. The actual content — that those invariants are derived, not assumed — is already established where each is discharged (Step (B) for S3★, the matrix cells, the per-property prose).

**Required**: Delete the inventory-and-deferral sentence and the S3★-aux parenthetical from the admissibility definition. The discharge locations (Step (A)/(B), matrix) already carry the substance; the admissibility definition should state clauses (i)–(iv) and stop.

### Issue 3: P4a definition box carries rationale-essay alongside the definition
**ASN-0047, P4a definition box**: "This trace-existential reading is the design-correct one: provenance rides on the permanent I-address and survives deletion from the current arrangement, so the witness is whatever historical version contained the content, not a live moment-of-recording check (Nelson, LM 4/9, 4/11 — ...)."

**Problem**: The classification of P4a as a trace property and its formal statement are load-bearing and belong here. But the "is the design-correct one" justification is essay content defending the classification choice rather than stating it — the structural-slot meta-prose pattern. The Nelson grounding for *what* provenance tracks is fine; the editorializing about correctness of the *reading* is not. (The adjacent "The content-subspace qualification is essential" sentence is genuine — it states what the qualification does — and should stay.)

**Required**: Trim "This trace-existential reading is the design-correct one:" framing to a plain statement of the witnessing semantics with its Nelson citation; drop the correctness editorializing.

## OUT_OF_SCOPE

### Topic 1: Mid-arrangement INSERT semantics
K.μ⁺ is append-only (existing mappings fixed + D-CTG★ forces new positions at the top); mid-sequence INSERT requires a K.μ⁻ + K.μ⁺ reordering composite. This is correct given that named operations (INSERT) are explicitly out of scope; not an error in this ASN.

### Topic 2: Link-withdrawal / tombstoning mechanism
The tension between D-CTG★/D-MIN★ suffix-only link contraction and Nelson's tombstoning (LM 4/9) is correctly deferred to the Open Questions; a separate withdrawal mechanism is future territory.

VERDICT: REVISE
