# Review of ASN-0116

I checked the operation's core: INSERT as a valid composite `K.α`(×n) → `K.μ⁻` → `K.μ⁺` → `K.ρ`(×n), the I3-family arrangement effect, the four named invariants (content immutability, position permanence, link anchoring, document isolation), the provenance coupling, the wp analysis, and the worked insertion with its boundary cases (append, empty subspace, front-insertion). The composite-validity argument is sound — coupling constraints correctly deferred to the boundary, intermediate J0-violation correctly permitted, K.μ⁻ strict-contraction precondition met in every branch, K.μ⁺ targets in `dom(C)`. The contiguity interval argument, the RAN derivation, P4's bijection-not-inclusion treatment, and the P6 containment wp all hold. Two issues, both precision/prose.

## REVISE

### Issue 1: I-DOM attributes the inserted block to lemmas that exclude it
**ASN-0116, "What shifts" (Effect, clause I-DOM)**: "`{v ∈ dom(M'(d)) : subspace(v) = S} = {q_1,…,q_{J-1}} ∪ {q_J,…,q_{J+n-1}} ∪ {q_{J+n},…,q_{N+n}}` — the domain closure ASN-0082 I3-CS/I3-CX specialised to the dense text subspace."
**Problem**: I3-CS (PostInsertionSubspaceClosure) characterizes the *gapped* domain as left ∪ shifted only — the middle interval `{q_J,…,q_{J+n-1}}` is precisely the region I3-V *vacates* and I3-CS *excludes*. The block is contributed by INSERT's own I-NEW fill, not by the cited foundation lemmas. The wholesale citation under-credits I-NEW for the middle interval. The same loose attribution recurs in the Claims table row for I-DOM ("domain closure cites I3-CS/I3-CX"). Section 4's interval argument computes the filled domain correctly; only the Effect-section citation is wrong.
**Required**: Split the attribution — left and shifted intervals from I3-CS/I3-CX (gapped domain); the block `{q_J,…,q_{J+n-1}}` from I-NEW.

### Issue 2: Citation-bookkeeping meta-prose in the composite section
**ASN-0116, "INSERT as a valid composite"**: "This is why the Effect clauses I-SHIFT, I-LEFT, I-NEW, I-DOM may continue to cite the I3 family for their *values* while the *transitions* realising those values are the K-atomics named here."
**Problem**: This sentence advances no part of the argument — it explains the note's own citation strategy (reconciling two reference styles). Under the note's anti-bloat classifier this is essay content occupying a structural slot. The adjacent paragraph ("The arrangement change is *not* itself one of these atomics… which K.μ⁺'s prior-domain agreement… forbids… ASN-0082's I3 family is a displacement *postcondition spec*, not a K-transition") carries the load-bearing motivation for the decomposition; the citation-reconciliation sentence does not.
**Required**: Delete the citation-bookkeeping sentence; keep the substantive motivation for why a single K.μ cannot realize the shift.

## OUT_OF_SCOPE

None. The link-survival (P4), discoverability-wp (P6), and isolation (P5) analyses concern INSERT's effect on *existing* links and other documents — INSERT's own guarantees — not link creation or discovery operations. The four Open Questions correctly route transclusion, concurrency, and post-edit fragmentation to future ASNs.

VERDICT: REVISE
