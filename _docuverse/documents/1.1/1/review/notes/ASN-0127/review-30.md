# Review of ASN-0127

I verified every derivation in this note step by step — the F-IMG family (including all four reorder witnesses, recomputed against the bijection equation), the F-UDIST/F-IMONO/F-VDIST algebra, the F-CIL/F-PRES/F-INERT/F-LAMBDA lane against ASN-0047's extended-state frames, the expanded E-CONS proof (anchor both directions, match well-definedness, both set-equality directions), D-CWP's bridge and biconditional, and the full worked illustration including the prefix-incomparability premise, every slot intersection, and the J0/J1★ composite-validity obligations. The mathematics is sound throughout; the anti-bloat scan also came back essentially clean — the prose is dense but proof-bearing, with no compounding deferral, consumer-enumeration, or relocated-finding patterns above threshold. One gap remains.

## REVISE

### Issue 1: D-CWP's biconditional is only ever instantiated on its failing side

**ASN-0127, D-CWP and Worked illustration**: "The contraction leaves the discovery set fixed iff `findlinks(Δ, Σ) ⊆ findlinks(I_R, Σ)`" — and, in the illustration, "D-CWP's `R = ∅` stability condition `findlinks_V(W, d, Σ) = ∅` fails — the discovery set is correctly *not* stable".

**Problem**: The wp is exercised concretely exactly twice, and both instances verify only the condition-false branch. The `R = ∅` boundary case fails (pre-state set `{L_1, L_2} ≠ ∅`), and the `n'_{s_C} = 1` contraction bullet instantiates the failing branch implicitly (`Δ = {a_2}`, `findlinks(Δ) = {L_2} ⊄ {L_1} = findlinks(I_R)`, matching the observed drop `{L_1, L_2} ↦ {L_1}`). No scenario shows the condition *holding* with `Δ ≠ ∅` — the case that distinguishes the wp from the cruder condition "no in-region I-address was dropped" and that demonstrates the satisfied branch is non-vacuously achievable. As written, a reader cannot tell from the note's own evidence whether stability under a genuine drop is ever realizable; a biconditional should be verified at both truth values, and the failing value is the only one exhibited.

**Required**: One contraction instance in the worked illustration where the stability condition holds with non-empty `Δ`. The note's existing material nearly supplies it: the K.α bullet's composite already arranges `v_4 ↦ a_4` with `a_4` fresh and (by the same sibling/`a_θ` incomparability arguments already established) reached by no stored link. From that four-position state, take `W' = {v_1, v_4}` and contract with `n'_{s_C} = 3`: then `I_R = {a_1}`, `Δ = {a_4}`, `findlinks({a_4}, Σ) = ∅ ⊆ {L_1} = findlinks({a_1}, Σ)`, and stability is confirmed by direct computation (`findlinks_V(W', d, ·) = {L_1}` at both states). Optionally add the re-witnessing shape (a link reaching both a dropped and a retained in-region address, e.g. `({a_1}, {a_2}, Θ)` in a state without `L_2`), which exhibits stability with `findlinks(Δ) ≠ ∅`.

## OUT_OF_SCOPE

### Topic 1: Multiplicity-aware query semantics
**Why out of scope**: The algebra is deliberately set-valued; how many V-positions witness each link's match (per-link witness counts, which a consumer weighting or rendering multiplicity would need, and which the "sole in-region witness" analysis in D-NONMONO gestures at) is a count-valued refinement with its own stability laws. New territory, not an error here.

### Topic 2: Q1–Q4 as marked
**Why out of scope**: Content-keyed queries through `Σ.C`, the slot-indexed conjunctive matching of Gregory's retrieval, the uniform stability wp across the whole K-vocabulary, and composition with ASN-0098's projection are all genuinely separate developments; the note correctly fences them as open questions rather than leaving silent gaps.

VERDICT: REVISE
