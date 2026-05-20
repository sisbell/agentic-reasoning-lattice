# Review of ASN-0047

## REVISE

### Issue 1: K.δ case-level `e ∉ E` is explicit for case (i), implicit for case (ii)
**ASN-0047, Elementary transitions, K.δ**: "`E' = E ∪ {e}` where `e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)`"; then case (i) has "Required: `ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E ∧ n₀ ≼ e`" while case (ii) lists only "Required uniformly: `parent(e) ∈ E`" plus per-sub-case operand-admissibility conjuncts.
**Problem**: Case (i) re-lists `e ∉ E` as an explicit per-case precondition; case (ii) silently relies on the "where" clause and lets each sub-case's freshness discharge mechanism (T10a GlobalUniqueness, FrontierEquivalence, NodeUniqueAllocation) carry the obligation without restatement. A reader scanning the per-case precondition lists sees a missing conjunct in case (ii) and must reconstruct that the "where" clause is meant to range over both cases.
**Required**: Either restate `e ∉ E` explicitly in case (ii) (and per sub-case, noting the discharge mechanism), or add a one-sentence preamble to case (ii) stating that the "where"-clause conjuncts apply uniformly and that `e ∉ E` is discharged per sub-case below.

### Issue 2: P7a discharge in the Class (b) prose elides one inferential step
**ASN-0047, Extended reachable-state invariants, Class (b) P7a paragraph**: "By S3★-aux, `subspace(v) ∈ {s_C, s_L}`, so `subspace(v) = s_C`. J1★ — which is range-based and triggers when an I-address is new to the content-subspace range of `M'(d)` — then supplies `(a, d) ∈ R'`."
**Problem**: The argument establishes `a ∈ ran(M'(d)|_{s_C})` (since `subspace(v) = s_C` and `M'(d)(v) = a`) but does not explicitly establish `a ∉ ran(M(d)|_{s_C})`, the *other* half of J1★'s range-new trigger. The missing one-line chain: `a ∈ dom(C') \ dom(C)` ⟹ `a ∉ dom(C)`; `ran(M(d)|_{s_C}) ⊆ dom(C)` by S3★'s content clause at Σ; therefore `a ∉ ran(M(d)|_{s_C})`. Without it, the trigger predicate is only half-discharged in the prose.
**Required**: Spell out the `a ∉ ran(M(d)|_{s_C})` step so J1★'s range-new trigger is justified end-to-end.

### Issue 3: K.δ k = 0 freshness discharge mixes axiomatic and derived T10a forms across the section without a consolidated handle
**ASN-0047, K.δ k=0 discharge paragraph and FrontierEquivalence lemma**: K.δ k = 0 cites "T10a chain-advancement uniqueness at `(t, 0)`" (derived from T10a.7 + P1 + precondition; FrontierEquivalence (i)), while K.δ k = 1 cites "T10a's per-`(t, k')` uniqueness" (the *direct* axiom for `k' ∈ {1, 2}`).
**Problem**: Both are labelled "T10a uniqueness" in the K.δ prose, but only k = 1 invokes the direct axiom — k = 0 uses the derived form. The Worked example (Step 1) further says "satisfied trivially as this is the first invocation," conflating the direct (k = 1) at-most-once with the derived (k = 0) at-most-once. A reader reconstructing the discharge has to recover the k vs k' distinction from FrontierEquivalence's body each time.
**Required**: Either consistently name the k = 0 form as "T10a chain-advancement uniqueness at `(t, 0)` (derived)" wherever it appears in K.δ k = 0 discharge prose, or add a one-line gloss at the K.δ definition pointing out which k uses the direct axiom and which uses FrontierEquivalence's derived form.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal mechanism
**Why out of scope**: D-CTG★ forces link-subspace contractions to be suffix-truncations under K.μ⁻, ruling out interior link withdrawal that preserves the V-positions of trailing links. A status-flag, tombstone marker, or retraction-link convention is needed to align with Nelson's tombstoning intent (LM 4/9) while preserving D-CTG★, but lies outside the presentational-removal contract this ASN defines. Already captured in Open Questions.

### Topic 2: External node-allocation registry protocol
**Why out of scope**: NodeUniqueAllocation and NodeRegistryBootstrap are taken as axioms — the protocol-layer specifics (issuing protocol, persistence model, concurrency discipline) of the external node-allocation registry belong to a separate registry-mechanism ASN. Whether the abstraction boundary is correct is itself an Open Question.

### Topic 3: Account-level depth-1 extension (K.δ with `k = 1` and `IsAccount(t)`)
**Why out of scope**: The K.δ k = 1 precondition restricts to `t ∈ E_doc`. Admitting `IsAccount(t)` would produce an account-shaped sibling; the structural form is well-typed but the role is not documented in Nelson or the implementation. Whether a future use case (account renaming, multi-account user identity) would require relaxing this is left to a future ASN. Acknowledged in Open Questions.

VERDICT: REVISE
