# Review of ASN-0027

Based on Alloy modeling-1

## SKIP

### Confirmatory counterexamples (expected by the ASN)

**A0 — ReachabilityNonPermanent.** The check asserts the *negation* of the lemma (reachability is permanent) and expects a counterexample to confirm the existential claim. SAT confirms exactly what the ASN states: transitions exist where reachable content becomes unreachable. The `run Witness` SAT confirms non-vacuity. Not a spec issue — the counterexample *is* the proof.

**A10 — PublicationObligation.** The ASN explicitly declares A10 as "contractual, not architectural" and states "the architecture permits DELETE on any V-space position without checking publication status." The Alloy model's own comment anticipates the counterexample. SAT confirms the architecture does not enforce publication permanence, which is the ASN's design intent.

### Modeling artifacts

**A2.length — DeleteLength.** Integer overflow in Alloy's bounded arithmetic. With `5 Int` (5-bit, range [-16, 15]), `plus[start, k]` can overflow to a negative value when the true sum exceeds 15. The precondition `plus[start, k] =< d.n` is then trivially satisfied (negative <= non-negative), allowing the Delete predicate to fire with nonsensical `k` values. This causes `minus[d.n, k]` to go negative, while `dPost.n` is constrained to [0, 5] by the Doc fact, producing the spurious assertion violation. Guard with `plus[start, k] > start` (overflow check) or widen the Int scope.

**A5 — VersionIdentitySharing.** The main assertion (VersionIdentitySharing) passed — UNSAT. The auxiliary A5_newPreservesWF assertion failed due to an incomplete frame in the `A5_new` predicate: `all d2: s.docs | sPost.ver[d2] = s.ver[d2]` constrains only docs in `s.docs`, leaving Doc atoms not in `s.docs ∪ {dNew}` with unconstrained version mappings in the post-state. Alloy assigns arbitrary versions to these "ghost" atoms, violating well-formedness. In the mathematical model, no such extra documents exist — this is a bounded-scope artifact. Fix: add `all d2: Doc - s.docs - dNew | no sPost.ver[d2]`.

### Passed properties (28)

All 28 remaining properties — Σ.reachable, A1, A2.pre/left/compact/frame-I/frame-doc, A3.pre/length/perm/range/frame-I/frame-doc, A4.pre/identity/length/left/right/frame-I/frame-doc, A5.new/frame-doc/frame-I, A6, A7, A7.corollary, A8, A9 — passed bounded check (UNSAT, no counterexamples within scope). Non-vacuity runs confirmed where present.

VERDICT: CONVERGED
