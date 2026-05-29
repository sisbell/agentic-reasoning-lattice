# Review of ASN-0040

This is a strong, largely sound development — the core induction skeleton (B0a → B0/B0★, B₀ conf. → B1/B_fin/B10, S(p,d) → S0/S1 → B2/B7/B8/B9) closes without circularity, and the layered dependency between Bop's freshness and B1 is handled correctly (B1's induction never invokes Bop freshness). The trace and B9 worked example satisfy the concrete-example requirement. My findings are dominated by the `anti-bloat` mode: meta-prose and repeated deferrals that the precise reader must read past. Two substantive precision points also stand.

## REVISE

### Issue 1: The same B4 read-consistency claim is deferred three times
**ASN-0040, Bop / Bop-freshness / B1**:
- Bop: "The read next(s.B, p, d) is against the precondition state s (by B4, §B4 below)."
- Bop freshness: "The value of children(s.B, p, d) used here is the same value committed by that edge (by B4)."
- B1 target case: "The value of children(B, p₀, d₀) appearing in the postcondition is read against the same precondition state B that licenses the transition (by B4)."

**Problem**: Three paragraphs in three sections defer to B4 for the identical fact (the registry read is taken against the precondition state). This is the "multiple paragraphs defer to the same downstream location" accretion pattern; each restatement forces the reader to re-confirm the same thing.
**Required**: State the read-against-precondition-state semantics once (in B4) and let the proofs cite it without re-narrating it.

### Issue 2: Bop precondition slot carries proof-bookkeeping essay
**ASN-0040, Bop, Formal Contract / Preconditions**: "(B1, B10, and B_fin are *state invariants*, not per-call obligations: they are established at genesis by B₀ conf. and preserved inductively by the proofs in §B1, §B10, and §B_fin, so they hold in every reachable state at which baptize(p, d) can be invoked. They are appealed to in the well-definedness and preservation arguments below but are not discharged by the caller.)"
**Problem**: This is an explanation of the proof architecture sitting in a precondition slot, not a precondition. It advances no reasoning the §B1/§B10/§B_fin proofs do not already carry.
**Required**: Reduce to a single clause — "B1, B10, B_fin are reachable-state invariants, not caller obligations" — and drop the rest.

### Issue 3: B6 has a redundant summary that previews its own proof
**ASN-0040, B6 intro**: "The three conditions together are necessary for the baptism system to maintain its invariants — each rules out a distinct failure, with (iii)'s independent contribution arising at d = 2."
**Problem**: This restates the per-condition analysis given in the immediately preceding three sentences and previews the proof's sub-case structure ("established in the necessity proof's sub-cases (a) and (b) below"). Pure use-site inventory.
**Required**: Delete; the per-condition sentences and the proof already carry it.

### Issue 4: B4 leaks an implementation/concurrency rationale
**ASN-0040, B4**: "B4's scope is *per-namespace*: B7 guarantees baptisms under distinct (p, d) pairs produce disjoint outputs, so the minimum serialization grain is the namespace, not the entire system."
**Problem**: "Minimum serialization grain" is an implementation concurrency-control claim, not a statement of what B4 (atomicity of the transition) asserts. It is rationale around the axiom, not the axiom's content.
**Required**: Remove the serialization-grain sentence, or relocate it to a non-normative remark; B4 should say what it constrains (single atomic edge), not editorialize about locking granularity.

### Issue 5: B8 prose paragraph duplicates the B8 proof
**ASN-0040, B8**: the paragraph "Within the same namespace, B4 makes each baptize(p, d) a single edge of the transition graph; distinct same-namespace baptismal transitions occupy distinct edges... Across namespaces, B7 ensures non-overlapping ranges."
**Problem**: This says, in prose, exactly what the subsequent Case 1 / Case 2 proof says. Two passages, same content.
**Required**: Keep the proof; drop the preview paragraph (or compress it to a one-line statement of the two-case split).

### Issue 6: B0a restates B6 before B6 is defined
**ASN-0040, B0a**: "Here 'satisfying B6' means p satisfies T4, d ∈ {1, 2}, and zeros(p) + (d − 1) ≤ 3 — depth validity as defined below."
**Problem**: Duplicates the B6 definition verbatim ahead of its site. The reader will re-read the same three conditions at B6.
**Required**: "satisfying B6 (Valid Depth, below)" suffices.

### Issue 7: "not addressable" overclaims in B3
**ASN-0040, B3**: "t ∉ s.B ∧ ¬Occupied(t, s): an unbaptized, unoccupied position (not addressable)."
**Problem**: Every t ∈ T is addressable by the algebra — T1 totally orders all of T, and an unbaptized tumbler is a perfectly well-formed address. "Not addressable" conflates "not baptized" with "not a valid address," contradicting the ASN's own point that the algebra cannot distinguish assigned from assignable positions.
**Required**: Replace "(not addressable)" with "(not a baptized position / not a system entity)."

### Issue 8: B7/B8/S0 substantially re-derive foundation results without acknowledging the parallel
**ASN-0040, B7, B8, S0**: B7 (namespace disjointness) re-proves the substance of T10a.6 (DomainDisjointness)/T10a.5; B8 re-proves GlobalUniqueness; S0 re-proves T10a.7 (EnumerationInjectivity); S(p,d) parallels T10a's per-allocator inc(·,0) chain with d playing the role of the child-spawn parameter k'∈{1,2}.
**Problem**: The reader cannot tell whether baptism *is* the allocator discipline at the registry level or a genuinely distinct layer. If it is the same mechanism, the re-derivation is reinvention (rule 7); if distinct, the relationship should be stated rather than left implicit. The ASN does flag the bridge (`allocated(s) ⊆ s.B`) as an open question, which partly justifies the standalone proofs — but B7/B8/S0 do not say "this restates the foundation guarantee at the committed-registry level because the allocation↔baptism bridge is not yet available."
**Required**: Either cite the foundation results where the registry-level proof mirrors them and state explicitly why the restatement is needed (no allocation↔baptism bridge yet), or, if baptism is meant to *be* the allocator discipline, build on T10a directly rather than re-proving S0/B7/B8.

## OUT_OF_SCOPE

### Topic 1: The allocation↔baptism bridge (`allocated(s) ⊆ s.B`)
**Why out of scope**: Correctly deferred in the Open Questions. Establishing when allocator-extension transitions align with baptismal operations is new territory, not a defect here.

### Topic 2: Parent-prerequisite chain (must p be baptized before its children?)
**Why out of scope**: Bop explicitly imposes no parent-baptized prerequisite and the ASN defers this to the ownership model; this is consistent with the stated scope.

### Topic 3: Ghost/structural-position distinction and Occupied semantics
**Why out of scope**: B3 is correctly stated as a forward requirement parametric in `Occupied`; content storage is out of scope, and B3 does not define it.

VERDICT: REVISE
