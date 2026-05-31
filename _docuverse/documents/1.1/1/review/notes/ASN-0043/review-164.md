# Review of ASN-0043

I checked the L1c/CPP chain argument, FSP/FSE, the L8/L9/L13 lemmas, and the six-step worked example. The mathematics is sound: the chain construction, the two-invocation CPP argument, the coverage-equality computation in Step 6, and the discrimination argument in Step 4 all hold. My findings are confined to accreted meta-prose, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: L1c postcondition proof carries defensive lemma-attribution bookkeeping
**ASN-0043, "Proof of L1c postconditions"**: "We discharge them in turn — the first from T10a.4 alone (CPP plays no role), the second as the genuine application of CPP." Followed by the headers "*T4-validity of `a` (T10a.4 alone, independent of CPP).*" and "*`s = home(a)` (the genuine CPP application, two invocations).*"

**Problem**: Within a few lines the proof asserts five times which lemma does or does not carry which part — "the first from T10a.4 alone," "(CPP plays no role)," "(T10a.4 alone, independent of CPP)," "the genuine application of CPP," "(the genuine CPP application, two invocations)." This is bookkeeping, not argument. The body already makes the attribution self-evident: the first sub-proof opens "By T10a.4…" and the second opens "Apply CPP…". The reader must parse past the meta-commentary to reach the reasoning. This is the reviser-drift pattern (defensive annotation accreted around a recently split proof) the anti-bloat classifier flags.

**Required**: Reduce the parentheticals. Headers "*T4-validity of `a`.*" and "*`s = home(a)`.*" plus the existing body sentences carry the lemma attribution without the repeated "CPP plays no role / genuine CPP application" framing.

### Issue 2: L0b closes with a backward-reference annotation that adds no content
**ASN-0043, L0b — LinkAddressValidity**: "The well-definedness of the T4b projections — and hence of `home` and `subspace_I` — that it underwrites was already noted in L1c's proof."

**Problem**: L0b's substantive claim is the universal lift in the preceding sentence ("This lifts the per-address T4-validity of L1c's chain terminus to a universal invariant"). The trailing "was already noted in L1c's proof" is cross-reference bookkeeping deferring to a location the reader already passed; it neither advances L0b's statement nor records a new consequence.

**Required**: Drop the clause, or state the projection well-definedness as L0b's own consequence rather than annotating where it was previously mentioned.

## OUT_OF_SCOPE

### Topic 1: Unconditional content-subspace residence
L14 (DualPrimitive disjointness) and L14a (NonTranscludability) hold only for `s_C`-resident states, and no invariant in this ASN forces `dom(Σ.C)` into a single subspace. Lifting the disjointness guarantee from the `s_C`-slice to all of `dom(Σ.C)` requires a content-side invariant fixing a global content-subspace constant — which belongs in the content ASN (ASN-0036 family), not here. The ASN already names this in its Open Questions and scopes every affected invariant explicitly, so it is an acknowledged boundary, not an error.

VERDICT: REVISE
