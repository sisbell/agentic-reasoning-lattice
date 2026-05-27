# Review of ASN-0069

## REVISE

### Issue 1: ASN-0098 references not justified by the foundation list

**ASN-0069, V6a, worked example, and Dependency Audit**: The ASN cites LP4, LP13, and LP16 from ASN-0098 in V6a's three-part derivation and in the worked example ("by LP16 (TransclusionDiscoverability, ASN-0098) applied at Σ'..."). The Dependency Audit declares "four foundation ASNs" including ASN-0098.

**Problem**: The verified foundation list provided to reviewers contains ASN-0034, ASN-0036, ASN-0040, and ASN-0047. ASN-0098 is not in that list. Per the review standards, references to non-foundation ASNs by number must be flagged as REVISE items — the ASN must either be self-contained or rely only on foundation claims. The recent commit `9d39952f2 revise(asn-69/V6a)` suggests the citations were intentionally added; this only sharpens the question of whether ASN-0098 has been promoted to foundation status.

**Required**: Either (a) confirm ASN-0098's foundation status and update the foundation list provided to reviewers, or (b) inline the LP4/LP13/LP16 statements (or the specific facts each call site needs) into V6a's body so that ASN-0069 is self-contained against the four-foundation set.

### Issue 2: V10(b) cites V5a beyond its scope

**ASN-0069, V10(b)**: "Their inherited V→I mappings live in separate arrangements `M¹(d_new¹)` and `M²(d_new²)`. By V5a, modifications to one do not propagate to the other."

**Problem**: V5a's statement is specifically about source–fork independence: "if the modification targets `d_src`" / "if the modification targets `d_new`". Sibling forks `d_new¹` and `d_new²` are *both* forks of `d_src` — neither plays the source role with respect to the other. V5a as written does not apply to the pair `(d_new¹, d_new²)`. The actual reason sibling forks are independent is the same per-target frame discipline that underwrites V5a's *derivation*, but the cited *claim* doesn't cover this pair.

**Required**: Either generalize V5a to "any pair of distinct documents" (since its derivation already establishes this) or, in V10(b), cite the per-target frame discipline of K.μ⁻ / K.μ⁺ / K.μ~ / K.μ⁺_L directly instead of V5a.

### Issue 3: V5a's statement is ambiguous for sequences with mixed targets

**ASN-0069, V5a**: "For any subsequent state transition `Σ' →* Σ''` after the fork: `(M''(d_src) ≠ M'(d_src) ⟹ M''(d_new) = M'(d_new))` *if the modification targets `d_src`*"

**Problem**: V5a is quantified over arbitrary multi-step sequences `Σ' →* Σ''`. A sequence may contain steps targeting `d_src` and steps targeting `d_new` (e.g., one K.μ⁺ on each). Both biconditionals' antecedents then become true while the conclusions are false. The italicized side conditions "if the modification targets X" are doing real work — restricting the implication to single-target sequences — but they are written as informal asides, not as formal preconditions on the implication. The derivation argues per-single-transition; the statement is per-sequence; the gap is not bridged.

**Required**: Restate V5a either (a) per-elementary-transition with a separate corollary about mixed sequences, or (b) per-sequence with an explicit precondition like "if every transition in `Σ' →* Σ''` targets `d_src` (or is `M`-frame to both `d_src` and `d_new`)". The current phrasing leaves the reader to reconstruct the intent.

## OUT_OF_SCOPE

None. The ASN's Open Questions section appropriately defers concurrency semantics, version-DAG presentation, snapshot vs. living-fork distinctions, transclusion sources, and discoverability bounds. The body itself does not stray into INSERT/DELETE/COPY/REARRANGE mechanics, link semantics beyond discoverability, or BEBE.

VERDICT: REVISE
