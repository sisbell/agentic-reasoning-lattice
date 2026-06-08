# Review of ASN-0100

## REVISE

### Issue 1: Citation-strategy meta-prose and downstream-consumer inventory in INS.I3-coincide
**ASN-0100, §Effect Three (Identification with the foundation's post-insertion shift)**: "We record the consequence once, here, and cite it directly in the verification sections below without rebuilding the premise: on Left ∪ Shifted-right, `M'(d)` inherits I3-S2 (PostInsertionFunctionality), I3-S3 (PostInsertionReferentialIntegrity), I3-VP (PostInsertionWellFormedness), I3-VD (PostInsertionDepthUniformity), and I3-fin (PostInsertionFiniteness), all from ASN-0082."
**Problem**: The clause "We record the consequence once, here, and cite it directly in the verification sections below without rebuilding the premise" is meta-prose describing the document's citation strategy, not the mathematics. The enumeration of which downstream invariants inherit (I3-S2/S3/VP/VD/fin) is a use-site inventory — it lists consumers rather than advancing the claim. The load-bearing content is simply: M'(d) coincides pointwise with M_{I3} on Left ∪ Shifted-right, so I3's per-state properties transfer there.
**Required**: Keep the pointwise-coincidence statement and the transfer principle; drop the citation-strategy sentence and the I3-* inventory. Each verification section already names the specific I3 lemma it uses at the point of use.

### Issue 2: Multiple sections defer to the same downstream location ("the S7 bullet")
**ASN-0100, §Link store unchanged, §Atomicity (link-store bullet), §Atomicity (K.α and K.ρ frame M)**: three separate paragraphs route the discharge of the fresh `a_k` content invariants to "the per-address paragraph of §Post-state V-position well-formedness (S7 bullet)" — e.g. "is discharged once, for both the K.α intermediates and the boundary, in the per-address paragraph of §Post-state V-position well-formedness (S7 bullet)"; "discharged per-address with the other content invariants of the fresh `a_k` in §Post-state V-position well-formedness (S7 bullet)"; "are discharged in the per-address paragraph of §Post-state V-position well-formedness (S7 bullet) … we do not repeat that discharge here."
**Problem**: This is the forward/cross-reference accretion pattern: several sections in different places defer to one location, and one adds the explicit "we do not repeat that discharge here." The deferrals are pointer-bookkeeping that the reader must chase; the "we do not repeat" clause is pure meta-prose.
**Required**: Establish L0's content clause and the per-address S7a/S7b/C1b/C1c/L0 facts once at the K.α discharge, and let later sections rely on it by a single bare citation (or by the general "P0 carries per-address facts to all intermediates" principle) without restating the deferral or narrating that it is not being repeated.

### Issue 3: "Why the lemma applies" justifications attached to foundation citations
**ASN-0100, §Coverage and link discoverability**: "(LP3★ extends to multi-step compositions, so it discharges the property across the substrate composite, not just per-step.)" and, in the INS.proj `d' ≠ d` case, "LP4 (ArrangementSpecificity; ASN-0098) applied at each step (its hypothesis `M_{j+1}(d') = M_j(d')` is met by that step's frame)…".
**Problem**: These parentheticals explain why a foundation lemma is invokable rather than advancing the projection derivation. The multi-step reach of LP3★ and the frame-discharges-LP4 hypothesis are properties of the cited foundation lemmas; restating them at each use is accretion.
**Required**: Cite LP3★/LP4 directly; drop the inline rationale for their applicability. If the per-step frame must be named, one mention suffices.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L) semantics
**Why out of scope**: The ASN correctly bounds itself to the content subspace and lists link-subspace insertion among the explicitly excluded topics; the Open Question about link-subspace invariants is a future-ASN pointer, not a gap here.

### Topic 2: Partial-failure recovery, INSERT self-composition, concurrency, derived-size updates
**Why out of scope**: These are raised as Open Questions and are genuinely new territory (implementation recovery, operation algebra, concurrency control, derived state), not defects in this ASN's per-state INSERT contract.

VERDICT: REVISE
