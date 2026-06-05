# Review of ASN-0103

I traced the allocation argument, the version-dominance proof, the freshness/uniqueness chain, the worked example, and the full invariant discharge. The ASN is rigorous on every point a Dijkstra-style review stresses.

Key checks performed:

- **Allocation correctness.** The length-restricted frontier `D_A = {e ∈ E : Document(e) ∧ parent(e)=A ∧ #e=#A+2}` is proven equal to `E ∩ S(A,2)` via the unique parse (T4b), with the load-bearing reverse inclusion shown explicitly. Both branches (`D_A=∅` → `inc(A,2)`; else `inc(max(D_A),0)`) land on `S(A,2)` with `Document(d)`, `zeros=2`, `parent=A`, `T4-valid`, `d∉E`.

- **Freshness robustness without contiguity.** The proof deliberately avoids assuming `D_A` is a contiguous prefix; `d > max(D_A)` plus `d ∈ S(A,2) = E∩S(A,2) ∪ (S(A,2)\E)` closes `d∉E` even with stream gaps. Verified that every `S(A,2)∩E` element satisfies the `D_A` predicate (zeros/parent/length all preserved by `inc(·,0)`), so the set equality is airtight.

- **Version dominance.** The hardest part. The on-chain case (`v_{#A+1}=0`) correctly freezes positions `#A+1,#A+2` across the version chain using TA5-SigValid (not just TA5(c)) — the distinction between "modifies `sig`" and "`sig=length`" is handled explicitly via T4-validity of every chain operand. The first-fork operand is pinned to a true root document `d_i=[A,0,i]∈D_A` via P1, yielding `i ≤ p−1 < p` and `d > v` by T1 case (i). The off-chain case (`v_{#A+1}≠0`) correctly claims only distinctness (divergence at `#A+1`), not dominance — consistent with CND.monotone's stated scope.

- **Edge/boundary cases.** First document (`D_A=∅`), account with versions (worked example excludes `v1` by length), never-populated documents and versions (in `E` via P1, hence dominated), deeply-nested accounts (argument generic in `#A`). The worked example `A=[1,0,1]` → `d=[1,0,1,0,2]` checks CND.alloc/empty/E/monotone, and crucially demonstrates the collision the length filter averts.

- **Uniqueness sourcing.** Same-chain via S0 (StreamOrdering injectivity, no single-authority premise); version/cross-account via B7 (NamespaceDisjointness). The ASN correctly declines GlobalUniqueness (undischarged T10a-conformance), B8's same-namespace branch (undischarged single-authority), and T10 (non-nesting premise fails since accounts can nest, e.g. `[N,0,5] ≺ [N,0,5,3]`). All justified.

- **Honest deferrals.** O5 (subdivision authority) and `ω_{Σ'}(d)=ω_Σ(A)` are explicitly deferred because the state `(C,L,E,M,R)` carries neither registry `B` nor `Π_Σ`; the missing `E↔B` coupling invariant is named precisely. CND.A-act is introduced as a transparent standing assumption (account-tier analogue of SubAllocatorBundle, which foundations state only at document tier). These are appropriate scoping, not gaps.

- **Atomicity & invariants.** Single `K.δ` firing → atomicity from the sequential-transition axiom; J0/J1★/J1'★ vacuous (no content/provenance). Every conjunct of ExtendedReachableStateInvariants + P3 is discharged: directly (M0, P1, S7d, ActivatedEmission), vacuously over `dom(M'(d))=∅`, or frame-inherited. ActivatedEmission for `d` correctly witnessed by `A_doc(A)` with activation from CND.A-act.

All cross-references are to foundation ASNs (0034, 0036, 0040, 0042, 0045, 0047, 0093). No reinvented notation. No proof-by-similarly, no proof-by-checkmark; multi-case arguments show each case.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the ASN appropriately confines forking, content allocation, link creation, and account provisioning to contrast or future-work references without defining claims for them.)

VERDICT: CONVERGED
