# Review of ASN-0043

## REVISE

### Issue 1: `home` definition restates its applicability-to-links inline, duplicating L1a and forward-referencing L1c

**ASN-0043, Definition — home**: "*This is the same field-extraction formula ASN-0036 uses to define `origin` on content addresses, applied here to link addresses. Every link address meets the precondition: `zeros(a) = 3` by L1, and T4-validity from L1c's chain (LinkAllocatorConformance, below) via T10a.4.*"

**Problem**: `home` is a general definition over any T4-valid element-level tumbler; its well-definedness condition is already stated one sentence earlier ("well-defined precisely because `a` is T4-valid and element-level"). The trailing sentence then re-establishes that *link addresses* satisfy that condition — but this is exactly what L1a's opening already does: "By the home definition above, `home(a)` is well-defined on every `a ∈ dom(Σ.L)`, and we state the invariant in terms of it directly." The two say the same thing, and the definition slot additionally carries a forward reference to L1c ("below"). A definition should advance its own meaning, not pre-justify its use at a downstream invariant that already carries that justification.

**Required**: Drop the final sentence of the `home` definition. The applicability of `home` to link addresses belongs at L1a (where it already lives), not pre-staged in the definition with a forward pointer.

### Issue 2: L0b's body re-derives L1c's T4-validity postcondition rather than citing it

**ASN-0043, L0b — LinkAddressValidity**: "*This is the T4-validity postcondition of L1c's chain: each `a ∈ dom(Σ.L)` is the terminus `tₙ` of a T10a-conforming chain from a T4-valid seed, and T10a.4 (T4PreservationUnderDiscipline, ASN-0034) propagates T4-validity along every step.*"

**Problem**: L1c's body already contains this derivation verbatim in its "*Postcondition: T4-validity of `a`*" paragraph ("The chain begins at the T4-valid seed `s` and proceeds entirely by T10a steps, so by induction on chain length, `tₙ = a` is T4-valid"). L0b reproduces the same chain-from-seed + T10a.4-propagation argument a second time. L0b is worth keeping as a *named* invariant so the L0a discharge has something to cite, but its body should reference L1c's established postcondition, not re-run the induction.

**Required**: Reduce L0b's body to a one-line citation of L1c's T4-validity postcondition; delete the duplicated derivation.

## OUT_OF_SCOPE

None. The Open Questions correctly defer transclusion consistency, compound-link well-formedness, and the global content-subspace constant to future ASNs; none are smuggled in as claims here.

The proofs themselves check out under spot verification: the L11a single-tree argument correctly establishes GlobalUniqueness's precondition in both the distinct-home and shared-home cases; PrefixSpanCoverage's mutual-inclusion argument is sound; and the worked example's Step-6 coverage equality (`[g,g') ∪ [g',h) = [g,h)` against `(g, δ(2,8))`) is arithmetically correct. The two findings above are accretion, not correctness.

VERDICT: REVISE
