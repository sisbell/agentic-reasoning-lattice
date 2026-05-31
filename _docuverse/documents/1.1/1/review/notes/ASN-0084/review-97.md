# Review of ASN-0084

## REVISE

### Issue 1: "S8-uniq" reuses a foundation property name for a strictly weaker statement, then claims a non-maximal partition satisfies it

**ASN-0084, "Correspondence-Run Decomposition Transformation" intro and R-BLK**: "We apply two of S8's clauses per-position and label them mnemonically: *S8-cons* ... and *S8-uniq* for the uniqueness of the containing run." Later: "Together these yield the E! quantification of S8-uniq on dom(M'(d))."

**Problem**: In the foundation, S8's uniqueness postcondition (c) is "*the maximal-run decomposition is unique*." The ASN rebinds the name "S8-uniq" to a per-position property — each position lies in exactly one run — which for any partition is just partition-ness (disjoint + cover), trivially weaker than maximal-decomposition uniqueness. R-BLK then explicitly produces a partition B' that "need not itself coincide with the maximal (canonical) partition" and asserts it "yield[s] the E! quantification of S8-uniq." Under the foundation reading this assertion is *false* (B' is not the unique maximal decomposition); it is only true under the ASN's silently weakened reading. A reader carrying the foundation meaning of S8's uniqueness will misread R-BLK as claiming B' is canonical, which the ASN elsewhere denies.

**Required**: Do not overload the foundation property name. Rename the per-position notion (e.g., "run-partition disjointness/coverage") and state plainly that R-BLK establishes B' is *a* run partition — disjoint and covering — and does **not** establish maximality. Keep the genuine content (the T10 cross-subspace disjointness + coverage argument), just stop labeling it with S8's uniqueness name.

### Issue 2: EXT-VAC over-derives an exhaustiveness characterization beyond the single fact any proof consumes

**ASN-0084, "Consequences of R-PRE" (EXT-VAC)**: the paragraph derives "R-PRE forces ord(c_{n−1}) ≤ N + 1, and the only R-PRE-admissible empty-right-exterior configuration is the single value ord(c_{n−1}) = N + 1."

**Problem**: The only downstream consumer is R-BLK Phase 1: "EXT-VAC then gives c_{n−1} ∉ dom(M(d)) with empty right exterior, so no run straddles it." That consumer needs only the implication *"c_{n−1} ∉ V_S(d) ⟹ right exterior empty and c_{n−1} ∉ dom(M(d))"* — which is essentially immediate from D-SEQ. The multi-step derivation bounding `ord(c_{n−1}) ≤ N + 1` and characterizing the unique admissible value is exhaustiveness padding: no postcondition proof (R-PIV, R-SWP, R-PPERM, R-SPERM, R-BLK) uses the bound or the "single value" characterization. The reader must work through a defensive boundary argument that advances none of the operation's guarantees. This is the meta-prose accretion the note's classifier targets.

**Required**: Reduce EXT-VAC to the one fact R-BLK consumes (empty exterior ⟹ cut ∉ dom, no straddle). Drop the `ord(c_{n−1}) ≤ N + 1` derivation and the "only admissible configuration" characterization, or relocate the boundary illustration into the boundary worked example where it is actually exercised.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond the depth-2 text subspace
The ASN restricts `m_1 = 2` and builds the singleton-tumbler/natural-number identification on it. Foundation D-CTG-depth already reduces contiguity at depth `m ≥ 3` to the last component, suggesting the operation generalizes. Lifting the restriction (ord as last-component projection for arbitrary `m`) is genuine new work, not an error in this ASN.

### Topic 2: k > 4 cut sequences and composition of rearrangements
The natural permutation class for `k > 4`, and whether composing two rearrangements is itself a rearrangement, are correctly deferred to Open Questions — future territory.

### Topic 3: Weakest-precondition analysis
The wp for establishing the post-state invariant suite is posed as an open question rather than derived. Acceptable to defer, though a future ASN should discharge it.

META: (none — the ASN specifies state, an operation on state, and its invariants abstractly; it has not drifted into implementation mechanics.)

VERDICT: REVISE
