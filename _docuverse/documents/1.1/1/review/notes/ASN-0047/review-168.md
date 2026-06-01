# Review of ASN-0047

## REVISE

### Issue 1: Cited ASN-0036 property "S9" does not appear among that foundation's claim statements
**ASN-0047, intro and ExtendedTransitionInvariants**: "arrangement mutations cannot alter the content store (S9)"; "ASN-0036's S9 (TwoStreamSeparation) — arrangement mutations cannot alter the content store — follows from P0."
**Problem**: S9 is cited as a named, load-bearing inherited property of ASN-0036 (it also appears in ExtendedReachableStateInvariants: "P3 ... and S9 are per-transition"). But ASN-0036's extracted claim statements run S0–S8 plus D-CTG/D-MIN/D-SEQ and contain no S9 (nor S6). A reader cannot confirm the referenced property exists. The substance is fine — the ASN actually *derives* the content ("follows from P0 by the arrangement frames") — so the dependency is on the label, not the result.
**Required**: Either correct the attribution (S9 is not in ASN-0036's claim set as extracted) or drop the named citation and rely solely on the local derivation from P0. If S9 genuinely exists in ASN-0036, the foundation extract should be reconciled so the reference resolves.

### Issue 2: ParentAllocatorDispatch carries a use-site inventory rather than advancing the lemma
**ASN-0047, *Allocator hierarchy under documents* (ParentAllocatorDispatch)**: "The cited sites below (*K.δ case (ii) discharge*, the worked examples) invoke this sub-lemma by name rather than re-derive the routing."
**Problem**: This sentence enumerates downstream consumers of the lemma and explains a citation convention; it advances neither the statement nor the proof. It is exactly the "definition's introduction enumerates downstream consumers" pattern the anti-bloat note flags. The lemma's content (the (a')/(b') routing by T10a.6) stands on its own.
**Required**: Delete the use-site inventory sentence. Downstream sites already cite the lemma by name; the lemma need not announce that they will.

### Issue 3: K.μ⁻ "Excluded shapes (side remark)" imagines configurations the constructive precondition already excludes
**ASN-0047, *Amendments to existing transitions*, K.μ⁻ admissible contraction shape**: "*Excluded shapes (side remark).* Configurations with an interior hole — ... violate D-CTG★ ... Configurations with a missing minimum — ... violate D-MIN★. Both are therefore excluded by the constructive form and reverse-confirmed by the per-state invariants."
**Problem**: The constructive precondition (`M'(d) = M(d) ↾ R` with per-subspace prefix `R`) already produces only the suffix-prefix shape; the equivalence proof immediately preceding establishes that interior-hole and missing-minimum configurations cannot arise. Re-stating that they "are therefore excluded" describes cases the carrier already forecloses — the reviser-drift pattern of imagining an excluded case. It adds no obligation and no new reasoning.
**Required**: Remove the side remark, or compress to at most a one-clause pointer if any reader value remains; do not re-derive exclusions the equivalence proof has already closed.

### Issue 4: Document-ordering and deferral justifications in structural slots
**ASN-0047, *Decomposition of K.μ~* (Preconditions)**: "The necessity and sufficiency of this precondition are proved at *Necessity and sufficiency of the precondition* below, after the proof obligations they consume." Also K.μ~ preamble: "Its bijection equation, admissibility constraints, and derived frame are stated in §*Decomposition of K.μ~* below."
**Problem**: These sentences justify *where* material sits and defer to a downstream location rather than advancing the claim — the "prose justifies document ordering / multiple deferrals to the same location" pattern. The precondition can be stated and a single forward pointer given without narrating the ordering rationale ("after the proof obligations they consume").
**Required**: Replace with a bare cross-reference (or none, since the section heading is adjacent). Drop the ordering rationale clauses.

### Issue 5: S8★ restates "why ASN-0036's S8 cannot apply" multiple times
**ASN-0047, S8★ (per-subspace span decomposition)**: "S8★(s_L) therefore satisfies condition (b) under the substitution `dom(C) → dom(L)`. ... The substitution is the whole reason ASN-0036's S8 cannot apply verbatim to the link subspace." Then again: "cannot use ASN-0036's S8 directly because its range lies in `dom(L)` not `dom(C)`, falsifying S3; S7b/C1b also do not apply ...".
**Problem**: The same point — link-subspace labels reside in `dom(L)`, so S3 (and S7b/C1b) fail and ASN-0036's S8 does not apply verbatim — is made at least twice within the one definition. Two paragraphs in the same passage say the same thing in different words.
**Required**: State the `dom(C) → dom(L)` substitution and its cause once; remove the duplicate explanation.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The Fork composite (J4) explicitly leaves a forked document's link subspace empty and notes that "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." Correctly deferred; the link-discovery-under-transclusion behavior belongs to a future operations/discovery ASN.

### Topic 2: Node-allocation registry mechanism
NodeUniqueAllocation / NodeRegistryBootstrap treat the external node registry as an axiom boundary. The minimal registry protocol (issuing model, persistence, concurrency) is correctly an open question for a future ASN, not a gap in this one. (The Open Questions entry restating Nelson LM 4/17–4/22 and Gregory's granfilade rationale at length is borderline essay-in-slot, but as an open-question context note it is acceptable.)

VERDICT: REVISE
