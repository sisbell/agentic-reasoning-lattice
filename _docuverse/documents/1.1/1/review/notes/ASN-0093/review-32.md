# Review of ASN-0093

The state/operation/invariant structure is sound, the simultaneous induction is well-founded (every inductive-step appeal is to a pre-state IH fact, no circularity), and the worked example computes correctly. The residual issues are accumulated meta-prose around the forward references and the chain-citation scaffolding — consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Explanatory paragraph contrasting the two first-emit chain lengths

**ASN-0093, L1c chain exhibition (after the first-emit case)**: "Note that the C1c first-emit chain has *two* inc steps (`d → b_C(d) → a`) while the L1c first-emit chain has *three* (`d → b_C(d) → b_L(d) → ℓ`) — they are not parallel chains differing only in a single-step substitution. The link chain must traverse the additional `inc(b_C(d), 0) = b_L(d)` step because the link subspace anchor sits one sibling-component beyond the content subspace anchor."

**Problem**: Pure explanatory essay. The two chain exhibitions sit directly above; their step counts are self-evident by inspection. The paragraph advances no claim — it narrates a difference the reader already has in front of them.

**Required**: Delete.

### Issue 2: Chain-indexed disciplines' "no per-transition discharge" stated four times via a pointer chain

**ASN-0093, Simultaneous-induction framing**: "Their once-and-for-all status as ASN-0040 citations requiring no per-transition discharge is recorded after the discharge matrix below."
**ASN-0093, after the lemma matrix**: "...are not state-dependent in their conclusions and so require no per-transition discharge; their once-and-for-all status as ASN-0040 citations is established in *Per-chain disciplines* above."

**Problem**: This single fact (chain disciplines are citations, no per-transition discharge) is asserted in the framing preamble (forward-pointing "below"), in the post-matrix recap (back-pointing "above"), in the base-case "Derived lemmas at Σ₀" paragraph, and established in *Per-chain disciplines* itself. The framing/post-matrix pair is a mutual-deferral pointer loop around content stated elsewhere — exactly the "multiple paragraphs defer to the same downstream location" pattern.

**Required**: State once, in *Per-chain disciplines*. Remove the forward-pointer sentence in the framing preamble and the recap paragraph after the lemma matrix.

### Issue 3: Subsequent-emit discharge duplicated verbatim across C1c and L1c

**ASN-0093, C1c chain exhibition (subsequent-emit) and L1c chain exhibition (subsequent-emit)**: the two paragraphs are identical modulo `content ↔ link` (`a_prev`/`t_{n+1}`/`A_C(d)`/`ChainElementT4Validity` ↔ `ℓ_prev`/.../`A_L(d)`), down to the same TA5a/TA5(c)/ChainEnumerationInjectivity/ChainMembershipForOrigin/ChainDiscipline citation sequence and the same strengthened-clause bookkeeping.

**Problem**: Two paragraphs saying the same thing in different words. The note already consolidates by acknowledgment for the *first-emit* length difference, but writes the subsequent-emit case out twice when it is structurally identical (extend the IH chain by one `inc(·, 0)` step).

**Required**: Discharge the subsequent-emit case once, noting it is identical for C1c and L1c modulo content↔link substitution.

### Issue 4: FirstEmission enumerates its downstream consumers

**ASN-0093, FirstEmission lemma, Anchor-construction admissibility**: "*Anchor-construction admissibility (cited downstream).*" ... "This establishes the T4-validity of `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`) and supplies the per-step admissibility that the C1c and L1c chain exhibitions cite."

**Problem**: Use-site inventory — the lemma's own statement names which downstream sections consume it ("cited downstream", "that the C1c and L1c chain exhibitions cite"). The admissibility result stands on its own; the consumer list is the dependency-graph's job, not the lemma's.

**Required**: State the per-step admissibility result and drop the "(cited downstream)" tag and the closing consumer enumeration.

### Issue 5: "Active" definition restates the operation precondition instead of advancing the definition

**ASN-0093, Active sub-allocator chains**: "Concretely, 'active' is the predicate under which K.α (resp. K.λ) admits the chain as the emission source for an address with `origin(·) = d`: the operation's precondition requires `d ∈ dom(M)`, which is exactly the activation condition."

**Problem**: Circular restatement. The definition already says "active at Σ iff `d ∈ dom(M)` at Σ"; this sentence then observes the precondition requires `d ∈ dom(M)` "which is exactly the activation condition." It adds nothing the one-line definition did not already fix. (The following sentence on permanence-via-M1 *is* substantive — keep it.)

**Required**: Delete the "Concretely..." sentence; retain the definition and the permanence-of-activation note.

### Issue 6: Worked example derives cross-document disjointness twice per step

**ASN-0093, Worked example Steps 5 and 9**: "Since `d ≠ d'` and both anchors are `B6`-valid, ASN-0040's B7 gives `A_·(d) ∩ A_·(d') = ∅` directly. Illustrating the equivalent anchor-incomparability (T10 form): ..." followed by a full by-hand position-`#d+1`/position-3 divergence computation.

**Problem**: Each step states the conclusion via B7 "directly," then re-derives the same disjointness by hand through T10 anchor-incomparability — the same conclusion computed two ways, repeated across both Step 5 and Step 9. One route is redundant verification.

**Required**: Keep the by-hand T10 computation (it exercises the prefix-comparable vs prefix-incomparable cases concretely) and drop the "B7 gives it directly" one-liner, or vice versa — not both, and not in both steps.

## OUT_OF_SCOPE

(none — deferred topics are properly enumerated under *Deferred to higher-layer ASNs* and Open Questions.)

VERDICT: REVISE
