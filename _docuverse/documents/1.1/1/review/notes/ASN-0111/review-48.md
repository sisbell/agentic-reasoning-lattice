# Review of ASN-0111

I checked every numbered claim (RL0–RL6, SOV), re-derived the wp computation, verified the structural screen's necessity/insufficiency arguments against the foundation invariants, walked the RL4 branched-history construction step by step against K.δ/K.λ preconditions, re-proved the three permanence families (depth via LP-Sub/F, lineage via the L1a→P8→NodeLineage chain, user-field via the account induction over K.δ cases), checked the exhaustiveness construction for the residual class against FrontierEquivalence/ChildSpawnFreshness/ChainMembershipForOrigin, and recomputed every tumbler in the worked read (addresses, `⊕`/`δ` arithmetic, interval decompositions, LP-Fin candidate counts). All of that is sound. One certification gap remains in the worked example's reachability route.

## REVISE

### Issue 1: Worked-read reachability route — the K.μ⁻ composites' validity is never certified

**ASN-0111, "A worked read"**: "A subsequent K.μ⁻ on each document with content-subspace retention `n'_{s_C} = 0` then empties the content V-positions while `dom(C)` retains all three entries (P0); the provenance entries persist through the contraction (P2), so P4★ and P7a hold at this and every subsequent composite boundary."

**Problem**: The reachability of the stipulated configuration is a proof obligation the ASN itself takes on explicitly ("it is nevertheless reachable, and we exhibit the route rather than assume it"), and every other segment of the route carries its validity certificate: the K.δ/K.λ segments via SOV, the allocation composites via an explicit J0/J1★/J1'★ discharge. The contraction segment is the one segment whose ValidComposite★ clause-2 obligation (J0, J1★, J1'★ evaluated initial-to-final) is left unaddressed. SOV cannot be silently relied on here — a K.μ⁻ modifies a content-subspace arrangement range, so SOV's hypothesis fails — and the facts the sentence does cite (P0, P2, P4★, P7a) are store-permanence and boundary properties, not the coupling discharge. The discharge itself is immediate: J0 is vacuous (`dom(C') ∖ dom(C) = ∅`), J1★ is vacuous (a contraction produces no range-new content-subspace I-address), J1'★ is vacuous (`R' = R`); the foundation states exactly this as J2 (ContractionIsolation, ASN-0047). Without that clause, the certified-route chain has one uncertified hop, and the worked example's "reachable" claim rests on an unstated premise.

**Required**: One clause certifying the contraction composites' validity — either cite J2 (ContractionIsolation, ASN-0047), or note the vacuity of all three couplings directly from K.μ⁻'s frame (`C' = C`, `R' = R`, arrangement range only shrinks). Nothing else in the route needs touching.

## OUT_OF_SCOPE

### Topic 1: Reader-facing guarantees deferred by the Open Questions
**Why out of scope**: The three Open Questions — what a reader may conclude about continued validity from a read alone, how FOLLOWLINK keeps a legitimately-empty endset distinguishable from an unwitnessed one, and how identical-valued links stay distinguishable by address — are traversal- and identity-layer obligations belonging to FOLLOWLINK and related future ASNs. The ASN correctly states them as questions rather than claiming them; no coverage is missing here.

For the record, the items I examined hardest and found sound, so they are not re-raised: RL0's insufficiency witness at `Σ₀` and the left-to-right evaluability of the screen; RL4's non-vacuity construction (both branches enable the same K.λ at the same frontier address, and the steps compose under SOV); RL5's account-field induction (k = 2 from a node yields user field `[1]`, k = 0 preserves `#U`, no other path mints accounts); the exhaustiveness of the permanence split (every residual-class member is allocatable from any reachable state via baptism, spawn-or-skip, frontier advances, and K.λ steps); and the worked example's arithmetic, including the LP-Fin candidate counts (two F-members under the first span, one under the second) and the allocation composites' J0/J1★/J1'★ discharge.

VERDICT: REVISE
