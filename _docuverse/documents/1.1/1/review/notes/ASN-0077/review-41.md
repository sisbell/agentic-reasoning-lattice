# Review of ASN-0077

I read this as a self-contained specification of a read-only query operation. The bulk of the work is establishing derived properties of `origin` and its two span lifts, plus the preservation/non-preservation boundary across arrangement transitions. I checked the load-bearing proofs in detail.

## Verification performed

**O0 (origin extended to dom(L)).** The semantic-correspondence half (b) composes L1c with the Allocator-hierarchy definition and SubAllocatorAxiom(e) without any K.λ-event closure — the routing through `A_L(origin(ℓ))` is justified by `subspace_I(ℓ) = s_L` (L0) plus disjointness (e). Totality (c) is discharged per-case by P6/P1. Sound.

**Singleton I-span edge case.** The three-way length split (`#b < #a` excluded by T1 case-(i)/(ii) analysis; `#b = #a` by T3; `#b > #a` by zero-count balance + T4b parse coincidence) is fully worked. The prefix-agreement minimal-index argument, the lower/upper bounds on position `#a`, and the NAT-discrete squeeze all check out. I confirm the deliberate decision *not* to push to a strict-singleton intersection (which would require an unwarranted `#E = 2` closure assumption) is correctly flagged.

**O11 / O11' (preservation under K.μ⁺ / K.μ⁺_L).** The (⊇) Case (ii) impossibility arguments are correct: sub-case (a)'s cross-state depth identification via S8-depth (pre-state positions force `m' = m`) and sub-case (b)'s subspace/depth contradictions against precondition (vi) are valid. Freshness of `v_ℓ` from K.μ⁺_L's strict-containment effect is correctly derived rather than assumed.

**O11★ / O11★★ exhaustiveness.** The binary modifies-`M(d)` / leaves-`M(d)`-fixed partition is genuinely robust to vocabulary extension and does not rely on enumerating ASN-0047's transition set. Non-`M(d)`-modifying steps correctly route to O7.

**O13 / O14 (negative claims).** Both witnesses are concrete and admissibility is verified (O14 discharges S8a, S8-depth, D-CTG★, D-MIN★, S3★, S3★-aux for the K.μ~ post-state explicitly). The distinction between O13's *admissibility loss* and O14's *incomparable sets* is correctly drawn, and the asymmetry with LP10/LP11 is correctly attributed to total/partial conventions rather than to differing facts.

**O10 idempotence, F1≡F2≡F3 equivalence, wp characterisations.** The single-origin wp is genuinely non-trivial (the pair-equality conjunct), and the worked example exercises both satisfying and falsifying configurations — including the `d_q = d₂` falsification that operationally confirms O4.

No cross-ASN references outside the foundation set appear in the body. No bare-checkmark proofs, no "by similarly" where cases materially differ (O11'★'s "parallel" reduction is acceptable because the induction is structurally identical and the genuinely-different single-step lemmas O11/O11' are each proved in full).

## OUT_OF_SCOPE

These are correctly deferred to the ASN's own Open Questions, not defects here:

### Topic 1: Link-origin reporting from an I-span
The I-span lift restricts to `dom(C)` by definitional choice; reporting link origins from an I-span range is new territory.

### Topic 2: Historical containment via Σ.R
Distinguishing current-arrangement origins from documents that *have ever* contained content is a separate operation coupling `origins_V` to the provenance relation.

### Topic 3: Surfacing the transclusion chain
SHOWORIGIN gives the direct answer (`d₁`); an operation exposing intermediate documents `d₂…dₙ₋₁` belongs elsewhere.

VERDICT: CONVERGED
