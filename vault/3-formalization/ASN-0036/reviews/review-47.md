# Cone Review — ASN-0036/S5 (cycle 2)

*2026-04-13 15:23*

I'll read the full ASN carefully, tracking definitions, quantifier scopes, and cross-property dependencies.

**Properties shown:** S0 (axiom), S1 (from S0), S2 (axiom), S3 (invariant), S5 (consistency claim).
**Properties referenced but not shown:** S4, S6, S7+.
**Shared axiom:** AX-1 (initial empty arrangement).

**Dependency chain:** S0 → S1 → S3 (via Case 1); AX-1 → S3 (base case); S0+S1+S2+S3+S4+S6 → S5 (conforming trace).

Let me trace the formal contracts and proofs against each other.

---

### AX-1 constrains arrangements but S5 proof extracts initial content-store emptiness from it

**Foundation**: (internal — foundation ASN)

**ASN**: S5 proof, cross-document construction: "Σ₀: The initial state. By AX-1, dom(Σ₀.M(d)) = ∅ for all documents d, **and dom(Σ₀.C) = ∅**." Same claim in the within-document construction: "Σ₀: The initial state (AX-1). dom(Σ₀.M(d)) = ∅ for all d, **and dom(Σ₀.C) = ∅**."

**Issue**: AX-1 as defined in S3's formal contract is "initial empty arrangement — `dom(Σ₀.M(d)) = ∅` for all `d`." It constrains the arrangement component M only. Both S5 constructions assert `dom(Σ₀.C) = ∅` as a consequence of AX-1, but this does not follow — AX-1 says nothing about the content store. The proof depends on this ungrounded claim in at least four places: (1) defining `Σ₁.C = {a ↦ w}` as the complete content store rather than `Σ₀.C ∪ {a ↦ w}`; (2) S0 verification at `Σ₀ → Σ₁` ("dom(Σ₀.C) = ∅, so the universal quantification holds vacuously"); (3) S1 verification at `Σ₀ → Σ₁` ("`dom(Σ₀.C) = ∅ ⊆ {a}`"); (4) S6 verification at `Σ₀ → Σ₁` ("`dom(Σ₀.C) = ∅`, so the implication holds vacuously"). If `dom(Σ₀.C)` were non-empty, the first transition would need to preserve all pre-existing content (S0 obligation), include pre-existing addresses in the domain comparison (S1), and check persistence independence for existing content (S6) — none of which the proof addresses.

**What needs resolving**: Either expand AX-1 to also specify the initial content store (e.g., `dom(Σ₀.C) = ∅`), or introduce a separate initial-state axiom for `C`, or rewrite the S5 constructions to work for arbitrary `Σ₀.C` (by allocating `a ∉ dom(Σ₀.C)` and defining `Σ₁.C = Σ₀.C ∪ {a ↦ w}`). The first option is simplest and aligns with the proof's apparent intent; the current phrasing "initial empty arrangement" names only half of what the proofs require from the initial state.
