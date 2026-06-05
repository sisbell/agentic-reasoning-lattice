# Review of ASN-0101

I checked the operation specification (D0), the gap-closure algebra (D1), the eight preservation claims (D2–D8), the projection characterisation and wp analysis (D9–D10), the composite-validity extension (D11), all six boundary cases, and the three worked examples against the foundation contracts.

The correctness core is sound. The shift-inverse construction is well-typed (TS2 at length `m_S`), D1's order-preserving bijection generalises ASN-0082's D-BJ cleanly to arbitrary depth, the D8 source-correspondence argument correctly handles the re-mapping at `Q ∩ X` positions (where a surviving V-position carries a different I-address), and the S8★ condition-(c) discharge via ASN-0058 M12/C1a restricted to the content subspace is properly routed. Edge cases are exhaustively covered and the wp computations are non-trivial (the `project ⊆ X` orphaning test is genuinely sharp). I found no hand-waved proof, no missing invariant conjunct, no scope drift.

The findings below are the accreted meta-prose the `review-mode.anti-bloat` classifier targets — not correctness defects, but degradations a precise reader must skip past.

## REVISE

### Issue 1: Essay content in a structural slot before D1
**ASN-0101, "What shifts: closing the gap"**: "That the operation actually closes the gap, rather than leaving it open with placeholders, is Nelson's explicit design choice. We extract it from the dense-sequence convention... There is nothing in the abstract specification of the V-stream to denote... The closure of the gap follows from the choice of representation, not from a separate gap-closing pass."

**Problem**: This paragraph is design-philosophy essay sitting between the operation spec and the formal claim D1. D1's argument is purely algebraic (TS1/TS2 on the shift-inverse) and does not consult the dense-sequence convention; the paragraph advances none of its reasoning. The recent commit already forward-referenced D0 for the `σ_d` form to tighten this section — the remaining philosophy paragraph is the residue.

**Required**: Cut to the one load-bearing sentence ("the post-state V-stream has no vacated-position denotation, so closure is intrinsic to the representation"), or fold it into the existing "No reconciliation across the gap" bullet.

### Issue 2: Hedge parentheticals in the worked examples
**ASN-0101, D9 content example**: "(...If V_2(d) = ∅ the consideration is vacuous; the projection result depends on neither possibility.)"
**ASN-0101, D10 discoverability check**: "witnessed by [1, 1, 1] ∈ project ∖ X (or equivalently [1, 1, 4] ∈ project ∖ X)."

**Problem**: Both are skippable. The first dismisses an unspecified case (`V_2(d)`) that the example never introduces; the second supplies a redundant second witness for an existential already discharged by the first. Neither advances the verification.

**Required**: Delete both parentheticals.

### Issue 3: Defensive meta-explanation in D8 Groups (ii)–(iii)
**ASN-0101, D8**: "A predicate over frame-fixed components — whether a per-state predicate ranging over a single state or a transition predicate comparing Σ and Σ' — propagates from Σ to Σ' unchanged; no member requires an individualized argument."

**Problem**: This sentence belabours the obvious (predicates over unchanged components are preserved) and the "no member requires an individualized argument" tail is an exhaustiveness-claim flourish. The two enumerated invariant lists that follow do serve rigor (standard #4) and should stay; only the surrounding meta-explanation is padding.

**Required**: Replace the quoted sentence with the bare principle ("D0's frame fixes `C`, `L`, `E`, `R`, `dom(M)` pointwise, so every Group (ii)/(iii) invariant predicating only over these is preserved") and keep the lists.

## OUT_OF_SCOPE

### Topic 1: Arrangement reconstruction / versioning
The Open Questions correctly defer pre-DELETE arrangement recovery, orphan-I-address rediscovery, and DELETE/INSERT round-trip reversibility to a downstream versioning mechanism. These are genuinely future ASNs, not gaps in D0–D11.

VERDICT: REVISE
