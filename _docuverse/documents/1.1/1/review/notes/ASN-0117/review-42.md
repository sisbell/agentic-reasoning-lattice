# Review of ASN-0117

## Verification performed

Before the verdict, the load-bearing claims were checked in detail:

**Arithmetic and foundation conformance.** The containment precondition `J + c ≤ N + 1` matches ASN-0082's contraction precondition `p₂ + w₂ − 1 ≤ N` exactly. The displacement chain was recomputed: `r = p ⊕ w = [1, J+c] = q_{J+c}` (TumblerAdd at action point 2), `σ(q_k) = vpos(1, [k] ⊖ [c]) = q_{k−c}`, with `k − c ≥ J ≥ 1` for every `k ≥ J + c`, so every shifted survivor is a well-formed positive ordinal — the OrdinalExceedsDisplacement appeal is correctly discharged by containment.

**Composite realisation.** Both cases were checked against ASN-0047's transition contracts. For `R ≠ ∅`: K.μ⁻'s strict-contraction obligation holds (`n'_{s_C} = J − 1 < N` since `J ≤ N` from `p ∈ V_S(d)`), and K.μ⁺'s strict-extension obligation holds (`N − c − (J − 1) ≥ 1` follows from `J + c ≤ N`). For `R = ∅`: `J + c = N + 1` gives `J − 1 = N − c`, the K.μ⁺ step would be an empty extension, and the ASN correctly routes to the lone K.μ⁻ rather than hand-waving the composite through. The net effect of the composite was reassembled by hand and equals D-L + D-SHIFT + D-DOM verbatim.

**Coupling discharge.** J0 and J1'★ are vacuous on empty antecedents (`dom(C')∖dom(C) = ∅`, `Σ'.R∖Σ.R = ∅`); J1★ was checked against its range-based trigger — every post-state content-subspace image of the operated `d` equals `M(d)(v)` for some pre-state content-subspace `v`, so the "range-new" conjunct is false everywhere, and DEL-FDOC closes all `d' ≠ d`. The `R = ∅` path correctly leans on J2.

**The wp derivation.** The set identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` was verified by direct set algebra: with `A_del^{excl} = A_del \ M(d)(L ∪ R)`, removal from `M(d)(L) ∪ M(d)(X) ∪ M(d)(R) ∪ ran(M(d)|_{s_L})` leaves exactly `M(d)(L ∪ R) ∪ ran(M(d)|_{s_L})`, with the SD/S3★ disjointness step needed (and supplied) to keep the `s_L` summand clear of `A_del`. Since the range only shrinks and the link store is fixed, `D(d, Σ') ⊆ D(d, Σ)` is unconditional and the stated per-link existential is genuinely the weakest condition for equality; the per-slot/per-link quantifier discussion is correct, not decorative.

**S8★ re-cut.** The fuse/split observation at the closed boundary is real (survivors `a_{J−1}`, `a_{J+c}` need not advance in lockstep), and the resolution — S8★ is per-state, with S8's five preconditions discharged conjunct by conjunct from the post-contraction package — is complete, including uniqueness via S8(c).

**Worked examples.** All five scenarios were recomputed: the primary delete (including the subtle point that label `q_3` stays but `q_4, q_5` vacate, matching DEL-REMOVE's count-and-label form), the multi-position shift (order preservation across `|R| = 3`), the leading-span delete (K.μ⁻ to empty, K.μ⁺ re-pinning S8-depth from scratch — the hardest sequencing case, worked explicitly), both `R = ∅` cases including `n'_{s_C} = 0`, the within-document-sharing case (`A_del^{excl} = ∅` computed correctly), and the cross-document transclusion case (including the correct observation that V-positions are shared vocabulary and scoping lives in the arrangement functions).

Boundary coverage is complete: first position, last position, entire document, empty suffix, sharing, transclusion. `c = 0` is excluded by `Pos(w)`; the empty document is excluded by `p ∈ V_S(d)`. No foundation notation is reinvented; every clause is read off ASN-0082/ASN-0047/ASN-0098 by citation with the label-collision between region `R`, provenance `Σ.R`, and retention `Ret` explicitly disarmed.

## REVISE

No issues. Every introduced claim is either a named citation of a foundation postcondition or carries an explicit derivation; the coupling obligations are discharged rather than asserted; the wp is non-trivial and exact; the examples verify the postconditions they cite. No anti-bloat patterns rose to a finding — the one terminology bridge (the consultation's "F0" mapped to DEL-FDOC) carries disambiguation content rather than defensive justification.

## OUT_OF_SCOPE

### Topic 1: DELETE at text-subspace depth m > 2
**Why out of scope**: The precondition pins `m = 2`, inherited from ASN-0082's contraction, which is stated only at depth 2. A document whose text subspace was re-pinned at `m ≥ 3` (permitted by S8a) has no DELETE under this ASN. Generalizing requires extending the foundation contraction to arbitrary depth first — new territory, not an error here.

### Topic 2: Caller-facing totalization over ill-formed spans
**Why out of scope**: The ASN correctly carries containment as a precondition and documents (via the implementation evidence) why the untotalized operation silently corrupts. Whether a caller-facing layer rejects or clips is a separate specification obligation, already recorded as an open question.

### Topic 3: Link-subspace contraction (un-arranging a link from a document)
**Why out of scope**: DELETE is text-subspace only (`S = s_C`). Removing a link's V-position from a document's `s_L` run is a distinct operation with its own CL-OWN/CL-UNIQ obligations, belonging to a future ASN.

VERDICT: CONVERGED
