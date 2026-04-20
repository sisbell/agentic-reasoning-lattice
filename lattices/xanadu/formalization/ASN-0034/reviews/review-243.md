# Cone Review — ASN-0034/T10a.8 (cycle 8)

*2026-04-18 05:44*

### Axiom body undercounts the consequences it claims to establish

**Foundation**: The axiom's framing paragraph announces the proof plan for the numbered consequences that follow, and the ordinal count fixes how many load-bearing conclusions the axiom claims. Downstream readers (and any summary-level reasoning about the axiom's scope) rely on the stated count matching the enumerated proofs.

**ASN**: T10a's axiom body closes with: "We justify the constraint by establishing **seven consequences** on which the coordination-free uniqueness guarantees depend, then proving that the sibling restriction is necessary for prefix-incomparability." The body then enumerates Consequences 1 through 8 (Uniform sibling length, Non-nesting sibling prefixes, Length separation, T4 preservation, Cross-allocator prefix-incomparability, Domain disjointness, Enumeration injectivity, Uniform sibling zero count) followed by Necessity.

**Issue**: The announced count is seven; the enumerated list contains eight. The discrepancy aligns with T10a.8 (Uniform sibling zero count) having been introduced into the numbered consequences and the Formal Contract Postconditions block (T10a.1 through T10a.8) without a corresponding update to the axiom body's framing sentence. A reader matching the plan sentence against the enumeration finds the count one short, and any extractor keying on "seven" as a structural invariant will undercount the consequences T10a claims to deliver.

**What needs resolving**: The axiom body's framing sentence must report the correct count of consequences established in this ASN (eight as currently enumerated) — or, if the intent is to exclude one of the eight from the "coordination-free uniqueness" framing, the sentence must identify which one is excluded and why, so the announced count and the enumerated list agree exactly.

## Result

Cone not converged after 8 cycles.

*Elapsed: 3716s*
