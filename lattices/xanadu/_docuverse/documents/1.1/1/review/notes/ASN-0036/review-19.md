# Review of ASN-0036

## REVISE

### Issue 1: Phantom foundation references — GlobalUniqueness
**ASN-0036, §Content identity (S4) and §Structural attribution (S7)**: "S4 follows from GlobalUniqueness (ASN-0034)" and "uniquely identifying the allocating document across the system (by GlobalUniqueness, ASN-0034, which covers all cases: same-allocator monotonicity, non-nesting prefixes, and nesting prefixes distinguished by length)"

**Problem**: "GlobalUniqueness" does not appear in the ASN-0034 formal export. The property is real — distinct allocations produce distinct tumblers — but it is a composite of T9 (ForwardAllocation: same-allocator monotonicity gives distinctness) and T10 (PartitionIndependence: cross-allocator subtrees are disjoint). Citing a label that doesn't exist in the foundation breaks the derivation chain. A reader checking S4's or S7's provenance will find no "GlobalUniqueness" to verify.

**Required**: Replace every citation of "GlobalUniqueness (ASN-0034)" with "T9 and T10 (ASN-0034)" and spell out the two cases: T9 covers same-allocator distinctness (later allocations are strictly greater, hence distinct); T10 covers cross-allocator distinctness (non-nesting prefixes yield disjoint subtree populations). The properties table entries for S4 and S7 must be updated accordingly.

### Issue 2: Phantom foundation reference — PrefixOrderingExtension
**ASN-0036, §Span decomposition (S8 cross-subspace uniqueness proof)**: "By PrefixOrderingExtension (ASN-0034), if s₁ ≠ s₂ and neither [s₁] nor [s₂] is a prefix of the other... all extensions of [s₁] and all extensions of [s₂] occupy entirely disjoint intervals"

**Problem**: "PrefixOrderingExtension" does not appear in the ASN-0034 formal export. The claimed property follows from T5 (ContiguousSubtrees: extensions of any prefix form a contiguous interval under T1) combined with T10 (PartitionIndependence: non-nesting prefixes yield distinct tumblers). Two disjoint contiguous sets under a total order cannot interleave — so the extensions of [s₁] and [s₂] are separated. The logic is sound; the label is phantom. The properties table lists "PrefixOrderingExtension" as a derivation basis for S8.

**Required**: Replace "PrefixOrderingExtension (ASN-0034)" with "T5 and T10 (ASN-0034)" in the S8 proof text and in the properties table. One sentence suffices: T5 gives contiguity of each prefix's extensions; T10 gives disjointness; together they give separation.

### Issue 3: Worked example does not verify D-CTG, D-MIN, or D-SEQ
**ASN-0036, §Worked example**: The multi-step scenario checks S0, S3, S5, S7, S8, S9 at each state transition but never mentions D-CTG, D-MIN, or D-SEQ — design constraints introduced in this same ASN.

**Problem**: The three states Σ₁, Σ₂, Σ₃ each have well-formed V-position sets that satisfy D-CTG and D-SEQ trivially (contiguous ranges starting at [1,1]). The D-CTG section has its own dedicated examples, but the worked example is the ASN's primary multi-step grounding scenario and should verify all introduced invariants. State Σ₃ (post-deletion) is particularly relevant: V₁(d₁) shrinks from five positions to two, and noting that {[1,1], [1,2]} satisfies D-CTG/D-MIN/D-SEQ completes the verification without adding more than a line per state.

**Required**: Add D-CTG, D-MIN, and D-SEQ checks to each of the three worked-example states. For Σ₁ and Σ₂: note that V₁(d) = {[1,k] : 1 ≤ k ≤ 5} satisfies D-SEQ with n = 5. For Σ₃: note that V₁(d₁) = {[1,k] : 1 ≤ k ≤ 2} satisfies D-SEQ with n = 2; V₁(d₂) is unchanged.

## OUT_OF_SCOPE

### Topic 1: Maximal (fewest-runs) span decomposition
**Why out of scope**: S8 proves existence of a decomposition (via the trivial singleton construction) but does not address uniqueness of the maximal form. Whether every arrangement has a unique coarsest partition into correspondence runs is a combinatorial question about the interaction of M(d) with tumbler arithmetic — new territory the ASN correctly identifies as an open question.

### Topic 2: Operation-specific preservation of D-CTG, D-MIN, D-SEQ
**Why out of scope**: The ASN introduces these as design constraints on well-formed states and explicitly defers verification that each operation (INSERT, DELETE, COPY, REARRANGE) preserves them. This is the correct factoring — each operation's ASN owns its own preservation proof.

### Topic 3: Computability bounds for the sharing inverse
**Why out of scope**: The ASN establishes that the sharing relation is determined by the state (the information is present) but correctly defers efficiency questions. Cost bounds for "given I-address a, find all documents referencing a" depend on indexing structure, which is implementation territory.

VERDICT: REVISE
