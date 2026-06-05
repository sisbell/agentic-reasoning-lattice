# Review of ASN-0107

## REVISE

### Issue 1: D2's reordering claim is false — reordering changes the image of a fixed query region

**ASN-0107, "Two Anchorings" (D2)**: "reordering d_q preserves the image as a set (LP11 gives `ran(Σ'.M(d_q)) = ran(Σ.M(d_q))`) and hence preserves the count."

**Problem**: `Qᵢ(Σ)` is the *forward image of a fixed V-region* `Wᵢ`, not the total range. LP11 preserves only the whole range `ran(M(d_q))`. Under K.μ~ the bijection π moves content among positions (`M'(d_q)(v) = M(d_q)(π⁻¹(v))`), so `Qᵢ(Σ') = {M(d_q)(u) : u ∈ π⁻¹(Wᵢ)}`, which differs from `Qᵢ(Σ) = {M(d_q)(u) : u ∈ Wᵢ}` whenever `π⁻¹(Wᵢ) ≠ Wᵢ`. Concrete counterexample: `d_q` maps `v1↦a1, v2↦a2`; query `W₁={v1}`, so `Q₁={a1}`; a link `a` whose from-coverage is `{a1}` matches. Swap `v1,v2` by K.μ~: now `Q₁={a2}`, the link no longer matches, `num_disc` drops 1→0 with no link created or retracted. So reordering can change the discovery count.

Relatedly, the extension/contraction citations are category-mismatched: LP9/LP10 govern `project(e,d,Σ)` (the *preimage* of an endset's coverage), not the forward image `Qᵢ(Σ)` of a query V-region. The directionality of extension/contraction happens to survive on independent grounds (domain growth + prior-domain agreement), but the cited lemmas do not establish it.

**Required**: State the correct reordering behaviour (the discovery count is *not* in general preserved under K.μ~ of `d_q` for a positionally-anchored query; preservation holds only when `π` fixes `Wᵢ` setwise, e.g. `Wᵢ` is an entire subspace), and derive the extension/contraction monotonicity of `Qᵢ` directly rather than via LP9/LP10.

### Issue 2: Retraction laws R1/R5 contradict the definition of `num` and contradict E2–E4

**ASN-0107, "How the Count Changes: Links Retracted" (R-section intro, R1, R5)**: "by an explicit nullification that excludes it from the active population"; R1: "Withdrawing a single link `a` removes exactly the element `a` from the counted set. The count decreases by one if `a` was counted"; R5: "`num(Q, Σ₂) − num(Q, Σ₁) = (matching links created) − (matching links retracted)` ... where 'retracted' denotes nullification."

**Problem**: `num(Q, Σ) = |{a ∈ dom(Σ.L) : sat(a,Q,Σ)}|` ranges over *all* resident links and never consults a nullified/active-subset notion (ASN-0086's `nullified`/`A_K` are nowhere in the definition). Nullification adds a retraction tuple to `dom(Σ.L)` but removes nothing, so it cannot decrement either the existence count or the discovery count as defined. Consequently R5's existence-count identity (with a nonzero "retracted" term) directly contradicts E2 (`num` monotone non-decreasing), E3 (contraction leaves the existence count unchanged), and E4 (existence-count change equals matching creations, with "no term subtracts"). R1's "withdraw exactly one link, Δnum ∈ {−1,0}" likewise has no count-visible mechanism: nullification is invisible to `num`, and arrangement-severing of a shared endpoint affects every link covering that endpoint (R2's own regime), not "exactly the element `a`."

**Required**: Resolve the definitional gap. Either define `num` over the active/discoverable subset (incorporating `nullified(Σ)`) so that R1/R5 hold, or restrict the retraction laws to arrangement-based withdrawal, explicitly state that `num` is blind to nullification, and drop the "− retracted" term from R5's existence identity (leaving it equal to E4).

### Issue 3: No concrete worked example

**ASN-0107, whole document**: the ASN states P0–W2 abstractly but never verifies them against a single concrete scenario.

**Problem**: Depth standards require at least one specific instance — e.g., a small `Σ.L` with named tumbler addresses and a specific triple `Q`, computing `num`, then checking P1 (multi-span link counted once), P2 (two equal-valued links counted twice), and E2/E4 across a K.λ step. Without it, the set-vs-multiset distinction (P1) and the conservation behaviour (E4) are asserted but not exercised.

**Required**: Add a worked instance computing `num` and checking the load-bearing postconditions (at minimum P1, P2, E4, and one discovery-count change under K.μ⁺/K.μ⁻).

### Issue 4: "At least one constrained part" is stipulated but never formalized

**ASN-0107, "State and the Counting Request"**: "We require at least one constrained part, so that the request denotes a genuine query rather than the entire store."

**Problem**: This precondition appears in prose only; it is not part of the request type, `sat`, or `num`, and `num` is claimed total over "every request." If a fully-unconstrained `Q = (T,T,T)` is admitted, `num` counts every link with three non-empty endsets — a defined value, but one the prose excludes. The status (precondition vs. always-defined) is ambiguous.

**Required**: Either fold the constraint into the request well-formedness conditions explicitly, or drop it and acknowledge `Q=(T,T,T)` as a legitimate (if broad) query with defined `num`.

## OUT_OF_SCOPE

### Topic 1: Independent per-slot anchoring across separately-evolving documents
**Why out of scope**: The first open question (request parts anchored to different documents' arrangements) is genuinely new territory — the present ASN fixes a single resolving document `d_q` — and belongs in a follow-on ASN, not this revision.

### Topic 2: Relationship between `num` and the cardinality the retrieval operation would return
**Why out of scope**: This couples ASN-0107 to FINDLINKS/ASN-0099 (explicitly out of scope per the scope section); the count-vs-retrieval staleness guarantee is correctly deferred.

VERDICT: REVISE
