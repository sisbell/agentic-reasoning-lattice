# Review of ASN-0116

## REVISE

### Issue 1: Insertion depth `m` is undefined when the target subspace is empty
**ASN-0116, "What shifts" / INSERT precondition**: "`p` is S8a-well-formed of the common depth `m` of `V_S(d)`; `p` is a valid insertion position (`p = q_1` if `V_S(d) = ∅`, else `p = q_J` …)"
**Problem**: When `V_S(d) = ∅` there is no "common depth `m` of `V_S(d)`" — S8-depth fixes a depth only for a non-empty subspace. Yet the notation `q_k = [S,1,…,1,k]` of depth `m`, the precondition, and the entire Effect block (I-NEW, I-DOM) all reference `m` and purport to cover the empty case. The depth is in fact pinned by the supplied position itself (`m = #p`), not by `V_S(d)`; foundation ValidFirstInsertionPosition takes an explicit `m ≥ 2` precisely because the first insertion *fixes* the depth. Open Question #4 admits this is unresolved, which directly contradicts the operation claiming to handle `V_S(d) = ∅`.
**Required**: State `m := #p`, require `#p ≥ 2`, and require `#p` to match the existing common depth when `V_S(d) ≠ ∅`. Make the empty-subspace case (first insertion fixes the depth) explicit rather than deferring it to an Open Question while simultaneously asserting an Effect for it.

### Issue 2: P4 (LinkSurvival) rests on a false premise and omits resurrection
**ASN-0116, P4 derivation**: "INSERT alters no existing I-address and the new addresses `A_new` are fresh, hence absent from any endset created before this operation."
**Problem**: Freshness against `dom(C)` does *not* imply absence from prior endsets. Foundation L4 (EndsetGenerality) and L9 (TypeGhostPermission) permit an endset to reference *any* tumbler, including ghost addresses not yet in `dom(C)`. A pre-existing endset may therefore reference an address that INSERT now allocates as part of `A_new`. Two consequences: (a) the cited premise is simply wrong (coverage-invariance actually follows from endset immutability alone, not from freshness); (b) such a link gains *new* resolved V-positions at the inserted block `{q_J, …, q_{J+n-1}}` — a resurrection (cf. foundation ASN-0098 LP18) — yet P4 asserts the only changed witnesses are `shift(v, n)` and concludes "only its resolved V-positions reflect the post-insert arrangement." This completeness claim is false. Note the asymmetry: the analogous "fresh ⇒ not in `M(d')`" step in P5 *is* valid, because arrangements obey referential integrity (`ran(M(d')) ⊆ dom(C)`), but endsets do not.
**Required**: Derive coverage-invariance from endset immutability (not freshness), and extend P4 to account for prior endsets whose coverage meets `A_new` — the inserted block then carries newly-discoverable witnesses, which the current statement excludes.

### Issue 3: Arrangement-layer effects and allocation reinvent foundation claims
**ASN-0116, Effect (I-SHIFT, I-LEFT, F-SUB, F-DOC) and "What is allocated"**: I-SHIFT is verbatim foundation ASN-0082 I3 (PostInsertionShift); I-LEFT is I3-L; F-SUB is I3-X; F-DOC is I3-D; the well-formedness re-derivation ("D-SEQ, D-MIN, D-CTG … preserved with `N' = N + n`") duplicates ASN-0082's I3-VD/I3-VP/D-SEQ-post family. P0/P2/P3 freshness and the contiguous run `A_new = {shift(a,k)}` restate foundation ASN-0093 K.α (ContentAllocation) with FirstEmissionFreshness/SubsequentEmissionFreshness; the valid-insertion-position precondition restates ASN-0036 ValidInsertionPosition / ValidFirstInsertionPosition.
**Problem**: Standard 7 — an ASN must use foundation definitions, not reinvent them under new labels. INSERT is a composite of K.α (n times) + K.μ⁺ (the I3 shift); the ASN reproves both layers from scratch instead of composing the cited foundation results. The `findpreviousisagr`/`granf2.c` description is acceptable as evidence, but the abstract guarantees it supports already exist in K.α.
**Required**: Express INSERT as a composition of the foundation transitions (K.α for allocation/freshness, the I3 family for the shift, ValidInsertionPosition for the precondition) and cite them, rather than introducing I-SHIFT/I-LEFT/F-SUB/F-DOC/P0 as fresh claims.

### Issue 4: No concrete worked example
**ASN-0116, throughout**: The ASN states P0, P1, I-DOM, I-SHIFT etc. but never verifies them against a specific scenario.
**Problem**: Standard 6 requires a concrete example checking key postconditions against one definite case. There is none here — e.g., "INSERT 'XY' (n = 2) at `p = q_3` into a text subspace with `N = 5`": show `A_new = {shift(a,0), shift(a,1)}`, the suffix `q_3,q_4,q_5 → q_5,q_6,q_7`, the new block at `q_3,q_4`, and the resulting dense run `{q_1,…,q_7}`, checking I-DOM, I-NEW, P1.
**Required**: Add a worked numeric example verifying the load-bearing postconditions (P0/P1/I-DOM) against a specific document state, including at least one boundary (append `J = N+1` and/or empty `V_S(d) = ∅`).

### Issue 5: No weakest-precondition / derived-consequence analysis
**ASN-0116, P4/P5**: The interesting guarantees (link discoverability survival, document isolation) are asserted but never analyzed via weakest precondition, and no non-trivial derived consequence is computed.
**Problem**: Standard 6 ("Missing depth") — wp analysis is absent, and the most informative case is exactly the one missed in Issue 2: the wp for "link discoverability from `d` is preserved (no spurious resurrection)" is *not* trivially true; it requires `coverage(e) ∩ A_new = ∅` for every prior endset. Computing it would have surfaced the resurrection gap.
**Required**: Compute at least one non-trivial wp (e.g., wp of INSERT against "the set of links discoverable from `d` is unchanged," or against P5 isolation), and derive its consequence explicitly.

## OUT_OF_SCOPE

### Topic 1: Provenance recording atomic with allocation (Open Question #3)
**Why out of scope**: The relation between fresh I-addresses and recorded provenance is ASN-0047 (K.ρ / J1★) territory; it is correctly left as an Open Question here, not an error in this ASN.

### Topic 2: Concurrent insertions without a serializing authority (Open Question #2)
**Why out of scope**: Concurrency/serialization is a separate concern (cf. foundation B-Seq single-authority assumptions); appropriately deferred.

### Topic 3: Post-insertion fragmentation of the inserted run (Open Question #5)
**Why out of scope**: Behavior under later DELETE/REARRANGE belongs to those operations' ASNs (reframed ASN-0117/0119), which are out of scope per the scope list.

VERDICT: REVISE
