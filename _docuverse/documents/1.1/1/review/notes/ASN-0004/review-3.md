# Review of ASN-0004

## REVISE

### Issue 1: INS1 contiguity is prose, not formal
**ASN-0004, Fresh address allocation**: "The freshly allocated addresses form a contiguous range in I-space: if a₀ is the starting address, the allocation produces {a₀, a₀+1, ..., a₀+#c-1}"
**Problem**: The formal INS1 is existential over an arbitrary set S of size #c. Contiguity and the definition of a₀ appear only in the surrounding prose. Every subsequent formal property — INS2, INS3, INS1a, INS-F1, INS5, INS-F6, INS-CORR — references `a₀ + i`, which is well-defined only if S is contiguous and a₀ is its minimum. Without formal contiguity, a₀ is a prose name with no formal anchor, and `a₀ + i` could refer to addresses outside S.
**Required**: Strengthen INS1's formal statement to assert contiguity (e.g., `(E a₀ : a₀ ∈ Addr ∧ {a₀, ..., a₀+#c-1} ∩ dom.ispace = ∅ : {a₀, ..., a₀+#c-1} ⊆ dom.ispace')`), or add a companion property INS1b that formally binds a₀ and asserts `S = {a₀ + i : 0 ≤ i < #c}`.

### Issue 2: Missing owner frame condition
**ASN-0004, The frame / INS-CORR**: The state vocabulary includes `owner(d)`, and PRE2 requires `user = owner(d)`. No frame condition asserts `owner' = owner`.
**Problem**: INS-CORR claims to be a "complete correctness" characterization — clauses (i)–(vii) — but omits owner. The specification technically permits INSERT to reassign document ownership. This is the classical frame problem the ASN itself identifies for INS-F5 ("silence is not a frame condition"). The same argument applies here: INS-CORR's silence about owner does not guarantee owner is preserved.
**Required**: Add a frame condition `(A d' : owner'(d') = owner(d'))` and include it as clause (viii) of INS-CORR.

### Issue 3: S-DISJ preservation not verified
**ASN-0004, Invariant preservation / S4**: The S4 proof's cross-subspace case relies on S-DISJ holding in the post-state: "By S-DISJ, text and link I-addresses are drawn from disjoint ranges, so the two I-addresses are necessarily distinct."
**Problem**: The invariant preservation section verifies S0–S5 but not S-DISJ. S-DISJ is introduced in "The state we need" and treated as a structural property of the allocation scheme, but this status is never made explicit. If S-DISJ is an allocation-scheme axiom (always true by construction), it should say so — then per-operation verification is unnecessary. If it is a state invariant, INSERT must be shown to preserve it (straightforward via INS1a, but currently unstated). As written, the S4 proof has a dependency on an unverified property.
**Required**: Either (a) explicitly classify S-DISJ as an axiom of the allocation scheme that holds by construction and therefore does not require per-operation verification, or (b) add S-DISJ to the invariant preservation section with a short proof (INSERT allocates only TEXT-subspace addresses by INS1a; link I-addresses are unchanged; disjointness is preserved).

## OUT_OF_SCOPE

### Topic 1: INSERT and version creation
The ASN specifies INSERT as a state transition but does not address whether INSERT creates a new version in the version DAG, or whether multiple INSERTs accumulate within a single version until an explicit checkpoint.
**Why out of scope**: Version management is a separate concern — the version DAG, CREATENEWVERSION, and the relationship between editing operations and version boundaries belong in a dedicated ASN.

### Topic 2: Concurrent INSERT semantics
The open questions ask about concurrent insertions from multiple front-ends. The ASN specifies INSERT as a sequential state transition; interleaving and merge semantics are unexplored.
**Why out of scope**: Concurrency is new territory requiring its own treatment (ordering, conflict resolution, convergence). The sequential specification is the correct foundation to build on.

VERDICT: REVISE
