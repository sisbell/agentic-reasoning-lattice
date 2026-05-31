# Review of ASN-0043

I checked each invariant's proof, the FSP/FSE conformance lemmas, the L1c chain derivation (CPP, the two-invocation argument), the L9 ghost-type construction (Case A explicit chain and Case B via FSE), and the six-step worked example for non-vacuous coverage. I respected the three declined findings (PrefixSpanCoverage locality, L1b grounding, FSP/L1c producibility) and did not re-surface them.

## REVISE

*(none)*

The substantive checks pass:

- **L1c postconditions** are genuinely derived, not asserted. T4-validity is inducted along the chain via T10a.4; `s = home(a)` is pinned by two CPP invocations, and the prose explaining why the second invocation is needed (CPP's `p ≤ #t₀` forbids reaching position `#s+1` in one pass) is load-bearing reasoning, not bloat.
- **Edge cases are covered.** Empty from/to endsets with a non-empty type slot (L9 witness `(∅, ∅, {(g,…)})`); arity 3 vs. arity `N` (Step 3, arity 4); singleton vs. multi-span endsets (L5 trivial at singletons, exercised at Step 5); single-span vs. two-span type endsets with equal coverage (Step 6); first-link-in-document vs. subsequent (L9 Case A vs. Case B); ghost types outside both stores.
- **FSP discharges every state-local invariant** in its enumerated set; L0b is correctly excluded since it is the universal lift of L1c (which FSP does preserve), so no gap. The Step-6 coverage equality `[g,g') ∪ [g',h) = [g,h)` is verified by adjacency at `g'`, and the L8 discrimination at Step 4 by disjointness of `{t : g ≼ t}` and `{t : g' ≼ t}` at the differing terminal component.
- **Cross-references** are exclusively to foundation ASNs (0034, 0036); no non-foundation references appear.
- **Anti-bloat scan:** the Gregory/Nelson confirmations are concrete evidence (explicitly not meta-prose), the proof sub-labels are structure markers, and FSP is reused by both L9 and L11b (DRY), not deferred-to-but-unstated. I did not find the flagged accretion patterns surviving in this revision.

## OUT_OF_SCOPE

### Topic 1: s_C-residence as a preserved invariant
The disjointness in L14/L14a holds only over the `s_C`-resident slice, carried as a hypothesis rather than established as an invariant. This is correctly deferred to Open Question #1 (a content-side global-subspace constant) and is not an error in this ASN.

VERDICT: CONVERGED
