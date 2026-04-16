# Cone Review — ASN-0034/TA1 (cycle 2)

*2026-04-15 23:56*

### T0 cited as carrier set foundation but never stated in the ASN
**Foundation**: N/A — the missing property *is* the foundation
**ASN**: T3 proof: "By T0, T is the set of all finite sequences over ℕ"; TumblerAdd proof: "a finite sequence over ℕ with length ≥ 1, hence `a ⊕ w ∈ T` by T0"
**Issue**: T0 is invoked at least twice by name — once to ground T3 as an axiom ("T3 is not derived from other properties; it holds by the definition of the carrier set. By T0, T is the set of all finite sequences over ℕ") and once in TumblerAdd to justify closure (`a ⊕ w ∈ T`). Yet T0 has no statement, no formal contract, and no axiom declaration anywhere in the ASN. Without T0, the carrier set T is undefined: it is unclear whether the empty sequence is in T, whether sequences must be non-empty, or what properties of ℕ the carrier inherits. T3 claims to hold "by definition of the carrier set," but that definition is absent. Every property in the ASN ultimately rests on membership in T, so the entire formal chain is anchored to an unstated premise.
**What needs resolving**: T0 must be given a formal statement and contract — at minimum specifying T as a set of finite sequences over ℕ and whether a minimum length (e.g., `#a ≥ 1`) is imposed. Every property that invokes T0 must then declare the dependency.

---

### T1 formally depends on T3 but is stated and proven before T3 exists
**Foundation**: T3 (CanonicalRepresentation) — axiom
**ASN**: T1 formal contract: "Depends: T3 (CanonicalRepresentation)"; T1 proof Case 1: "so `a = b` by T3"; T1 proof Case 3: "we have `a ≠ b` by T3 (distinct lengths)"
**Issue**: T1's formal contract explicitly declares `Depends: T3`, and the proof invokes T3 in two of the three trichotomy cases — Case 1 uses T3 forward (component-wise agreement implies equality) and Case 3 uses T3 contrapositive (length difference implies inequality). But T3 is defined in the "Canonical form" section that appears *after* the entire T1 proof. The declared dependency runs forward in document order. Unlike the TA0/TumblerAdd issue (previous finding #2), where undefined *symbols* are used, here the *logical content* of T3 is paraphrased inline, so the proof is followable. But the formal contract creates a specific obligation: "Depends: T3" asserts that T3 is available, and it is not available at that point. For TLA+ formalization, the T3 axiom must be declared before T1's proof module can import it.
**What needs resolving**: Either T3 must precede T1 in the document (natural, since T3 is an axiom and T1 is a theorem that depends on it), or the forward reference must be explicitly flagged as such rather than presented as a satisfied dependency.

---

### TA0 and TA1 formal contracts omit dependency declarations despite proof-level citations
**Foundation**: N/A — formal contract completeness
**ASN**: TA0 proof: "By TumblerAdd, each component of the result lies in ℕ"; TA1 proof: "By TA0, both `a ⊕ w` and `b ⊕ w` are well-defined," "By TumblerAdd, the operation `⊕` builds the result in three regions," "T1 provides exactly two cases," "`a ⊕ w = b ⊕ w` by T3"
**Issue**: T1 and TumblerAdd both include `Depends` fields in their formal contracts (T1 declares T3; TumblerAdd declares T1 and T3). TA0 and TA1 have no `Depends` field at all, despite their proofs explicitly invoking other properties by name. Specifically: TA0's proof delegates entirely to TumblerAdd, yet its contract is silent on this dependency. TA1's proof cites four distinct properties — TA0 (well-definedness), TumblerAdd (piecewise structure), T1 (case analysis on ordering), and T3 (equality from component agreement) — yet its contract declares none. This makes the dependency graph unrecoverable from contracts alone. A change to any of T1, T3, TA0, or TumblerAdd could invalidate TA1's proof, but the contract gives no indication of which properties are load-bearing. TumblerAdd also omits T0 from its Depends despite invoking T0 for carrier-set membership.
**What needs resolving**: Every formal contract must include a `Depends` field listing every property whose statement or postcondition the proof invokes. The convention should be uniform across all properties in the ASN — either every contract declares its dependencies, or none does (in which case the dependency graph must be maintained elsewhere).
