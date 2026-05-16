# Review of ASN-0086

## REVISE

### Issue 1: R3 proof conflates K with its representative

**ASN-0086, R3 — TypedSliceMonotonicity proof**: "Let `(a, F, G) ∈ L_K^Σ`. Then `a ∈ dom(Σ.L)` with `Σ.L(a) = (F, G, K)`."

**Problem**: Membership in `L_K^Σ` requires `coverage(Σ.L(a).e₃) = coverage(K)`, not `Σ.L(a).e₃ = K` literally. The stored third endset is some `K''` with `coverage(K'') = coverage(K)`; it need not equal `K`. The proof's "`Σ.L(a) = (F, G, K)`" is therefore strictly wrong as stated. The conclusion is still correct (R2 preserves the literal value `K''`, and coverage-equivalence carries through), but the intermediate step is loose.

**Required**: Replace "`Σ.L(a) = (F, G, K)`" with "`Σ.L(a) = (F, G, K'')` for some `K''` with `coverage(K'') = coverage(K)`", and "`Σ'.L(a) = (F, G, K)`" with "`Σ'.L(a) = (F, G, K'')`" — then conclude membership in `L_K^{Σ'}` from coverage-equality of `K''` and `K`.

### Issue 2: R6a proof has the parallel imprecision

**ASN-0086, R6a — RetractionStability proof**: "By R2, `b ∈ dom(Σ'.L)` with `Σ'.L(b) = (F', G', R)` — the same value `G'` appears in both states."

**Problem**: Same coverage-class vs. literal-value issue as R3. The third endset stored at `b` is some `R''` with `coverage(R'') = coverage(R)`, not necessarily literal `R`. The argument's reliance on G's literal preservation is sound, but the third-slot wording should reflect coverage-equivalence.

**Required**: State the third entry as `R''` with `coverage(R'') = coverage(R)`. Note explicitly that the proof only needs `G'` (the to-set) preserved literally, which R2 gives.

### Issue 3: R0 Step 4 lumps L14a under "orthogonal" without citing the setup hypothesis

**ASN-0086, R0 proof, Step 4**: "Remaining L-invariants (L2, L4–L10, L13, L14, L14a): all are properties of `Σ.L`'s value structure or its targets that are either orthogonal to extension at a fresh key (L2, L4, L5, L6, L7, L8, L10, L13, L14a) or preservation lemmas under monotone extension (L14, L9 …)."

**Problem**: L14a says `Σ.M(d)(v) ∉ dom(Σ.L)` for every `v ∈ dom(Σ.M(d))`. After Emit, `dom(Σ'.L) = dom(Σ.L) ∪ {a}`, so preservation requires `a ∉ ran(Σ.M(d))` for all `d`. This is NOT orthogonal to fresh-key extension — it requires showing `a` is not an arrangement target. The argument that closes it (Step 2 fixes `subspace_I(a) = s_L`; setup hypothesis fixes content as `s_C`-resident; S3 makes arrangement targets content addresses; so `a ∉ ran(Σ.M)`) is sound but absent.

**Required**: Move L14a out of the "orthogonal" bucket. Either give it its own bullet citing the setup hypothesis and S3, or add a sentence acknowledging the L14a preservation chain is setup-hypothesis-conditional.

### Issue 4: Intro count mismatches the table

**ASN-0086, introduction**: "The answer is six structural properties, of which five (R0–R5) are derivable from ASN-0043 and one (R6, the active subset) is the substrate's own contribution"

**Problem**: The table lists R7 (NullifyIsEmit) as a LEMMA, with R6a/R6b/R6c as sub-claims of R6. The intro acknowledges only R0–R6 and silently omits R7. Readers tracking the count are left to discover R7 mid-document with no framing.

**Required**: Either add a clause in the intro acknowledging R7 as a derived fact about the operations (not one of the six foundational properties), or relabel the introductory framing to match the table's actual contents.

### Issue 5: Case A's subspace-sweep wording is loose

**ASN-0086, R0 Step 2 Case A**: "(ii) Sibling sweep `inc(·, 0)` from subspace 1 across to subspace `s_L` at element-field depth 1, applied `s_L − 1` times"

**Problem**: The phrasing "from subspace 1" reads as though it depends on `s_C = 1`. The actual claim is independent of where `s_C` sits — what is being swept is `A_d`'s enumeration from its base `d.0.1` (always the first sibling, regardless of which subspace identifier numbers content vs. links). For `s_L = 1`, "s_L − 1 = 0" applications means no sweep; for `s_L > 1`, the sweep advances through intermediate subspace identifiers regardless of whether `s_C` sits among them.

**Required**: Rephrase as "from `A_d`'s base `d.0.1` to `d.0.s_L`, applied `s_L − 1` times" — phrased in terms of `A_d`'s enumeration index, not subspace-1-as-anchor.

## OUT_OF_SCOPE

### Topic 1: Interaction between L_K (coverage-equality) and L10 (hierarchical containment)

**Why out of scope**: The note's typed relation is built on L8 — coverage-equality at the type slot. L10 establishes a separate, hierarchical relation among types (subtypes via prefix-containment). Under the current definitions, `[K_parent] ≠ [K_child]` when `coverage(K_child) ⊊ coverage(K_parent)`, so `L_{K_parent}` does NOT include child-typed tuples — a substantial departure from how relational queries usually treat type hierarchies. The ASN inherits L8 cleanly and defers hierarchical queries to higher layers; a follow-up ASN should specify how `L_K` and L10 compose (e.g., union-over-subtypes, or a separate hierarchical-typed-relation primitive).

### Topic 2: Concurrency and atomicity beyond what Open Questions covers

**Why out of scope**: The author's open questions touch on atomicity and ordering, but a follow-up ASN should formally define the consistency model — particularly what guarantees hold when multiple agents call `Emit_K` and `Observe_K` concurrently, and whether `nullified(Σ)` transitions are atomic with respect to `A_K` reads.

VERDICT: REVISE
