# Review of ASN-0103

## REVISE

### Issue 1: The non-invocation of GlobalUniqueness/B8/T9/T10 is argued at three separate sites
**ASN-0103, Effect One (Freshness), CND.monotone (Claims table), Invariants Maintained (address permanence)**: Effect One says "we do not need GlobalUniqueness ... Nor do we route through partition independence (T10) ... We deliberately do *not* route this through B8"; CND.monotone repeats "T9 does not apply across allocators", "GlobalUniqueness not used", "B8's same-namespace branch is deliberately not invoked"; the invariants section repeats again "We do not invoke GlobalUniqueness, whose T10a-conformance premise this state model leaves undischarged, nor B8's same-namespace branch."
**Problem**: The same four non-invocations, each with the same rationale (undischarged T10a-conformance / single-authority premise / cross-allocator scope), are restated in three sections. This is defensive justification a precise reader must skip past; the argument is carried once by the positive citations (S0 for same-chain, B7 for cross-namespace).
**Required**: State the proof route positively once (S0 + B7), with the non-invocation caveat at a single site if at all. Remove the repetitions in CND.monotone and the invariants section.

### Issue 2: The ω-deferral / E↔B-coupling essay is restated across five slots
**ASN-0103, Ownership and Immediate Referability; CND.pre; CND.own; CND.inv; Open Question 6**: The "Ownership" section devotes a full paragraph to why `ω_{Σ'}(d) = ω_Σ(A)` is not derivable, enumerating "(i) a registry component ... (ii) a coupling invariant ... e.g. `{e ∈ E : ...} = Σ.B ∩ S(A, 2)`", naming O17b/O18, and deferring to "an ASN whose state carries the registry." CND.own restates the entire deferral; CND.pre restates the O5 deferral; CND.inv restates it again; Open Question 6 asks for the same coupling.
**Problem**: Multiple paragraphs in different sections defer to the same downstream location and explain *why* the registry-carrying claim is not made rather than advancing this ASN's content. The Open Question already captures the forward obligation; the prose duplication is accretion.
**Required**: Make the ω/O5 deferral once (the Open Question is the right home), and reduce the claims-table and section prose to a one-line "ownership is structural (`pfx(π) ≼ d`); effective-owner deferred — see Open Questions."

### Issue 3: A version-dominance paragraph imagines a case the dominance scope already excludes, then declares it moot
**ASN-0103, Effect One (subsequent case, off-chain)**: "Such a `v` is a document — or a version thereof — allocated under a *proper sub-account* `A' = [A, x, …]` ... The concrete shape is `d' = inc(A', 2) = [A', 0, 1]` ... (Whether such a `v` is even allocable in `E` is moot for correctness — divergence at `#A+1` settles distinctness regardless of realizability.)"
**Problem**: CND.monotone's dominance scope explicitly excludes off-chain (`v_{#A+1} ≠ 0`) entities; distinctness for them is already settled in one line by divergence at `#A+1`. The paragraph constructs an `A'`-sub-account scenario, derives its shape, and then admits the whole construction is "moot for correctness." This is reviser drift — elaborating a case the claim does not need.
**Required**: Collapse the off-chain case to the one-line divergence argument (`d_{#A+1}=0 < v_{#A+1}` ⟹ `d < v` ⟹ distinct). Delete the proper-sub-account construction and the "moot" parenthetical.

### Issue 4: The first-case version-dominance argument forward-references the subsequent case for the same proof it then repeats in full
**ASN-0103, Effect One (CND.monotone, first case vs. subsequent case)**: First case: "consider the *first* `k=1` fork in its ancestry chain ... so (by the length argument detailed in the subsequent case below) `t` has no version among its predecessors ... forcing `#t = #A+2 ∧ parent(t) = A ∧ Document(t)`." Subsequent case then re-derives exactly this — the first-fork operand `t`, `A ≼ t`, single `k=2` descent off `A`, `t = [A,0,i] ∈ D_A` — at full length.
**Problem**: Two paragraphs run the same first-fork length argument; the first defers to the second ("detailed in the subsequent case below") rather than sharing it. This is a same-document deferral to a downstream location for an argument the document already contains.
**Required**: Factor the first-fork operand argument ("the first `k=1` fork's operand is a root document `[A,0,i] ∈ D_A`") into a single named sub-lemma and cite it from both cases, or merge the two cases.

### Issue 5: Use-site inventories in the `D_A` and Effect One development
**ASN-0103, Effect One**: "Three consequences, each used below, now follow: when `D_A ≠ ∅` ..."; "it is the *reverse* direction ... that the load-bearing facts below actually consume"; "We claim only what the load-bearing facts below require."
**Problem**: These forward-pointing inventories announce that later steps will consume the facts without advancing the derivation. They are noise around an otherwise correct development.
**Required**: State the consequences where they are used, or state them plainly without the "each used below" / "load-bearing facts below" framing.

### Issue 6: B7 invoked for the version chains without discharging its B6 precondition
**ASN-0103, Effect One (Freshness)**: "each `A_v(d_i) = S(d_i, 1)` is a *distinct namespace* ... so `S(A, 2) ∩ S(d_i, 1) = ∅` by namespace disjointness (B7, ASN-0040)."
**Problem**: B7 (ASN-0040) requires *both* `(p,d)` and `(p',d')` to satisfy B6. The cross-account case immediately below correctly discharges B6 for `(A',2)`, but the version case never states B6`(d_i, 1)`. The premise holds (`d_i` is T4-valid, `zeros(d_i)=2`, depth 1 gives `2 ≤ 3`), but it is asserted without the check the parallel case supplies.
**Required**: Add the one-line B6`(d_i, 1)` discharge (T4-valid document, `zeros(d_i)+(1-1)=2 ≤ 3`) before applying B7, matching the cross-account treatment.

### Issue 7: CND.A-act prose explains why the assumption is needed rather than stating it
**ASN-0103, The Operation's Input (CND.A-act)**: "Nelson's design intent makes the assumption structural rather than incidental: owning an account *is* holding the authority ... 'Once assigned a User account, the user will have full control over its subdivision forevermore' (4/29). There is no enabling step between 'account exists' and 'documents can be forked under it' ..."
**Problem**: The axiom content is the one-line `A ∈ E ∧ Account(A) ⟹ Activated(A_doc(A))`. The surrounding paragraph is "why the assumption is needed" rationale (a labeled-rationale anti-pattern), restating the account-tier analogue point already made by the SubAllocatorBundle reference.
**Required**: State CND.A-act and its single SubAllocatorBundle-analogue citation; cut the design-intent justification to at most one clause.

## OUT_OF_SCOPE

### Topic 1: Effective-owner conclusion `ω_{Σ'}(d) = ω_Σ(A)` and the E↔B coupling invariant
**Why out of scope**: Correctly deferred — `ω` and the registry `B` are not components of ASN-0047's state `(C,L,E,M,R)`. The forward obligation is properly logged as an Open Question; it belongs to a registry-carrying ASN, not here.

### Topic 2: O5 grounding of subdivision authority
**Why out of scope**: O5 quantifies over `B` and `Π_Σ`, absent from this state model. Taking the caller's allocation authority as a stated assumption is the right boundary; grounding it is future work.

VERDICT: REVISE
