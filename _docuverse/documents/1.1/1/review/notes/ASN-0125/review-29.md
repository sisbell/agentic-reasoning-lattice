# Review of ASN-0125

This is an exceptionally thorough note. I checked the core proofs and they hold: EL0's mutation-exclusion is LP13 correctly read as a wp (false at Σ₀ for every program); EL1's intent-invisibility is a sound determinism argument; EL2's four-way closure is a genuine exhaustiveness case-split; EL6/EL7's contracts are correctly split into unconditional vs. edit-disciplined halves, with the `nullified` frame discharged via R0a and ASN-0086's wp Case 2; the constructions in EL9(2), EL10, EL13, EL14 are faithful to ASN-0047's K.μ⁻/K.μ⁺_L semantics and reachable within the editing layer; the worked example traces correctly (I re-derived the five-entry standoff and the registry-churn re-binding). Boundary cases — empty store (EL-DM base), last/only link (EL9(2) parenthetical), self-supersession (irreflexivity), length-2 cycles (EL14c standoff, `current = ∅`), fork (EL12) — are all handled. No improper cross-ASN references (every citation is a foundation ASN); implementation evidence is present and appropriate.

One prose finding remains, of exactly the kind this note's anti-bloat classifier targets.

## REVISE

### Issue 1: Df-SUCC's totality paragraph is defensive justification that re-states EL4

**ASN-0125, Df-SUCC (Successor relations)**: "Restricting the comprehension to `Ŝ^Σ` keeps the relations total at *every* reachable state, not only disciplined ones: the accessors are undefined on a non-conforming `[K_sup]`-class tuple ... a full-vocabulary `K.λ` (one not routed through the editing-layer discipline) can emit one. (Df-LAY's *bare* `K.λ` cannot: it is confined to original-link creation ... at editing-layer-reachable states every claim conforms and `Ŝ^Σ = S^Σ`, EL4.)"

**Problem**: The definition of `succ_h`/`succ_o` is complete in its first two lines; this third paragraph is justification a reader skips to reach the definition. It carries two anti-bloat patterns:

1. *Duplication.* The closing clause "at editing-layer-reachable states every claim conforms and `Ŝ^Σ = S^Σ`" restates verbatim what EL4 already establishes one block earlier ("at an edit-disciplined state every claim conforms, so `Ŝ^Σ = S^Σ`"). The same fact is asserted twice in different words.

2. *Defensive scoping.* The bulk of the paragraph argues robustness against a case the editing layer (this ASN's subject) excludes — a rogue full-vocabulary `K.λ` emitting a malformed `[K_sup]` tuple — together with a parenthetical re-deriving that Df-LAY's bare `K.λ` cannot do it (which Df-LAY itself already fixed by confinement to original-link creation). The Ŝ-vs-S robustness thread recurs as a briefer caveat in EL11(b) ("filtered by the decidable schema-conformance predicate (a no-op at disciplined states...)"); the heaviest instance is here.

To note: the `Ŝ` apparatus itself is *correct and worth keeping* — `assert_sup`'s precondition genuinely admits non-disciplined input, so totality over all reachable states is a real property, not a fabrication. The finding is on the exposition, not the construction.

**Required**: Condense to a clause attached to the definition — e.g., "over `Ŝ^Σ` (the schema-conforming claims, EL4) so the accessors are total at every reachable state; `Ŝ^Σ = S^Σ` at editing-layer states by EL-DM." Drop the rogue-`K.λ` walkthrough and the bare-`K.λ` parenthetical (both are already settled by Df-LAY), and do not re-state EL4's coincidence point.

## OUT_OF_SCOPE

### Topic 1: Well-foundedness of currency over claims-that-supersede-claims
**Why out of scope**: EL8(d) correctly asserts only the *mechanism* (editlink applies to a claim address, `DC` permitting), and `current(·)` is total regardless (finite closure over `dom(Σ.L)`). Whether currency resolution must *stratify* meta-claims is a semantic design question, properly deferred to the Open Questions rather than resolved here.

META: not applicable — the ASN specifies an operation, the supersession relation, and their invariants abstractly (an alternative implementation would equally need allocation-plus-assertion under immutability); it has not drifted into implementation mechanics.

VERDICT: REVISE
