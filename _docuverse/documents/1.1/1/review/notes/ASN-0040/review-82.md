# Review of ASN-0040

## REVISE

### Issue 1: S0's re-derivation note is forward-reference accretion
**ASN-0040, §"The sibling stream", S0**: "S0 mirrors T10a.7 (EnumerationInjectivity); it is re-derived here from TA5(a) pending the `allocated(s) ⊆ s.B` alignment (Open Questions)."
**Problem**: This sentence explains *why* S0 is re-derived and defers to an Open Question, rather than advancing S0's content. It is meta-prose justifying document structure ("re-derived here... pending the alignment"). The re-derivation itself is fine; the explanatory framing is noise the precise reader must skip.
**Required**: Delete the note. If a pointer to the analogous foundation property is wanted, it belongs nowhere in the claim body — the proof from TA5(a) and T1 stands on its own.

### Issue 2: B7's "B6(i)'s role is visible" paragraph is defensive justification
**ASN-0040, §"Namespace disjointness"** (after the B7 proof): "B6(i)'s role is visible in the unequal-length case... Without it... distinct pairs (p, d) ≠ (p', d') could share a stream and B7 would be false. Requiring (i) admits exactly one of each such pair, making the disjointness statement well-posed."
**Problem**: This explains *why precondition (i) is needed* rather than what the claim says — the precise pattern flagged for anti-bloat review. The concrete aliasing example (`([1,0],1)` vs `([1],2)`) is legitimate content; the surrounding "B6(i)'s role is visible... would be false... well-posed" framing is not.
**Required**: Keep the one-line counterexample if it earns its place; strip the "role is visible / would be false / well-posed" justification scaffolding around it.

### Issue 3: B₀ conf. quantifies over all (p, d) but only B6-valid namespaces are used
**ASN-0040, §"Seed conformance", B₀ conf.**: "`(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))`"
**Problem**: The universal quantifier ranges over *every* (p, d), but B1's base case consumes it only "for every B6-valid (p, d)" ("a fortiori for every B6-valid"), and `next`/`hwm`/B10 are likewise B6-restricted. The seed requirement is strictly stronger than anything downstream uses. Since an Open Question already asks "What concrete seed sets B₀ are valid," an over-broad conformance condition makes that question harder than it needs to be.
**Required**: Either restrict the quantifier to B6-valid (p, d), or justify in the proof where contiguity over non-B6 streams is actually needed. As written it is an unused obligation.

### Issue 4: Imprecise foundation citation in B6
**ASN-0040, §"Depth and field structure", B6**: "Condition (ii) follows from the ASN-0034 lemma 'TA5 preserves T4'".
**Problem**: There is no foundation property named "TA5 preserves T4." The relevant foundation claim is TA5a (IncrementPreservesT4), which the proof body does cite correctly. The informal paraphrase in the prose invites confusion about which property is being invoked.
**Required**: Name TA5a directly.

## OUT_OF_SCOPE

### Topic 1: Cross-branch (divergent-path) address uniqueness
B8 proves uniqueness only for *co-reachable* baptismal acts (both on one path `s_init →* s`). Uniqueness across divergent branches of a version DAG, or across replicas, is unproven here.
**Why out of scope**: This is genuinely new territory — it depends on the distributed/cross-replica ordering question already listed in Open Questions, and on the foundation's GlobalUniqueness. The co-reachable scoping is stated honestly and is not an error in this ASN.

VERDICT: REVISE
