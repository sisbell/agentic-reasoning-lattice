# Review of ASN-0118

I checked every claim against the foundations it cites: the relaxation of ASN-0058's condition (iii) and whether the inherited machinery (C1a, C1b, B3 lockstep) still applies under it; the composite decomposition in both the append/empty and displacing cases against ASN-0047's elementary K.μ⁻/K.μ⁺/K.ρ contracts; the coupling discharges J0, J1★, J1'★ over the full post-state quantifier; the range equations in both the J1★ section and the wp section; the ordinal arithmetic of the tiling derivation; CP4's exactness; CP8's three-branch membership analysis; and the worked example's tumbler arithmetic. I found no error.

Specific verifications worth recording:

- **The condition-(iii) drop is sound.** C1a's claim statement is explicitly general — it holds for *any* restriction whose induced domain lies in a single subspace — and the content-residence precondition supplies exactly that hypothesis, replacing C0a's role (which would not survive the relaxation, since a relaxed span's denotation need not be prefix-confined). The per-position grounding of `expand` (run interiors included) correctly routes through B3 consistency on the restriction rather than through any property of the span's shape.
- **The displacing-case decomposition is faithful.** The retained prefix `{[s_C,1,…,1,k] : 1 ≤ k ≤ j}` matches K.μ⁻'s canonical per-subspace retention form; the full link-subspace retention is admissible because the text subspace supplies the required strict contraction (including the `j = 0` boundary, where the intermediate D-MIN★ is correctly noted vacuous); step (ii)'s added positions are disjoint from the retained domain, so K.μ⁺'s strict-extension frame holds; and CP3c's production correctly accounts for vacated tumblers re-entering as placement or shifted positions under single new bindings — the union ranges `[min,p) ∪ [p,p+W) ∪ [p+W,max+W]` are consecutive and disjoint by TS1/TS3/TS4, with the abutment arithmetic `min+(j+W) = p+W` checked.
- **The coupling discharge is now complete over the full quantifier.** Other documents are handled by the arrangement frames (J1★ vacuous off `d`, J1'★ vacuous because only K.ρ at `d` touches `R`); at `d`, the range equation's `⊆` direction is genuinely derived from CP3c plus CP6's closure, reducing J1★ to membership per placed address; and the three branches (range-new unrecorded → K.ρ, range-new recorded → P2, not range-new → P4★ + P2) are exhaustive, with P4★'s availability correctly licensed by the composite-boundary standing precondition. The K.ρ inventory is determinate, and J1'★'s constraint on `R' ∖ R` matches it exactly.
- **Boundary cases are covered**: empty destination (D-MIN/D-SEQ established rather than preserved), append (`j = N`), insertion at minimum (`j = 0`), `W ≥ 1` exclusion of the degenerate resolution, partial binding, duplicate addresses in the resolved sequence (CP4's occurrence-count arithmetic, CP8's set semantics), self-transclusion (CP9), and re-COPY of previously deleted content (the range-new-yet-recorded branch).
- **Depth requirements are met**: a non-trivial wp (link discoverability, with state-dependent guard conjuncts correctly placed inside `enabled`), a worked two-source example whose arithmetic I verified (resolution runs, shift of `[1,2]` to `[1,5]`, origin multiset `⦃d_A, d_A, d_B⦄`, provenance classification via S4), and derived consequences (closure inventory, source-side connectedness, the REPLICATE contrast at three distinct seams).

I also read the ASN under the anti-bloat lens. The defense of the condition-(iii) drop carries Nelson exegesis, but it is doing verification work — a reviewer must be shown that nothing downstream consumes the dropped condition, and the two mini-examples demonstrate the relaxation has bite. The three REPLICATE contrasts each derive a distinct consequence (identity collapse, link loss, multiset collapse) rather than repeating one. No paragraph defends document ordering, enumerates consumers in place of meaning, or relitigates an excluded case. Cross-ASN references are confined to foundation ASNs.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Undiscoverability after subsequent contraction of transcluded positions
**Why out of scope**: The ASN proves discoverability is *established* by COPY; what later K.μ⁻ steps must guarantee about its loss is a property of contraction sequences, not of this operation. The ASN's Open Questions already fence it.

### Topic 2: Transclusion into the link subspace and mixed-depth assembly
**Why out of scope**: Both are new territory — a different placement target (K.μ⁺_L semantics) and a spec-set regime the content-residence precondition deliberately excludes. Correctly deferred in the Open Questions rather than half-specified here.

VERDICT: CONVERGED
