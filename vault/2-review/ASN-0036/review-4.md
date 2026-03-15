# Review of ASN-0036

## REVISE

### Issue 1: S5 uses derivability operator without model-theoretic support

**ASN-0036, Content identity / Sharing**: "`¬(E N ∈ ℕ :: S0–S3 ⊢ (A Σ reachable, a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| ≤ N))`"

**Problem**: The `⊢` symbol makes a formal derivability claim. To justify non-derivability, you need a model existence argument — exhibit, for each candidate bound N, a state satisfying S0–S3 where sharing exceeds N. The ASN provides only an informal argument ("none of these place any bound"). Additionally, "Σ reachable" is undefined — reachability depends on the transition relation (operations), which is out of scope. The notation sets a standard the argument does not meet.

**Required**: Either (a) sketch the model family: for any N, construct a state with N+1 documents each mapping a V-position to the same I-address a ∈ dom(C), verify S0 (no transition involved — single state), S2 (each M(d) is a function), S3 (a ∈ dom(C)); or (b) restate S5 without `⊢` and "reachable" — e.g., "S0–S3 are consistent with any finite sharing multiplicity: the invariants place no constraint on |{(d, v) : M(d)(v) = a}|."

### Issue 2: S8 depends on I-address depth uniformity within runs, unstated and underived

**ASN-0036, Span decomposition**: "Similarly, I-addresses within a single document and subspace share a common prefix and differ only at the element ordinal (the last component of the element field)."

**Problem**: S8's correspondence runs use `a + k` (I-address ordinal increment). This requires all I-addresses in a run to share the same tumbler depth and prefix — otherwise TA7a's ordinal-only formulation does not apply. The ASN asserts this as fact but does not state it as a property or derive it. The derivation chain is: T9 (forward allocation) produces consecutive addresses via TA5(c) (sibling increment, k=0), which guarantees `#t' = #t` — same depth. Since runs arise from contiguous allocation sequences, all I-addresses in a run share depth. The ASN cites T9 and TA7a but drops the connecting step through TA5(c).

**Required**: State explicitly that I-addresses within a correspondence run share the same tumbler depth and prefix. Derive this from T9 + TA5(c): consecutive allocations use sibling increment, which preserves length.

### Issue 3: S8-depth has ambiguous status — property or design requirement

**ASN-0036, Span decomposition**: "S8-depth (Fixed-depth V-positions). Within a given subspace s of document d, all V-positions share the same tumbler depth."

**Problem**: S7a is explicitly classified: "This is a design requirement, not a convention." S8-depth is stated as a property and justified empirically ("Gregory's evidence is conclusive"). It cannot be derived from the abstract model without operation-level constraints (which are out of scope), so it should be classified as a design requirement — a structural constraint on V-space that any correct implementation must satisfy.

**Required**: Classify S8-depth as a design requirement, parallel to S7a. The empirical evidence supports the requirement but does not substitute for stating it as one.

### Issue 4: Open question 6 is answered by S8's own definition

**ASN-0036, Open Questions**: "Must the arrangement function M(d) preserve any relationship between V-space ordering and I-space ordering within a correspondence run, or can the mapping be arbitrarily permuted as long as each V-position maps to exactly one I-address?"

**Problem**: A correspondence run is *defined* by ordinal correspondence: `M(d)(v + k) = a + k` for `0 ≤ k < n`. Asking whether M(d) must preserve ordering within a run is asking whether a run must be a run. The answer is already in the ASN: any M(d) decomposes into runs (possibly all singletons), and runs are defined by the ordinal correspondence property. M(d) itself is unconstrained beyond S2 (functionality) — the run structure is a decomposition, not a constraint.

**Required**: Either resolve the question (state that any M(d) decomposes into runs by S8; the ordinal correspondence is definitional, not a constraint on M(d)) or rephrase to ask the intended question — perhaps whether non-trivial runs (length > 1) are guaranteed to exist, which depends on operation semantics.

### Issue 5: Properties table misclassifies S8

**ASN-0036, Properties Introduced**: "S8 | Span decomposition | introduced"

**Problem**: S8 is not an independent axiom. The ASN proves S8's existence from S8-fin (finite domain → finitely many singleton runs) and the functionality of M(d) (S2 — each V-position maps to exactly one I-address, giving a well-defined singleton run). The singleton construction is an explicit proof, not an introduction. The table correctly classifies S1 as "corollary of S0" and S9 as "theorem from S0" — S8 should receive analogous treatment.

**Required**: Reclassify S8 as "theorem from S8-fin, S2" (or similar) in the properties table.

## OUT_OF_SCOPE

### Topic 1: Document independence under editing
Whether modifying M(d₁) must leave M(d₂) unchanged for d₂ ≠ d₁. This is a frame condition for operations — requires operation definitions not present in this ASN.

**Why out of scope**: Operations and their frame conditions are explicitly excluded from this ASN's scope.

### Topic 2: Compactness guarantee for span decomposition
Whether operations maintain a run count bounded by the number of editing events (rather than document size). S8 proves existence of a decomposition but says nothing about compactness — the singleton decomposition has |dom(M(d))| runs. The architectural claim that run count is proportional to editing events requires operation semantics.

**Why out of scope**: Requires operation definitions to establish how editing events create and split runs.

### Topic 3: Atomicity of compound operations relative to S3
Whether S3 must hold at every intermediate state within a compound operation (e.g., an INSERT that extends dom(C) and dom(M(d)) in the same transition), or only at quiescent states. The ASN's temporal ordering claim ("content enters C first, then M(d) may reference it") touches on this but cannot resolve it without transaction semantics.

**Why out of scope**: Transaction semantics and intermediate states require operation-level specification.

VERDICT: REVISE
