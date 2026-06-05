# Review of ASN-0103

I worked through the three effects, the document/version separation that underpins the allocation, the cross-allocator monotonicity argument, and the full invariant discharge. The ASN is rigorous; I was unable to find a defect that requires revision.

The load-bearing arguments all hold up under scrutiny:

- **The `D_A = E ∩ S(A, 2)` identity** is proved in both directions, and the hard direction (`D_A ⊆ S(A,2)`) correctly uses the T4b parse plus the length constraint to force the canonical form `[A, 0, j]`. The length filter `#e = #A + 2` is exactly what excludes versions, and the worked example demonstrates the collision (`inc(v1,0) = [1,0,1,0,1,2]` re-baptising a future version of `d1`) that would otherwise occur — a genuine, non-trivial justification for the filter.

- **The version-dominance argument** (CND.monotone) is the right strengthening. It correctly declines to use T9 across allocators and instead argues by direct T1 lexicographic comparison at position `#A+2`. The freezing of positions `1..#A+2` across all `k=1`/`k=0` steps (TA5(b)/(c)) is sound, and the routing of the root document into `D_A` via entity permanence (P1) — so that `i ≤ max(D_A) index = p−1 < p` — closes the inequality. I verified that K.δ forbids `k=2` descent off a `zeros=2` document, so the first length-increasing step in any version lineage is necessarily a `k=1` fork off a length-`#A+2` document, which the argument relies on.

- **Cross-account freshness** is correctly routed through GlobalUniqueness/B8 rather than T10, with an explicit and correct note that `Account(A') ∧ A' ≠ A` does not discharge T10's non-nesting premise.

- **The ω deferral** (CND.own) is handled with unusual care: structural ownership `pfx(π) ≼ A ≼ d` is derived over ASN-0047's state, while the effective-owner equality `ω_{Σ'}(d) = ω_Σ(A)` is correctly identified as underivable (no registry component, no E↔B coupling) and deferred, rather than asserted.

- **Invariant discharge** is complete: I cross-checked every conjunct of `ExtendedReachableStateInvariants` plus P3 against the direct/vacuous/frame-inherited partition, and each is covered. The vacuity premise `dom(M'(d)) = ∅` and the frame `C' = C ∧ L' = L ∧ R' = R` legitimately discharge the empty-arrangement and content/link/provenance families.

- **Atomicity** follows correctly from the single-K.δ decomposition, and the coupling constraints J0/J1★/J1'★ hold vacuously since no content is allocated.

All foundation references (ASN-0034, 0036, 0040, 0042, 0045, 0047, 0093) are within the permitted foundation set. The CREATENEWVERSION contrast is named only for distinction and is properly out of scope. A concrete worked example is present and checks the key claims. The ASN defines an operation on state with abstract invariants — squarely specification territory, no drift.

## OUT_OF_SCOPE

### Topic 1: Registry/entity coupling for the effective-owner reading
The ASN's final open question — what E↔B coupling makes the document-tier K.δ coincide with a `Bop(A, 2)` baptism so that `ω_{Σ'}(d) = ω_Σ(A)` becomes derivable — is genuinely new territory requiring a registry-carrying state model, not a defect here. Correctly deferred.

VERDICT: CONVERGED
