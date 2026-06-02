# Review of ASN-0047

## REVISE

### Issue 1: J4 fork is characterized by range equality, which is strictly weaker than the "whole arrangement copy" it claims to formalize
**ASN-0047, J4 (Fork composite), step (ii)**: "K.μ⁺ populating M'(d_new) by a *complete* transclusion of `d_op`'s content subspace: `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})` — every content I-address of the source is inherited (range equality, not mere containment)" and "The equality ... is what 'copies the contents' demands ... the *whole* current arrangement, never a deliberate proper subset."

**Problem**: Range equality does not capture an arrangement copy. Two independent defects:
1. **Order is unconstrained.** D-SEQ★ forces `V_{s_C}(d_new) = {[s_C,1],…,[s_C,n]}`, but nothing links `M'(d_new)([s_C,k])` to `d_op`'s k-th position. A fork that places the source's content in reverse (e.g. `[1,1]↦a₂, [1,2]↦a₁`) satisfies `ran(M'(d_new)) = {a₁,a₂} = ran(M(d_op)|_{s_C})` yet is not a faithful version of the source. A new version must start identical to its source, including order.
2. **Multiplicity is lost.** Under S5 (UnrestrictedSharing, ASN-0036) one I-address may sit at multiple V-positions of `d_op` (e.g. `M(d_op) = {[1,1]↦a, [1,2]↦a}`, `ran = {a}`). Range equality permits `M'(d_new) = {[1,1]↦a}` (`n=1`), collapsing the duplicate and changing the document's content/length. Nelson's CREATENEWVERSION copies the full POOM width, duplicates included.

The worked examples happen to exhibit position-preserving forks, so they are faithful instances of an under-constrained spec — they do not establish that the spec rules out the unfaithful forks above.

**Required**: Characterize the fork by a position- and multiplicity-preserving copy of `d_op`'s content-subspace arrangement (e.g. a depth-rebasing bijection `φ: V_{s_C}(d_op) → V_{s_C}(d_new)` with `M'(d_new)(φ(v)) = M(d_op)(v)` for every `v`), not by range equality. Range equality should at most be a derived consequence.

### Issue 2: Temporal decomposition table omits K.δ as a transition that modifies M
**ASN-0047, Temporal decomposition table**: the M row reads "Presentational | M | Fully mutable | K.μ⁺, K.μ⁺_L, K.μ⁻ (elementary); K.μ~".

**Problem**: K.δ's own Document-case frame/effect explicitly grows the arrangement family: "Document(e): `dom(M') = dom(M) ∪ {e}` with `M'(e) = ∅`". Since `dom(M) = E_doc` (Bridging lemma), every document-creating K.δ modifies M's domain. The J4 discharge even insists this is "the *explicit* effect M'(d_new)=∅ ... not a totality-convention default." The table contradicts both K.δ's frame and the J4 discharge by attributing M-modification only to the K.μ* transitions.

**Required**: Either add K.δ to the M row's transition list (as a domain-growing, non-destructive modifier), or reconcile by committing to the convention reading uniformly (drop the "explicit effect" language in K.δ/J4 and state once that K.δ grows only E_doc, with `M(e)=∅` arising from the default-value convention). The two readings cannot both stand.

### Issue 3: Forward-reference deferral and meta-prose around classification (anti-bloat)
**ASN-0047, multiple sites**: Several paragraphs defer reasoning downstream rather than advancing it at point of use:
- "the precise firing condition is J1★ (Scoped coupling constraints, below)" (Coupling and isolation preamble);
- "Validity of a composite transition `Σ →* Σ'` is governed by **ValidComposite★**, defined in *Scoped coupling constraints*" (Permanence-adjacent);
- "the per-subspace strengthening to D-CTG★/D-MIN★ is adopted at the K.μ⁺ amendment — see *Amendments to existing transitions*" (K.μ⁺ precondition).

**Problem**: These are the "multiple paragraphs in different sections defer to the same downstream location" pattern the anti-bloat classifier flags. A reader following the K.μ⁺ precondition or the coupling preamble must jump forward to obtain the actual constraint; the deferral text occupies a slot where the constraint itself (or a one-line statement of it) belongs. The P4a treatment compounds this — it is classified as a trace property in its definition box, re-classified in the ExtendedReachableStateInvariants preamble, and re-described in the composite-boundary matrix, three restatements of the same temporal-scope point.

**Required**: State the operative constraint inline where the precondition/preamble first needs it (a single clause naming J1★'s trigger, or ValidComposite★'s two-clause shape), reserving the cross-reference for the full derivation. Collapse the P4a temporal-scope explanation to a single authoritative location.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior arrangement contraction
The ASN's K.μ⁻ is suffix-only and explicitly does not model the implementation's compact-and-renumber interior `DELETEVSPAN`. This is correctly identified as an open question rather than a defect — interior-deletion-with-renumbering is operation-level (DELETE) territory, out of scope for the elementary transition model.

### Topic 2: One-sided / type-only link admissibility
Whether K.λ should require `e₁ ∪ e₂ ≠ ∅` is raised as an open question. The semantics of one-sided links belong to a future ASN on link operations (MAKELINK), not to this transition model.

VERDICT: REVISE
