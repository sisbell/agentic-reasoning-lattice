# Review of ASN-0116

## REVISE

### Issue 1: Valid-composite argument forward-references the lemmas it depends on

**ASN-0116, "INSERT as a valid composite over the K-vocabulary"**: The K.μ⁺ precondition discharge asserts "(ii) every added V-position is S8a-well-formed of depth `m` **(shown below)**" and "(iii) the resulting content subspace `{q₁, …, q_{N+n}}` is the dense run, so S8-depth, D-CTG★, D-MIN★ hold." The closing sentence likewise defers "clause 2 (the coupling constraints J0, J1★, J1'★) discharged at the composite boundary in the provenance section below."

**Problem**: The section *concludes* that INSERT is a valid composite, yet three prerequisites of that conclusion are proved only in the *following* section ("The document remains one coherent sequence"): the new block's S8a/depth, the density of the post-state domain (I-DOM), and the coupling discharge (PROV). Clause (iii) in particular silently uses I-DOM — the post-state domain characterization — which is established later. The reader cannot verify K.μ⁺'s preconditions, hence cannot verify validity, hence cannot license the appeal to ExtendedReachableStateInvariants, without jumping forward. This is the forward-reference accretion pattern: the assembly claim precedes its own lemmas, with two deferrals pointing into the same downstream section. Compounding this, the section opens by restating ASN-0047's `ValidComposite★` definition verbatim rather than citing it.

**Required**: Reorder so that block well-formedness (S8a/depth), the domain characterization (I-DOM), and the coupling discharge are established *before* the validity claim, then assemble. Replace the restated `ValidComposite★` definition with a citation. Remove the "(shown below)" / "discharged...below" deferrals once the order is linear.

### Issue 2: Post-state contiguity stated in unstarred (ASN-0036) form when the operative invariants are starred (ASN-0047)

**ASN-0116, "The document remains one coherent sequence"**: "Therefore `V_S(d') = {q₁, …, q_{N+n}}` is the canonical dense run... This *is* the D-SEQ/D-MIN/D-CTG property of the post-state, established for INSERT rather than borrowed."

**Problem**: The note declares it "works inside ASN-0047's extended state," whose reachable-state theorem requires the *starred* per-subspace invariants D-CTG★, D-MIN★, D-SEQ★ — and the amended K.μ⁺ precondition (ASN-0047) requires D-CTG★/D-MIN★, which the valid-composite section correctly cites in starred form. The coherence section then concludes the *unstarred* D-SEQ/D-MIN/D-CTG (ASN-0036). On subspace `s_C` the two coincide, so this is not a soundness gap, but the labels are inconsistent with the operative state model and with the same ASN's own starred usage a section earlier.

**Required**: State the post-state contiguity conclusion in the starred forms (D-CTG★/D-MIN★/D-SEQ★) that ExtendedReachableStateInvariants and the amended K.μ⁺ actually require, or note explicitly that on `s_C` the starred forms reduce to the unstarred ones being cited.

## OUT_OF_SCOPE

The four Open Questions (transclusion at a shared position, concurrent insertion freshness, transclusion provenance, post-fragmentation obligations) are correctly framed as future work and define no claims; no action needed.

VERDICT: REVISE
