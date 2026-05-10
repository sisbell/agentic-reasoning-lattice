# Review of ASN-0036

I reviewed every proof, every dependency citation, every edge case, and every invariant conjunct. The ASN is thorough and well-constructed — proofs are explicit, notation is consistent with ASN-0034, and boundary cases (empty documents, m=1, depth ≥ 3, cross-subspace partition) are handled correctly. The S8 partition proof, which is the most intricate argument, is airtight: the within-subspace case analysis on divergence point j (cases j < m and j = m) correctly excludes all distinct same-depth V-positions from each singleton interval, and the cross-subspace case correctly applies T5 + T10 at m ≥ 2 with a separate direct argument at m = 1.

One issue remains.

## REVISE

### Issue 1: S7c presented as part of S7's derivational basis but not used by S7

**ASN-0036, Structural attribution section**: "With S7a, S7b, and S7c established, we can state structural attribution:"

**Problem**: This sentence lists S7c alongside S7a and S7b as part of the basis for S7. But S7's proof never references S7c — `origin(a)` truncates the element field entirely, so the element-field depth constraint plays no role in well-definedness, identification, uniqueness, or permanence of attribution. The formal contract's preconditions correctly list S7a, S7b, T4, and T10a without S7c. The derivation summary ("S7 follows from S7a, S7b, T4, and GlobalUniqueness") also omits S7c. The properties table's Status column for S7 likewise excludes S7c. The narrative sentence is the sole source of the false dependency claim.

S7c IS load-bearing — but for S8-depth's analysis of subspace preservation under ordinal shifts (where δ ≥ 2 ensures E₁ is structural context outside the shifted ordinal), not for S7. The current placement between S7b and S7, combined with the "With... established" phrasing, misattributes S7c's role.

**Required**: Revise the connecting sentence to avoid presenting S7c as a dependency of S7. For example: "With S7a and S7b established, we can state structural attribution. (S7c, stated here for architectural completeness, is load-bearing for S8-depth's ordinal shift analysis below, not for S7 itself.)"

## OUT_OF_SCOPE

### Topic 1: Maximal decomposition uniqueness
**Why out of scope**: S8 proves existence via singleton construction. Whether a unique coarsest decomposition exists is a representation-layer question that the abstract state model need not resolve. Acknowledged in Open Questions.

### Topic 2: Operation-specific preservation of state invariants
**Why out of scope**: The ASN defines D-CTG, D-MIN, and S8-depth as design requirements on well-formed states. Verifying that INSERT, DELETE, COPY, and REARRANGE each preserve these constraints is the obligation of each operation's ASN. Explicitly deferred.

VERDICT: REVISE
