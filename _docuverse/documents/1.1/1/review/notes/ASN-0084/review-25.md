# Review of ASN-0084

## REVISE

### Issue 1: Broken parenthetical justification in canonical decomposition step (c) forward extension

**ASN-0084, "Canonical decomposition" step (c), forward extension paragraph**: "Partition disjointness — distinct partition runs have disjoint V-extents (S8(a) gives uniqueness of containing run for any position in dom(M(d))) — forces b = c, contradicting v_c ≠ v_b (since v_c precedes v_b + n_b strictly while v_b does not)."

**Problem**: The parenthetical justification is incorrect. Since n_b ≥ 1, ord(v_b) < ord(v_b) + n_b = ord(v_b + n_b), so v_b *does* precede v_b + n_b strictly under T1. The parenthetical does not establish v_c ≠ v_b.

**Required**: Replace the parenthetical with the actual contradiction route: if b = c, then v_c = v_b, so v_b + n_b = v_c + k_c = v_b + k_c forces n_b = k_c; but k_c < n_c = n_b under the b = c identification gives n_b < n_b, contradiction. (Equivalently: b = c would put v_b + n_b ∈ V(b), but offsets of b are {0, ..., n_b − 1}, impossible.) The backward extension paragraph handles the analogous step correctly — match that pattern.

### Issue 2: Forward/backward extension dichotomy asserted without proof of exhaustiveness

**ASN-0084, canonical decomposition step (c), non-maximality dispatch**: "By the definition of maximality, b admits a strict extension as a valid correspondence run — either *forward* ... or *backward* .... At least one of these holds whenever b is non-maximal; we dispatch on the two directions and derive a contradiction in each."

**Problem**: The claim that any extension of b must be forward or backward is asserted without proof. Non-maximality (some partition run c is V-adjacent and I-adjacent to b) admits two configurations: c starts at v_b + n_b, or c ends at v_b. The argument requires this exhaustive dichotomy, which follows from the Merge condition `v₂ = v₁ + n₁`, but the ASN does not derive it.

**Required**: One sentence establishing that V-adjacency between two contiguous runs forces one of two configurations: either b's V-end meets c's V-start (forward), or c's V-end meets b's V-start (backward). No third option exists because runs are themselves contiguous.

### Issue 3: Associativity citation does not strictly cover zero-offset cases

**ASN-0084, "State and Vocabulary" preamble**: "Associativity `(c₀ + j) + k = c₀ + (j + k)` follows from TS3 (ShiftComposition, ASN-0034): `shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)`."

**Problem**: TS3's preconditions require `n₁ ≥ 1 ∧ n₂ ≥ 1`. The general claim of associativity over `j, k ∈ ℕ` (including 0) is not strictly licensed by TS3; the identity convention `c₀ + 0 = c₀` is required for the boundary cases. The same overstated citation appears at numerous proof sites — R-PIV's "By associativity, c₀ + (w_β + j) = (c₀ + w_β) + j" (j can be 0), R-SWP's analogous step, R-COMM's "by associativity" (k = 0 case), and the Split lemma's TS3 invocation (where the proof correctly handles k = 0 via identity, but cites TS3 alone).

**Required**: Lift this to a labeled "Extended Associativity" claim covering all four cases (both ≥ 1, both = 0, mixed), with TS3 for the both-≥-1 case and identity convention for the others, then cite it uniformly. Alternatively, qualify each "by associativity" invocation with the relevant case split.

### Issue 4: Subspace preservation derivation does not cover offset zero

**ASN-0084, "Consequences of R-PRE — Subspace confinement"**: "The shifted positions `c₀ + j`, `c₁ + j`, `c₂ + j` named in R-P1, R-P2, R-S1, R-S2, R-S3 retain subspace S by OrdShiftHom (b) of ASN-0036 (`subspace(shift(v, n)) = subspace(v)`), with the cuts' subspace fixed by CS3."

**Problem**: OrdShiftHom (b) is stated for `n ≥ 1`. When `j = 0` (the first position of every region's image), `c_i + 0 = c_i` by identity convention; subspace preservation then follows from CS3 directly, not from OrdShiftHom (b). The j = 0 case is load-bearing — it's the start of each region — yet the cited lemma doesn't cover it.

**Required**: Split the derivation: for j = 0, c_i + 0 = c_i and subspace(c_i) = S by CS3 directly; for j ≥ 1, OrdShiftHom (b) applies.

### Issue 5: R-RI stated as standalone lemma but not consumed downstream

**ASN-0084, R-RI lemma**: A separate lemma proves `ran(M'(d)) ⊆ dom(C')` via three-step chain: ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C').

**Problem**: R-RI is derived but no subsequent lemma cites it. The invariant-preservation paragraph after the rearrangement definition references R-RI as the proof of S3 maintenance, but the relationship is parenthetical. The standalone-lemma framing suggests R-RI is a load-bearing intermediate result, but it functions only as a verification obligation.

**Required**: Either (a) inline R-RI into the invariant-preservation paragraph as a one-sentence derivation (it is one), and remove the standalone status; or (b) keep R-RI as a lemma but explicitly note in the invariant paragraph that S3 maintenance *is* R-RI. The current arrangement makes R-RI's role unclear.

### Issue 6: Definition of `c₀ + 0` for the identity convention introduces a typing question

**ASN-0084, "State and Vocabulary"**: "By convention, `c₀ + 0 = c₀` (identity)."

**Problem**: OrdinalShift (ASN-0034) requires `n ≥ 1`. The identity convention extends shift to `n = 0`, but its interaction with downstream OrdinalShift consumers (TS3, TS2, TS5, OrdShiftHom) is not stated systematically. Specifically: do TS2 (ShiftInjectivity) and TS5 (ShiftAmountMonotonicity) extend to `n = 0`? The canonical decomposition's a₁ = a₂ derivation case-splits on k₁ = 0 vs k₁ ≥ 1 precisely because TS2 doesn't apply at 0.

**Required**: State explicitly which downstream OrdinalShift consumers extend to the identity convention and which don't. The proofs in this ASN already case-split appropriately, but the convention's domain of validity should be stated once, in the preamble.

## OUT_OF_SCOPE

### Topic 1: Link endset preservation under rearrangement
**Why out of scope**: Links attach to I-addresses, and C' = C (R-FRAME-P (c), R-FRAME-S (c)) preserves all I-address content; endset semantics under rearrangement is a corollary belonging in a future link-preservation ASN.

### Topic 2: Cross-subspace transposition
**Why out of scope**: Explicitly excluded by the ASN's text-subspace-only scope. The link subspace's tombstone-and-gap structure requires separate treatment.

### Topic 3: Composition of cut-point rearrangements
**Why out of scope**: Whether two cut-point rearrangements compose to a cut-point rearrangement, and whether sequences can reach arrangements unreachable by single operations, is listed in the open questions and belongs to a future ASN.

### Topic 4: k-cut rearrangements for k > 4
**Why out of scope**: A general n-cut theory is a natural extension noted in the open questions but lies beyond the 3-cut/4-cut scope here.

### Topic 5: Maximal-partition uniqueness as a standalone result
**Why out of scope**: The canonical decomposition machinery (Split, Merge, maximal-partition uniqueness) is presented as scaffolding for R-BLK, but R-BLK itself only uses Split and Merge — the full uniqueness theorem is not consumed. This material could be lifted into its own ASN as a foundational property of correspondence runs, leaving ASN-0084 to focus on rearrangement-specific results.

VERDICT: REVISE
