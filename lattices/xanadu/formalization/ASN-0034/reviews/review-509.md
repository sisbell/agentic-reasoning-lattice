# Regional Review — ASN-0034/TA5-SigValid (cycle 1)

*2026-04-24 08:50*

Reading as a system to find new issues distinct from previous findings.

### Defensive meta-prose in TA5-SIG opening
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: TA5-SIG, second paragraph: "The maximum of a bounded nonempty ℕ-subset is not delivered directly by NAT-wellorder, which states only the *least-element* principle; ℕ has no greatest element, so the principle does not dualize unconditionally, and greatest elements are guaranteed only on subsets bounded above. We derive `max(S)` from the least-element principle with `#t` as the explicit boundedness witness."
**Issue**: The first sentence is a defensive justification — explaining why the `max(S)` construction is needed rather than advancing the proof. A precise reader must skip past it to reach the actual construction ("Form the upper-bound set `U`..."). The derivation stands on its own without the dualization commentary. This is the reviser-drift pattern where new prose around an axiom explains why the axiom is insufficient rather than what the proof does.

### T4b cites NAT-discrete for positivity into `ℕ⁺` that NAT-zero alone supplies
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: T4b prose: "a nonempty finite sequence over `ℕ` (by T0) with every component strictly positive by NAT-zero and NAT-discrete at `m = 0`." And Depends bullet: "NAT-discrete — at `m = 0`, promotes non-zero components to strictly positive, placing the image of each projection in the all-`ℕ⁺`-component subset of `T`."
**Issue**: T4 defines `ℕ⁺ = {n ∈ ℕ : 0 < n}`. From `tᵢ ≠ 0`, NAT-zero's disjunction `0 < n ∨ 0 = n` alone (equality branch excluded by `tᵢ ≠ 0`) gives `0 < tᵢ`, i.e., `tᵢ ∈ ℕ⁺`. NAT-discrete's `0 < n ⟹ 1 ≤ n` would land in `{n : n ≥ 1}`, a presentation not used elsewhere in the ASN. The citation and the Depends bullet are either spurious or are silently invoking an `ℕ⁺`-via-`≥ 1` reading that diverges from T4's definition. T4b also inherits `0 < Nᵢ, 0 < Uⱼ, …` directly from T4's Axiom; the re-derivation is in any case redundant.

### NAT-sub strict-monotonicity/strict-positivity rationale is design commentary inside the claim body
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: NAT-sub, e.g., "Strict monotonicity … is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from the right-inverse … Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form … from being separately exported"; and the parallel passage for strict positivity.
**Issue**: Both Consequence sections open with a paragraph of editorial rationale explaining why a clause is a Consequence rather than an Axiom, and cross-referencing NAT-order's design choice. A precise reader has to skip past it to reach the derivation. The rationale is about specification-style choices, not about what the Consequence says or why it holds. It belongs in design notes, not the claim body. Flag the placement, not the existence of the discussion.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 732s*
