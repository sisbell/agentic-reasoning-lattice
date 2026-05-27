# Review of ASN-0091

## REVISE

### Issue 1: Cross-document transclusion derivation skips two foundation steps

**ASN-0091, "Cross-Document Transclusion Preserved"**: "By RE-other applied to `d' = origin(a)`, the source arrangement is unchanged. By RE-C, the address `a` remains in `dom(Σ'.C)` with its original value."

**Problem**: Two implicit foundation moves are not cited. (i) Applying RE-other at `d' = origin(a)` requires `origin(a) ∈ dom(Σ.M)`, which comes from C2 (ASN-0093) for content or L1a (ASN-0093) for link addresses. (ii) Invoking RE-C requires `a ∈ dom(Σ.C)` to begin with. For a foreign address `a ∈ ran(Σ.M(d))` with `origin(a) ≠ d`, this holds because CL-OWN (ASN-0047) forces every link-subspace V-position in d to map to a link with `origin = d`, so the V-position witnessing `a ∈ ran(Σ.M(d))` must be content-subspace, after which S3★ gives `a ∈ dom(Σ.C)`. CL-OWN, S3★, and C2 are load-bearing here but uncited.

**Required**: Insert the chain "by CL-OWN, foreign addresses (origin ≠ d) in ran(M(d)) arise only at content-subspace V-positions, so `a ∈ dom(Σ.C)` by S3★; by C2, origin(a) ∈ dom(Σ.M)" before applying RE-other and RE-C. The provenance entry for RE-trans in the claims table should also cite CL-OWN, S3★, and C2.

### Issue 2: Sloppy parenthetical justification in worked-example P4★ check

**ASN-0091, Worked Example (3-cut), Admissibility verification**: "`Contains_C(Σ') = ... = Contains_C(Σ)` as a set of pairs (the bijection π restricted to `V_{s_C}(d)` carries each I-address's singleton pre-image set onto itself)"

**Problem**: "Onto itself" is misleading. For I-address `a₁`, the pre-state pre-image is `{[1,1]}` and the post-state pre-image is `{[1,3]}` — different singletons. The bijection carries the pre-state singleton onto the *post-state* singleton, not "onto itself." The conclusion (Contains_C invariance) is correct, but the stated reason is wrong. The correct reason is that π restricted to `V_{s_C}(d)` preserves which I-addresses appear in the range (RE-ran restricted to the content subspace), so the set of (a, d) pairs is preserved. The same phrasing appears in the 4-cut example.

**Required**: Rephrase the parenthetical in both worked examples to "π restricted to `V_{s_C}(d)` preserves the content-subspace range, so the set of (a, d) pairs Contains_C is preserved."

## OUT_OF_SCOPE

None — the ASN explicitly lists out-of-scope topics (INSERT, DELETE, COPY, version creation, BEBE) and does not stray into them. The Open Questions section captures REARRANGE-adjacent territory (link-subspace rearrangement semantics, fragmentation upper bounds, bijection realizability via cut sequences) as future work rather than claiming results.

VERDICT: REVISE
