# Review of ASN-0042

## REVISE

### Issue 1: O17b labels delegation as registry-frame, contradicting O18 and the ASN's own worked example
**ASN-0042, State Axioms (O17b BaptismalRegistryCoupling)**: "for every `Σ → Σ'`, either `Σ'.B = Σ.B` (a registry-frame transition — delegation, allocation hint changes, and 'every other op' all reduce to this on the Σ.B component) or `Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}`..."
**Problem**: The parenthetical places *delegation* in the frame branch (`Σ'.B = Σ.B`, no registry change). But O18 (DelegationBaptizes) states `π' ∈ Π_{Σ'} ∖ Π_Σ ⟹ pfx(π') ∈ Σ'.B ∖ Σ.B` — a delegation transition *does* change `Σ.B`. DelegatorAllocatesPrefix asserts `allocated_by_{Σ'}(π_d, pfx(π'))`, and the Worked Example is explicit: "The delegated prefix `[1, 0, 2]` is deliberately *not* seeded — it is baptized at the delegation transition below, satisfying O18's freshness conjunct." So a delegation falls in the *second* branch, not the frame branch. The parenthetical also contradicts O17b's own opening sentence ("Every ownership transition that changes the baptismal registry does so by an ASN-0040 baptism"). This is an internal contradiction at the seam between O17b, O18, and the example.
**Required**: Remove "delegation" from the frame-branch parenthetical. Delegation must be classified as a `next(Σ.B, p, d)` baptism (the second branch), consistent with O18 and condition (v). The frame branch covers only `Π`-only changes (e.g., none — since `Π` changes always co-occur with baptism by O18) and genuine no-op-on-`B` operations.

### Issue 2: `delegated_Σ*` is defined as the closure of `R_Σ`, not of `delegated_Σ` — the notation asserts an identity that is never established
**ASN-0042, State Axioms (after Definition (delegated))**: "The reflexive-transitive closure `delegated_Σ*` is built from a *parent relation* `R_Σ` on `Π_Σ`... `R_Σ(π, π')` hold iff `π` is the most-specific covering principal... Then `delegated_Σ* = ∪_{m ≥ 0} R_Σ^m`."
**Problem**: `delegated_Σ` (no star) is the five-condition admission predicate (i)–(v), which includes `zeros ≤ 1` (iii) and next-reachability (v). `delegated_Σ*` is defined as the closure of the *structural* relation `R_Σ` (most-specific cover), which carries none of conditions (iii) or (v). The starred notation reads as `(delegated_Σ)*`, but it is the closure of a different relation. The two are provably related (a newcomer's actual delegator is its most-specific cover at every later state, by condition (iv) + O13), but that equality is asserted by naming, never proved. Downstream proofs (NestingByDelegation, O8) lean on `delegated_Σ*` as if it tracked real delegation events.
**Required**: Either (a) prove `delegated_Σ* = (delegated_Σ)*` explicitly, or (b) rename the `R_Σ`-closure (e.g., `covers_Σ*`) so it is not confused with the closure of the admission predicate. State which relation each downstream proof actually consumes.

### Issue 3: O17b carries use-site-inventory and implementation prose in an axiom slot
**ASN-0042, State Axioms (O17b)**: the frame-branch parenthetical "(a registry-frame transition — delegation, allocation hint changes, and 'every other op' all reduce to this on the Σ.B component)" plus "Gregory's implementation corroborates the coupling: every registry write in udanax-green funnels through a single allocation point — `findisatoinsertgr` for the ISA store, and `findpreviousisagr` for account slots — which issues each new tumbler..."
**Problem**: The parenthetical is a use-site inventory enumerating which operations "reduce to" the frame case — exactly the "definition's introduction enumerates downstream consumers" pattern flagged by the anti-bloat classifier — and it is also where the Issue-1 error lives. The Gregory paragraph is an implementation walk-through (function names, store internals) appended to an axiom whose content is the abstract coupling `Σ'.B = Σ.B ∨ Σ'.B = Σ.B ∪ {next(...)}`. A reader must work past the inventory and the code tour to reach the axiom.
**Required**: State the axiom as the two-branch disjunction. Drop the op-by-op inventory (it is neither needed nor correct). Reduce the implementation note to a one-line provenance pointer if retained.

## OUT_OF_SCOPE

None. The ASN correctly defers content identity, inclusion links, and ownership transfer to the content model and to its Open Questions, rather than smuggling them into ownership claims.

VERDICT: REVISE
