# Review of ASN-0134

This is a strong, careful note — the §4 operation-level non-confluence analysis (the de-duplication seam and the cross-home `Nullify`/emit race), the V2 strict-implication chain, and the worked allocation scenario in §7 are exactly the kind of depth the standard demands. Three issues remain, one in a load-bearing definition.

## REVISE

### Issue 1: A6's "single-state" package includes cross-state stability invariants P2/R2

**ASN-0134, A6 (CanonicalState)**: "This package is genuinely single-state — a reader handed `Σ_k` alone can in principle check every conjunct, each being a predicate of `Σ_k`'s own components." Listed members include "ASN-0126's `P6`/`P1`/`P2`, and ASN-0128's `R1`/`R2`."

**Problem**: A6's entire architecture rests on one distinction — per-state predicates (checkable at `Σ_k` alone) versus relational invariants with "no single-state form" — and it uses that distinction to *exclude* C0/L12, on the grounds that their "content is inherently relational ... a property of a *step* ... the only single-state shadow is the trivial 'the store is a function'." But P2 (ShapeStability: "shape(K) takes the same value at every →_sh*-reachable state") and R2 (IdemStability: "idem(K) takes the same value at every reachable state") have *exactly* that disqualifying form: each quantifies over the set of reachable states and asserts a value is constant across them. A reader handed `Σ_k` alone provably cannot check "shape(K) is the same at every reachable state" — that requires comparing states. So P2/R2 are not "predicates of `Σ_k`'s own components," and by the very criterion that ejects C0/L12 they do not belong in the single-state package. The criterion is applied inconsistently: C0/L12 (cross-step, trivial single-state shadow) are excluded; P2/R2 (cross-state, equally trivial shadow) are included. P1/R1 are borderline — "Σ.registry = Σ_init.registry" is single-state only if `Σ_init.registry` is treated as a fixed external constant, which the phrase "predicate of Σ_k's own components" elides.

**Required**: State the registry-related single-state member as the genuine per-state predicate the argument needs — "`Σ_k`'s record equals the canonical initial record R₀" (the per-state instance of P1/R1, with R₀ named as a fixed substrate constant) — and present P2/R2 as the *cross-state corollaries* of R₀-fixity holding at all states, not as conjuncts a lone snapshot exhibits. Otherwise drop the "each being a predicate of Σ_k's own components" characterization for these members.

### Issue 2: H1/W1 disjointness proof omits the cross-document, cross-subspace case

**ASN-0134, H1 (CrossHomeIndependence) proof**: "The two chains are disjoint with prefix-incomparable anchors (`DisjointSubAllocatorChains` for `d = d'`, `S ≠ S'`; `CrossDocumentDisjointness` for `d ≠ d'`)." (Same citation pattern in W1.)

**Problem**: "distinct `(d,S) ≠ (d',S')`" splits into three sub-cases: (a) `d=d', S≠S'`; (b) `d≠d', S=S'`; (c) `d≠d', S≠S'`. The cited lemmas cover only (a) and (b). DisjointSubAllocatorChains is one document, two subspaces (`A_C(d)` vs `A_L(d)`) — case (a). CrossDocumentDisjointness is one subspace, two documents — its anchors are `b_·(d_i)` for a single fixed `·` — case (b). Neither, as stated, compares `b_S(d)` with `b_{S'}(d')` when both differ — case (c). And (c) is not exotic: it is the most common cross-home pair (one writer allocates content in `d`, another a link in `d'`), and H1 must commute exactly such pairs for G1's adjacent-transposition argument.

**Required**: Add the one-line argument for case (c): for `d≠d'`, anchors `b_S(d)=[d.0.S…]` and `b_{S'}(d')=[d'.0.S'…]` diverge already at the document component, so they are prefix-incomparable regardless of `S, S'`, and the chains are disjoint. Document-level divergence subsumes all `d≠d'` cases within the 0093 stack; the citation as written does not.

### Issue 3: M1(b)(ii) overstates de-duplication, contradicting I2

**ASN-0134, M1 (SafetyUnderMIC) proof, (b)(ii)**: "Under `idem(K) = ⊤`, a semantic repeat — a second `Emit_K` with coverage-equal `(F, G)` — is a zero-step hit returning the incumbent address: it adjoins nothing to `A_K`, so it cannot duplicate."

**Problem**: As written this is false in a case the note relies on elsewhere. By I2 (AuditSliceNotConsulted / RestorationByReemission), de-dup consults `A_K`, not `L_K`: if the incumbent has been nullified between the two emits, it sits in `L_K` but not `A_K`, so the second `Emit_K` is a *miss* that deposits a fresh (resurrected) tuple — not a zero-step hit. So "a semantic repeat is a zero-step hit" holds only when the incumbent is currently active. The intended conclusion (no duplicate *in `A_K`*) does survive, but via I1a (ActiveIdemUniqueness: at most one active tuple per coverage class) — which M1(b) never invokes — not via the stated "it's a hit" mechanism. §4 correctly carries the "provided the deposit lands active" hedge; M1(b) drops it.

**Required**: Either restrict the claim to active incumbents ("a repeat of a *currently active* coverage-equal tuple is a zero-step hit"), or rest the no-duplicate conclusion on I1a (`A_K` holds ≤ 1 tuple per coverage class) rather than on the unconditional hit, noting that a repeat of a nullified incumbent is deliberate resurrection (I2), not an `A_K` duplicate.

## OUT_OF_SCOPE

(none — the note properly defers cross-server composition, batch read-atomicity, durability promotion, and the concrete exclusion primitives to its Open Questions rather than asserting claims about them.)

VERDICT: REVISE
