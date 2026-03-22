# Review of ASN-0073

## REVISE

### Issue 1: Exactness of N+1 count asserted without distinctness argument
**ASN-0073, ValidInsertionPosition**: "In the non-empty case, there are exactly N + 1 valid insertion positions"
**Problem**: "Exactly N+1" requires the N+1 enumerated positions to be pairwise distinct. The definition enumerates them via `min(V_S(d))` (j=0) and `shift(min(V_S(d)), j)` for 1 ≤ j ≤ N, but never shows these yield distinct tumblers. The distinctness is straightforward — TS4 separates j=0 from j≥1, and TS5 separates any two j values with both ≥ 1 — but the argument is absent. Alternatively, computing the explicit form `shift([S, 1, …, 1], j) = [S, 1, …, 1+j]` via OrdinalShift makes distinctness obvious from distinct last components (T3), but this computation is also missing.
**Required**: Derive distinctness, either by citing TS4+TS5 or by computing the explicit form from OrdinalShift and appealing to T3.

### Issue 2: Lower bound m ≥ 2 in the empty case stated without derivation
**ASN-0073, ValidInsertionPosition, empty subspace**: "v = [S, 1, ..., 1] of depth m ≥ 2"
**Problem**: The constraint m ≥ 2 is asserted but never justified. At m = 1, `v = [S]` and `shift([S], 1) = [S] ⊕ δ(1, 1) = [S] ⊕ [1]`. The action point of `[1]` is k = 1, so TumblerAdd gives `r₁ = S + 1`, producing `[S+1]` — a position in subspace S+1, not subspace S. This violates the requirement that shift produce positions within the same subspace, which is what makes m = 1 inadmissible. Without this argument, the reader has no reason to accept m ≥ 2 over m ≥ 1.
**Required**: Derive m ≥ 2 from the requirement that OrdinalShift preserve the subspace identifier (action point m must satisfy m ≥ 2 so that TumblerAdd copies component 1 unchanged).

### Issue 3: Structural properties of valid positions claimed without verification
**ASN-0073, ValidInsertionPosition**: "In both cases, #v equals the common V-position depth in subspace S (S8-depth)" and "In both cases, S = v₁ is the subspace identifier"
**Problem**: Two structural properties are stated as observations without derivation:
- **Depth preservation**: For the non-empty case, `#shift(min, j) = #min = m` follows from OrdinalShift's result-length identity (`#shift(v, n) = #v`), but this is not cited. For the empty case, `#v = m` is by construction — trivial, but should be noted as such.
- **Subspace identity**: `shift(min, j)₁ = min₁ = S` holds because δ(j, m) has action point m ≥ 2, so TumblerAdd copies component 1 unchanged. This is the same argument that motivates m ≥ 2 (Issue 2) but needs to be stated as a property of all valid positions in the non-empty case.
- **S8a consistency**: For text-subspace positions (S ≥ 1), every valid position `[S, 1, …, 1+j]` satisfies `zeros(v) = 0` and `v > 0` (all components ≥ 1). This is visible from the explicit form but unstated.

**Required**: Brief verification of each property from the relevant foundation definitions (OrdinalShift for depth, TumblerAdd for subspace, explicit form for S8a).

## OUT_OF_SCOPE

### Topic 1: Displacement mechanics at occupied positions
**Why out of scope**: The predicate intentionally identifies structurally feasible positions without specifying what happens to existing mappings when an operation targets an occupied position. The ASN correctly defers this to operation-level ASNs and lists it as an open question. This is new territory (operation semantics), not an error in the definition.

### Topic 2: Exhaustiveness — positions outside the predicate are invalid
**Why out of scope**: The predicate defines validity; it does not claim or prove that no other positions could work. A lemma showing that inserting at `shift(min, N+k)` for k ≥ 2 necessarily violates D-CTG (creating a gap) would strengthen the definition but is a separate result, not a defect in this ASN.

VERDICT: REVISE
