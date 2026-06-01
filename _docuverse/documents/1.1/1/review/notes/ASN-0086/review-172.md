# Review of ASN-0086

## REVISE

### Issue 1: Non-circularity justification embedded in R0
**ASN-0086, R0 proof, subsequent-emission "on-chain admissibility" bullet**: "L-ContiguousPrefix (ContiguousPrefix, proved below — its proof rests on ASN-0093's ChainMembershipForOrigin and the conformance clauses (b)–(c), not on R0, so the forward reference is non-circular) gives that the homed-set..."

**Problem**: This is the exact forward-reference-accretion pattern the anti-bloat pass targets: prose that defends a forward pointer's non-circularity ("not on R0, so the forward reference is non-circular") rather than advancing the argument. A reader following the on-chain-admissibility step must skip past a dependency-ordering defense to reach the actual content.

**Required**: Cite L-ContiguousPrefix plainly. If the ordering genuinely matters, place L-ContiguousPrefix before R0 so the parenthetical defense is unnecessary; otherwise delete it.

### Issue 2: Scope-justifying forward pointer in R0's L1b discharge
**ASN-0086, R0 proof, L-invariant-preservation, L1b discharge**: "(Over R0's substrate-conforming domain L-ContiguousPrefix-Cor1, DepthTwoLinkAddresses below, further pins `#E(ℓ_prev) = 2`, hence `#E(a) = 2`; only `≥ 2` is needed to discharge L1b.)"

**Problem**: The parenthetical introduces a strictly stronger downstream result, derives a consequence from it, then states that consequence is not needed here ("only `≥ 2` is needed"). It advances nothing for the L1b discharge — it is a forward pointer to a result the very sentence disclaims as superfluous.

**Required**: Delete the parenthetical. The L1b conjunct needs only `#E(a) ≥ 2`, already established two sentences earlier.

### Issue 3: Premise-inventory preamble in R0a
**ASN-0086, R0a proof opening**: "The argument decomposes into two cases on `home(a)` vs. `home(a')`, and the two cases rest on *different* premise sets. Case 1 (cross-home) uses only L1 + L1a — a zero-counting argument over the NUDE-prefix `home` projection, with no appeal to chain machinery. Case 2 (same-home) uses L-ContiguousPrefix + (UL) + T3 — the contiguous-chain structure that the substrate's allocator discipline supplies."

**Problem**: This previews which premises each case consumes before either case states or uses them — a use-site inventory that duplicates the case bodies (each case re-cites L1/L1a, or L-ContiguousPrefix/(UL)/T3 at point of use). The reader reads the premise list twice.

**Required**: Delete the preamble; the two case headers already carry their premises at the point they are used.

### Issue 4: CoverageEqualityDecidable partition omits exterior cells
**ASN-0086, Lemma CoverageEqualityDecidable**: "...each interval is a union of consecutive *cells* of the partition `{c₁}, (c₁, c₂), {c₂}, …, {c_m}` (points and open gaps)... comparing the two indicator vectors decides `coverage(e) = coverage(e')`."

**Problem**: The enumerated cells span only `[c₁, c_m]`. The regions `(−∞, c₁)` and `(c_m, ∞)` are not cells of the stated partition, so the "indicator vector over the finitely many cells" does not, as written, cover all of `T`. The conclusion is still correct (both coverages are subsets of `[c₁, c_m)`, hence agree trivially on the exterior), but the decision procedure's completeness rests on that unstated fact.

**Required**: One sentence noting both coverages lie within `[c₁, c_m)`, so equality on the listed cells suffices — closing the partition argument.

## OUT_OF_SCOPE

### Topic 1: Higher-arity links (`|Σ.L(a)| > 3`)
**Why out of scope**: The note explicitly restricts `L_K`/`A_K`/`Nullify`-effects to standard-triple links and defers the higher-arity construction (acknowledged in the Open Questions). The binary-projection vs. n-ary-relation choice is genuinely new territory, not an error here.

### Topic 2: Concurrency/atomicity model for Emit vs. Observe
**Why out of scope**: Observe-consistency and Emit atomicity under concurrency are raised in Open Questions and depend on a transition-ordering model this note does not (and need not) supply.

VERDICT: REVISE
