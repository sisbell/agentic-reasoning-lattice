# Review of ASN-0103

I checked the three effects, the load-bearing `D_A = E ∩ S(A,2)` argument, the freshness/distinctness reasoning, the worked example, and the full invariant discharge against `ExtendedReachableStateInvariants` + P3.

## REVISE

(none)

The core technical content holds up under scrutiny:

- **The length filter is justified, not asserted.** `D_A = E ∩ S(A,2)` is proved in both directions; the load-bearing inclusion `D_A ⊆ S(A,2)` is discharged via T4b parse (`Document(e) ∧ parent(e)=A ∧ #e=#A+2 ⟹ e = [A,0,D(e)₁]`), and the `#D(e)=1` step is forced correctly. The version-exclusion discussion and the worked-example collision (`inc(v1,0)` re-baptising the next version, violating B8) are concrete and load-bearing — they are the justification for the filter, not drift.
- **Freshness is clean over all of E with no case split.** The set-algebra step `d ∈ S(A,2)\D_A = S(A,2)\E ⟹ d ∉ E` is valid in both branches (vacuous `d ∉ D_A` when `D_A=∅`; `d > max(D_A)` otherwise). Future distinctness is covered: same-chain by S0 injectivity, version chains and cross-account by B7 (both pairs B6-valid, including versions-of-`d`).
- **K.δ grounding is correct.** Case (ii) k=2 off `A` (`zeros(A)=1≤1`) and k=0 off `d_prev` (`d_prev ∈ E ∧ ¬Node`) satisfy the elementary preconditions; `parent(d)=A` follows from K.δ-ID.parent-2/parent-0; `M'(d)=∅` from the Document sub-case frame; single-transition atomicity from the sequential axiom.
- **Invariant discharge is exhaustive.** Each conjunct is verified directly, vacuous on `dom(M'(d))=∅`, or frame-inherited. ActivatedEmission is discharged via `A_doc(A)` under the standing assumption CND.A-act — a legitimate scoping of out-of-scope account provisioning.
- **Ownership is derived, not asserted.** `pfx(π) ≼ A ≼ d` via prefix transitivity, with effective ownership (registry-dependent) correctly deferred to Open Questions.

## OUT_OF_SCOPE

The Open Questions (effective-owner/registry coupling, concurrency serialisation, partial-failure recovery, removal-vs-permanence, write-readiness) are correctly scoped out and need no claims here. The CREATENEWVERSION contrast in "What Distinguishes Creation From Forking" is used only as an empty-vs-inherited contrast with no forking claims introduced, so it does not stray into the forking ASN's territory.

On the anti-bloat classifier: the recent tightening pass appears effective. The version-exclusion prose and worked example are concrete explanatory content (explicitly exempted from the meta-prose rule), not defensive accretion. The minor overlap between the Effects sections and the Invariants Maintained section is the unavoidable cost of conjunct-by-conjunct correctness verification, and the two deferrals to Open Questions for effective ownership are too slight to warrant a finding.

VERDICT: CONVERGED
