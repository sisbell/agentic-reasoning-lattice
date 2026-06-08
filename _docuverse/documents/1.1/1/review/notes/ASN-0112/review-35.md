# Review of ASN-0112

I worked through the span construction, the V2 covering proof (both depth cases), the cross-subspace bounding-box argument, the wp derivations, and the worked examples (including the depth-divergent variant). The arithmetic is correct: I reproduced `1.1 for 0.11`, `1.1 for 1.2`, `2.1 for 0.1`, and the `[1,2,0]`/`r⋆=[2,2,0]` variant, and the D0/D1 case split on `#origin_d` vs `#reach_d` is sound and exhaustive. The technical core holds. The remaining issues are a rigor gap and one accretion pattern.

## REVISE

### Issue 1: Purity asserted in prose but never recorded as a claim
**ASN-0112, "The substrate we measure" / Claims table**: "We write the operation as a pure query, `RETRIEVEDOCVSPAN(d)`, that observes the state and returns a value, changing nothing."
**Problem**: This is an operation ASN, and the operation's defining guarantee — that it transitions no state component (`C, L, E, M, R` all unchanged) — appears only as prose. All seventeen V-claims describe the *returned value*; none records the frame. V15 (snapshot stability) is about the returned value persisting, and V16 (determinism) is purity *of the output function*, but neither asserts that the observed state `Σ` is left intact. For a specification whose entire premise is "boundary query, not a content read," the no-mutation property is exactly the kind of guarantee an alternative implementation must satisfy and should be stated formally.
**Required**: Add a frame/purity claim (e.g. `V-frame: Σ' = Σ`) so the no-mutation guarantee is a checkable property rather than an aside.

### Issue 2: V14 re-derives V6 inline rather than citing it
**ASN-0112, V14 (permanence)**: "The restriction to `O(d)` is essential: in the cross-subspace case V6 establishes `O(d) ⊊ ⟦σ_d⟧` strictly, so the span also covers inter-subspace and unoccupied positions (e.g. `[1,4]` in the worked example) on which `M(d)` is simply undefined; for those covered-but-unoccupied positions there is no image through `M(d)`, and the permanence claim makes no assertion about them."
**Problem**: The scoping (V14 speaks only of *occupied* positions) is legitimate, but the justification restates V6's conclusion and re-walks the worked example to establish a fact V6 already owns. A reader following the permanence argument must detour through a relocated copy of V6's content. This is the accretion pattern the anti-bloat classifier targets — downstream content carried into a neighbouring claim's slot.
**Required**: Replace the inline re-derivation with a bare pointer ("covered-but-unoccupied positions, which exist by V6, carry no `M(d)` image"), dropping the restatement and the example replay.

## OUT_OF_SCOPE

None. The forward-looking topics (count/extent relation, permanent-identity-vs-min-origin, historical-version faithfulness, correspondence-run composition, out-of-range arithmetic) are correctly confined to Open Questions, and no claim strays into content delivery, per-subspace reporting, or link discovery.

VERDICT: REVISE
