# Review of ASN-0103

I worked through the core construction (the document frontier `D_A`, the freshness/distinctness argument, the K.δ decomposition, and the invariant discharge) and checked each against the foundation contracts and the worked example.

## REVISE

(none)

The load-bearing parts hold up under scrutiny:

- **`D_A = E ∩ S(A, 2)` is proven both directions.** The load-bearing inclusion `D_A ⊆ S(A,2)` correctly uses T4b's parse: `Document(e) ∧ parent(e) = A` gives `e = A.0.D(e)`, and the length filter `#e = #A + 2` forces `#D(e) = 1`, landing `e = [A,0,D(e)₁]` on the canonical stream form. The length restriction is genuinely necessary, not decorative — the version-masquerade collision is real (a version `v` satisfies `Document(v) ∧ parent(v) = A`) and the worked example demonstrates the concrete B8 violation that would result from the unrestricted frontier.
- **Both branches are covered.** `D_A = ∅` (first emission `inc(A,2)`) and `D_A ≠ ∅` (sibling `inc(max(D_A),0)`), with document-level, validity, and freshness each verified per branch.
- **Freshness is airtight.** `d ∈ S(A,2) \ D_A = S(A,2) \ E ⟹ d ∉ E` quantifies over all of `E`, and distinctness from version chains and other accounts is discharged by B7 namespace disjointness — present *and future*, which is the right standard.
- **The K.δ decomposition checks against the foundation.** Case (ii) k=2 (`zeros(A)=1 ≤ 1`, `parent = A ∈ E`) and k=0 (`d_prev` non-node, `parent(d)=A`) preconditions are satisfied; the empty-arrangement post-state matches K.δ's Document sub-case; coupling J0/J1★/J1'★ hold vacuously.
- **Depth bar met.** Concrete worked example present and checked against CND.alloc/empty/E/monotone; derived guarantees (CND.own via prefix transitivity, CND.no-sharing via S4) carry explicit derivations rather than assertions.

The invariant discharge is honest — directly-verified, vacuous-on-empty-arrangement, and frame-inherited conjuncts are correctly partitioned, and the effective-owner reading is deferred to Open Questions rather than overclaimed. No non-foundation ASN is referenced by number; forking/content/link operations appear only as out-of-scope contrast, not as defined claims.

The anti-bloat scan found the recurring permanence/baptism themes and the proof-roadmap labels ("easy direction," "load-bearing direction") to be within normal exposition — each instance advances the argument or supplies a required concrete check. The sub-allocator-activation note documents a true K.δ effect (SubAllocatorBundle) rather than meta-prose.

## OUT_OF_SCOPE

(none)

VERDICT: CONVERGED
