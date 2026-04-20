# Review of ASN-0036

## REVISE

### Issue 1: S8 property table omits T3 as a dependency
**ASN-0036, Properties Introduced table (S8 row)**: Status lists "theorem from S8-fin, S8a, S2, S8-depth, T1, T5, T10, TA5(c), TA7a (ASN-0034)"
**Problem**: The singleton partition uniqueness proof (same-subspace, j = d case) concludes "Therefore t = v" from the fact that t and v agree on all d components with equal length. This step is T3 (CanonicalRepresentation): `a = b ⟺ #a = #b ∧ (∀i: aᵢ = bᵢ)`. T3 is not listed in S8's dependency column. The same implicit use of T3 appears in D-CTG-depth's proof (distinct n values yield distinct w by T3's contrapositive), where T3 is also unlisted.
**Required**: Add T3 (CanonicalRepresentation, ASN-0034) to the S8 and D-CTG-depth dependency lists.

### Issue 2: S8 dependency should cite TA5, not just TA5(c)
**ASN-0036, Properties Introduced table (S8 row)**: Status lists "TA5(c)"
**Problem**: The proof uses two sub-properties of TA5. TA5(c) (inc(v,0) changes only position sig(v), preserving length) is cited explicitly for the uniqueness argument. But TA5(a) (inc(t,0) > t, strict increase) is also required: the singleton interval [v, v+1) is non-empty only because v < v+1, which is TA5(a). The partition property S8(a) quantifies `vⱼ ≤ v < vⱼ + nⱼ`, so the strict inequality v < v+1 is load-bearing — without it the singleton interval degenerates.
**Required**: Broaden "TA5(c)" to "TA5" in S8's dependency list (or list TA5(a) and TA5(c) separately).

## OUT_OF_SCOPE

### Topic 1: Unique maximal run decomposition
**Why out of scope**: S8 proves existence of a finite decomposition (via singletons) but does not address uniqueness or maximality. Whether a canonical "fewest-runs" decomposition exists is a structural question about the arrangement, not an error in S8. Already noted in the ASN's open questions.

### Topic 2: Operation-specific preservation of D-CTG, D-MIN, D-SEQ
**Why out of scope**: The ASN correctly identifies this as a verification obligation for each operation's ASN. D-CTG is introduced as a design constraint; whether INSERT, DELETE, COPY, and REARRANGE preserve it is future work. The ASN's scoping is explicit and correct.

### Topic 3: Origin function and version structure
**Why out of scope**: S7's origin(a) extracts the full document field D, which per the shared vocabulary encodes "the document and version." The precise relationship between document identity and version identity — whether origin distinguishes versions of the same document — depends on version semantics, which is explicitly out of scope.

VERDICT: REVISE
