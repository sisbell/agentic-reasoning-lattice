# Review of ASN-0047

## REVISE

### Issue 1: K.μ⁻'s precondition uses circular post-state formulation

**ASN-0047, "Elementary transitions" K.μ⁻ definition**: "The contracted arrangement `M'(d)` must satisfy the per-state arrangement invariants S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, and D-MIN★."

**Problem**: This precondition is evaluated against the post-state `M'(d)`, encoding "valid contraction" as "operation only fires when result is valid." While this partial-domain idiom is common, it leaves the operation under-specified: the caller cannot determine *a priori* which contractions are valid without computing the post-state. The downstream "K.μ⁻ admissible contraction shape" derivation supplies the constructive form (per-subspace suffix removal), but the precondition itself remains opaque.

**Required**: Move the constructive shape characterization (per-subspace suffix removal under D-CTG★ + D-MIN★ + D-SEQ★) into the precondition directly, or reframe the precondition as a domain restriction that the implementer can check operationally.

### Issue 2: Verification matrix cells are non-uniform in elaboration depth

**ASN-0047, ExtendedReachableStateInvariants verification matrix**: Some cells provide detailed load-bearing arguments ("T10a GlobalUniqueness on parent allocator..."), while others use terse phrases ("restriction of decomposition", "inherits via decomposition", "frame") without specifying the route.

**Problem**: For the K.μ~ column especially, "inherits via K.μ⁻ + K.μ⁺ decomposition" appears repeatedly without distinguishing which sub-case is consumed. Readers must cross-reference the decomposition section and the body-text convention to determine the actual discharge.

**Required**: Either elaborate the terse cells with explicit per-step discharge (one sentence each), or move the dispatching convention (full-clearance form universally) into a matrix legend at the head of the table.

### Issue 3: Sprawl — 30,000+ word ASN risks unreviewable state

**ASN-0047 overall**: The ASN combines new entity/provenance components, redefines elementary transitions, amends inherited operations, derives strengthened invariants, proves the reachable-state invariants via matrix + prose, includes four worked examples, and lists 11 open questions.

**Problem**: The length exceeds what one cycle can hold in working memory. The "Sprawl blinds review" memory flags a related risk: coupling gaps in large pre-compress states went undetected for ~6 cycles. Beyond editorial cost, length increases the chance that subsequent revisions introduce internal inconsistencies between distant sections (e.g., K.μ⁻'s admissible contraction shape derivation appears in two paragraphs ~5,000 words apart, each restating the non-circularity argument).

**Required**: Consider splitting — the four-component analysis (state model, K.α/K.δ/K.μ⁺/K.μ⁻/K.μ~/K.ρ, P0-P8, J0-J4) is largely independent of the extended-state material (link store, K.λ/K.μ⁺_L, S3★, CL-OWN/CL-UNIQ, J1★/J1'★). The fork example and link-allocation example could move to supplementary material once the elementary verification is established.

### Issue 4: K.μ~ admissibility clause (i) explicitly retained as "redundant for clarity"

**ASN-0047, "Decomposition of K.μ~"**: "Clause (i) is retained in the admissibility statement only for *expository* clarity — marking each step's S8a obligation explicitly rather than leaving it as a derived consequence — and does not extend the operational obligations beyond clauses (ii) and (iii)."

**Problem**: An admissibility clause stated as a precondition that the body then certifies as provably-redundant is contract-bloat. The clarity gain is debatable; the cost is that downstream verifiers may discharge clause (i) as an independent obligation rather than recognizing the redundancy.

**Required**: Either remove clause (i) and let S8a fall out of the matrix-level discharge, or retain it but flag it inline at the admissibility statement (not buried two paragraphs below).

## OUT_OF_SCOPE

None — the ASN appropriately defers operation-level concerns (INSERT, DELETE, COPY, MAKELINK, CREATENEWVERSION) and concurrency to future ASNs via the Scope section and Open Questions.

VERDICT: REVISE
