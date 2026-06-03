# Review of ASN-0098

## REVISE

### Issue 1: LP2★ is unused machinery subsumed by LP13
**ASN-0098, "Immutability of the Stored Link" / Claims table**: "**LP2★ — MultiStepSlotInvariance**: For every reachable state sequence `Σ →* Σ'` ... `a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ`"
**Problem**: LP2★ is introduced as a labeled claim but is consumed nowhere. Every downstream proof that needs persistence cites either single-step LP2 (LP12a: "using LP2 for `a ∈ dom(Σ'.L)`..."; the trace: "byte-identical (LP13, LP2)"), LP3★ (LP18), Store Monotonicity★ (LP18, LP19a), or LP13. LP13 — "full value equality of the stored link object, arity included" — strictly subsumes LP2★ (slot equality follows from full-value equality by component projection), and its own proof applies schema (★) directly to L12 rather than routing through LP2★. So LP2★ is redundant with a stronger sibling and has no consumer. By contrast its companion LP3★ *is* wired into LP18. This is exactly the unused-machinery pattern the anti-bloat mode targets.
**Required**: Either cite LP2★ at a real use site, or delete it and let LP13 (full value) plus single-step LP2 carry the slot-level reasoning.

### Issue 2: LP13 closing prose restates its own point in two forms
**ASN-0098, "Discoverability and Survival" (LP13)**: "Persistence requires only `a ∈ dom(Σ.L)` and is independent of arrangement state, whereas discoverability is arrangement-conditional (LP9–LP11). A holder can therefore rely on the stored object permanently, but not on discoverability from any particular document without further conditions on that document's arrangement."
**Problem**: The second sentence re-expresses the first verbatim in content — persistence unconditional, discoverability arrangement-conditional — re-skinned with the "holder" framing. This is the "two sentences say the same thing in different words" pattern; the precise reader reads the same claim twice.
**Required**: Keep the first sentence (the technical persistence/discoverability contrast) and drop the second, or fold the single "holder can rely" point into the first sentence without restating the conditionality split.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order reflection, cross-document operation equivalence
**Why out of scope**: These are correctly parked in "Open Questions" as future ASNs — they require new primitives (reverse lookup, V-order invariants under K.μ~) not defined by this note's state-and-projection vocabulary. No error here.

### Topic 2: Link-canonical contraction discoverability (final open question)
**Why out of scope**: The note explicitly notes the content-canonical disjointness argument (LP12b) inverts in the link subspace and defers the link-canonical case. Deferring is the right call; not a gap in this ASN.

VERDICT: REVISE
