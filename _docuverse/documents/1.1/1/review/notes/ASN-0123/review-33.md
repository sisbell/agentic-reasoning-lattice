# Review of ASN-0123

I checked the load-bearing proofs against the foundations and find them sound: PS's registry-coverage derivation (the position-1 induction through K.δ's increment cases is correct), SA's zero-count antichain argument, VN-B1's four-case induction (Node/k=2/k=1/k=0 all close, freshness forces the frontier), V9's severance theorem and the structural O5(ii) maximality discharge, V-WF's ValidComposite★ clause-by-clause, and V10 with both worked instances (the `a₁ ⋠ a₂` / SA collapse to `{a₁}` and the cross-owner divergence-at-position-4 arithmetic both verify). The G2 necessity argument (range preservation forced via SA) and the VD/`derives` restricted biconditional are correct. No correctness defect, no skipped boundary case (n=0, version-of-version, multi-origin source, links-only source all handled or honestly deferred), and no non-foundation cross-ASN reference in the body.

The residue is accreted meta-prose, which is what this review pass targets.

## REVISE

### Issue 1: V-WF closes with a forward-reference use-site inventory
**ASN-0123, V-WF (final sentence before ∎)**: "This is the standing P-bdy hands to the next operation — in particular to a subsequent fork from v (V6), whose own P4★ use (V9w) is licensed in turn."
**Problem**: This sentence sits inside V-WF's proof, after the post-state's invariants and boundary properties are already established, and does nothing but enumerate downstream consumers (V6's subsequent fork, V9w's P4★ use). It advances neither the well-formedness argument nor the boundary conclusion — it advertises the conclusion's later utility. This is the "definition/proof enumerates downstream consumers" pattern; a reader following V-WF has to step over it.
**Required**: Delete it. V-WF's job ends at "satisfies ... P4★ ∧ P4a ∧ P7a (ExtendedReachableStateInvariants, boundary clause)." If V6/V9w need to assert that a fork's output is again a valid composite boundary, that assertion belongs at their use site, not pre-advertised here.

### Issue 2: V6's conformance disquisition over-states and overlaps deviation 1
**ASN-0123, V6**: "This requirement is mandatory for conformance, not an idealization a sufficiently large finite bound approximates... A fixed cap C is nonconformant as a design choice, whatever its size... A larger C only postpones when that contradiction is met, never whether; outgrowing the bound is not conformance." — restated concretely in **deviation 1**: "raising NPLACES (as the 11 → 16 history did) postpones the fatal overflow but does not confer conformance, since the renumber-or-refuse dilemma recurs at the new bound."
**Problem**: The load-bearing content of V6 is three lines (depth-1 consumes no separator → `B6(wⱼ,1)` unconditional → `T0(b)` gives unbounded length). The "finite cap can never conform, whatever its size / enlarging only postpones / mandatory not idealization / falls on the address format not storage" point is then made several times over in V6 and once more in deviation 1. The renumber-or-refuse dilemma is genuine and worth stating once; the surrounding restatements are essay. Deviation 1 already references "the renumber-or-refuse dilemma" by name, so the argument has a natural single home.
**Required**: Argue the dilemma once (V6, as the abstract reason unboundedness is mandatory), trim V6's "whatever its size / only postpones / not an idealization / falls on the address format" restatements to a single sentence, and let deviation 1 keep only the concrete NPLACES verdict and remedy (variable-length tumblers) while citing the dilemma rather than re-spelling "enlarging only postpones."

## OUT_OF_SCOPE

No drift items. The note scopes editing, comparison, document-creation, link, delivery, and replication operations out cleanly, touches them only through frame conditions (V11(a), V2b), and routes genuinely future obligations to the eight Open Questions (concurrent-fork serialization, derivation-direction recovery, link-subspace carry, location-fixed windowing, withdrawal semantics). The cross-owner determinism that initially looks under-specified relative to the owned `nextv` is in fact correctly deferred: the owned case reproves VN-B1 because it needs the contiguous-prefix form for the `nextv` formula and V5's rank semantics, whereas the cross-owner case needs only freshness, which FrontierEquivalence/ChildSpawnFreshness supply directly — the asymmetry is justified, not a gap.

VERDICT: REVISE
