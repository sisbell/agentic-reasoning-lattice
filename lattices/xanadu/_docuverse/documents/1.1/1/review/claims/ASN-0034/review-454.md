# Regional Review — ASN-0034/OrdinalDisplacement (cycle 1)

*2026-04-23 17:31*

### Shift promised in section header but not defined
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: Section header "Ordinal displacement and shift" precedes OrdinalDisplacement, and the trailing prose remarks "we write δₙ" with an aside about "the tumbler being shifted". No shift claim is defined in the content shown.
**Issue**: The reader is told to expect a shift definition by the section header and by the trailing-notation aside ("typically m = #v for the tumbler being shifted"). Without a shift claim in scope, the notation remark is a forward reference that cannot be grounded from this ASN alone. This is either a structural gap (shift should be here) or a section-header overreach (header should match what is present).

### OrdinalDisplacement's `n ≠ 0` step cites only irreflexivity
**Class**: OBSERVE
**Foundation**: NAT-order
**ASN**: OrdinalDisplacement derivation: after establishing `0 < n`, the proof concludes "By NAT-order's irreflexivity, `n ≠ 0`."
**Issue**: Irreflexivity alone does not yield `n ≠ 0` from `0 < n`; the step requires substitution of equality (assume `n = 0`, rewrite `0 < n` to `0 < 0`, then apply irreflexivity). NAT-order's disjointness axiom `(A m, n ∈ ℕ : m < n : m ≠ n)` instantiated at `(0, n)` would discharge this directly in one step. The current citation hides the substitution the earlier NAT-zero block makes explicit.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 291s*
