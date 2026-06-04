# Review of ASN-0076

## REVISE

### Issue 1: E11 collapse relies on an unsupported "precisely the union" assertion to establish #E = 2

**ASN-0076, E11 "The collapse"**: "No element of dom(Σ.L) properly extends ℓ_new either, and this we derive rather than assert. Every link address lies in F (LP-Sub, ASN-0098) and is an emission of some A_L sub-allocator with element-field depth exactly #E = 2 (SubAllocatorBundle, ASN-0047); dom(Σ.L) is precisely the union of these A_L-emissions, so every link ∈ dom(Σ.L) carries zeros = 3..."

**Problem**: The load-bearing fact for excluding proper extensions of `ℓ_new` is "#E(t) = 2 for every `t ∈ dom(Σ.L)`." The paragraph announces "this we derive rather than assert," then immediately rests it on the assertion "dom(Σ.L) is precisely the union of these A_L-emissions." That equality is *not derived* — establishing it would require an induction over the transition system showing every K.λ output is an `A_L` sibling emission, which is never given. The hypothetical `t ≻ ℓ_new` with `t ∈ dom(Σ.L)` and `#E(t) = 3` is L1c-conforming and not excluded by any cited invariant; only the asserted union-equality rules it out. So the step labeled "derived" is in fact the assertion it disclaims.

**Required**: Drop the `A_L`-emission detour and derive `#E(t) = 2` directly from the facts already cited: LP-Sub (ASN-0098) gives `dom(Σ.L) ⊆ F`, and F's structural form `[d, 0, s, k]` (ASN-0098) fixes `#E = 2` for every element of F by inspection. That chain is explicit and needs no claim about which sub-allocator produced `t`. Remove the self-referential "this we derive rather than assert" phrasing along with the unsupported union claim.

## OUT_OF_SCOPE

### Topic 1: Editing a supersession link (supersession chains)
**Why out of scope**: EDITLINK applied to an `ℓ_old` that is itself a supersession link is admitted by the generality of the construction but its chain/cycle semantics are explicitly deferred to the Open Questions; this is future territory, not a defect here.

### Topic 2: Authorization of who may publish a supersession against `ℓ_old`
**Why out of scope**: E6's application-layer note correctly defers executor/capability constraints; the link model has no executor field, so this belongs to a future authorization ASN.

VERDICT: REVISE
