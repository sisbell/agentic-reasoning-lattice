# Review of ASN-0093

I checked the invariant discharges, the sub-allocator chain construction, the freshness lemmas, the cross-document disjointness argument, and the worked example against the foundation contracts.

## Key verifications performed

- **C1c/L1c chains are genuinely T10a-conforming.** Content chain `(d, b_C(d), a)` has `k = (2,1)`; link chain `(d, b_C(d), b_L(d), ℓ)` has `k = (2,0,1)`. Each step's TA5a side condition holds: `inc(d,2)` needs `zeros(d) ≤ 2` (M0 gives `=2`); `inc(b_C(d),1)`/`inc(b_L(d),1)` need `zeros ≤ 3` (anchors carry `zeros=3`); `inc(·,0)` unconditional. The at-most-once child-spawn constraint is respected — `A_C(d)=S(b_C(d),1)` is the unique `k'=1` child stream.
- **Anchor construction depends correctly on the pinned subspace values.** `b_C(d)=inc(d,2)=[d.0.1]=[d.0.s_C]` only because `s_C=1`; `b_L(d)=inc(b_C(d),0)=[d.0.2]=[d.0.s_L]` only because `s_L=s_C+1`. Both dependencies are explicitly discharged from SubspaceConventionAxiom.
- **Cross-document disjointness covers both the incomparable and nested (`d ≺ d'`) cases.** For `d₁ ≺ d₂`, the separator divergence at `k=#d₁+1` (where `p₁[k]=0`, `p₂[k]=d₂[k]≠0` because `zeros(d₂)=2` leaves no zero past `#d₁`) is correctly argued. Verified against Step 5 (`d=[1,0,2,0,5] ≺ d'=[1,0,2,0,5,3]`) and the multi-component `D(d')=[5,3]` origin recovery in Steps 6–7.
- **Subsequent-emit `zeros`/`#E`/`origin` preservation** rests on B5a (precondition `a_prev_{sig}>0` discharged via T4-validity + TA5-SigValid + T4's `t_{#t}≠0`) and TA5(b)'s single-position modification at `sig=#a_prev`. The element-field boundary is genuinely invariant under `inc(·,0)`.
- **Freshness lemmas are non-circular** within the simultaneous induction: FirstEmissionFreshness/SubsequentEmissionFreshness consume ChainMembershipForOrigin, StoreT4Validity, and L0 at the pre-state `Σ` (IH), then close via T10 (cross-document) and T7 (cross-subspace).
- **SD derivation** correctly discharges T7's preconditions on each side (`zeros=3` from C1/L1, T4-validity from StoreT4Validity) and the matrix avoids re-deriving it.

## Anti-bloat scan

The previously-flagged forward-reference accretion has been addressed: M2 carries no deferral roadmap (deferrals live only in Scope); the symmetric content↔link discharges reference rather than duplicate (e.g., L1/L1b cite the C1/C1b cells under explicit substitution, and the cases are genuinely identical, not merely "similar"); each derived ASN-0040 lemma (ChainDiscipline, ChainElementT4Validity, ChainEnumerationInjectivity, DisjointSubAllocatorChains, ChainPrefixExtension) is used downstream. The origin/home naming reconciliation in the State model advances understanding (it prevents confusion against the foundation's `home`), not skip-past meta-prose. No use-site inventories, axiom-rationale sub-paragraphs, or document-ordering justifications found.

## REVISE

None.

## OUT_OF_SCOPE

None beyond those the Scope section already enumerates (arrangement mutation, entity allocation, provenance, coupling, withdrawal).

VERDICT: CONVERGED
