# Review of ASN-0042

## REVISE

### Issue 1: Delegation ordering permits unauthorized nesting — Account-level permanence Corollary unsupported

**ASN-0042, Permanence and Refinement (Corollary)**: "No delegation can introduce a principal whose prefix extends pfx(π) without π's involvement: condition (ii) of the delegated relation requires the delegator to be the most-specific covering principal for the new prefix. For any prefix extending pfx(π), that most-specific covering principal is π itself (or a sub-delegate of π within dom(π)) — the base case holds by O14's non-nesting constraint"

**Problem**: The delegation relation's five conditions do not prevent a higher-level principal from delegating a longer prefix *before* delegating the shorter enclosing prefix. Condition (ii) checks whether the delegator is the most-specific covering principal for the new prefix — it examines prefixes *of* the target, not extensions *beyond* it.

Counterexample:

1. `Π₀ = {π_N}`, `pfx(π_N) = [1]`
2. `π_N` delegates to `π₂`, `pfx(π₂) = [1, 0, 2, 3]` — all five conditions satisfied (`π_N` is the sole covering principal for `[1, 0, 2, 3]`)
3. `π_N` delegates to `π₁`, `pfx(π₁) = [1, 0, 2]` — all five conditions satisfied (`pfx(π₂) = [1, 0, 2, 3]` has length 4 > 3 = `#[1, 0, 2]`, so `π₂` does not cover `pfx(π₁)`; `π_N` remains the sole covering principal)

After step 3: `pfx(π₁) = [1, 0, 2] ≺ pfx(π₂) = [1, 0, 2, 3]`, so `dom(π₂) ⊂ dom(π₁)`. But `π₁` never authorized `π₂`'s existence. Concretely, `π₂` can now delegate `pfx(π₃) = [1, 0, 2, 3, 5]` — changing `ω` for addresses in `dom(π₁)` without `π₁`'s involvement, because `π₂` (not `π₁` or any sub-delegate of `π₁`) is the most-specific covering principal for `[1, 0, 2, 3, 5]`.

The Corollary's inductive proof claims the base case holds by O14's non-nesting constraint. This works for bootstrap principals (`π ∈ Π₀`), but fails for delegated principals: when `π₁` enters `Π` in step 3, `π₂` already has a prefix extending `pfx(π₁)`. The base case — "no principal other than `π` itself has a prefix extending `pfx(π)`" — is already violated at `π₁`'s moment of creation.

O14 correctly requires non-nesting at bootstrap. The same principle must extend to delegation to support the Corollary.

**Required**: Add a sixth delegation condition preventing out-of-order creation, e.g.:

> (vi) `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))` — no existing principal has a prefix strictly extending the new delegate's prefix

This forces top-down delegation order (parent before child), matching Nelson's hierarchical design intent. With (vi), when `π'` enters `Π`, no principal already occupies a sub-domain of `dom(π')`, and the Corollary's base case holds for all principals — bootstrap or delegated. Without it, the "forevermore" guarantee that the ASN derives from Nelson is formally unsupported.

### Issue 2: Primitive relation "allocated by" undeclared

**ASN-0042, O5**: "`a` newly allocated by `π`"
**ASN-0042, O16**: "`a` allocated by `π`"

**Problem**: The relation "a allocated by π" appears in two formal properties but is never declared as a primitive or given a formal signature. The ASN defines `delegated_Σ(π, π')` with five explicit conditions and lists it in the Properties Introduced table. The parallel allocation relation receives neither treatment. A reader cannot distinguish "allocated by" as casual prose from a formal relation that O5 and O16 constrain.

**Required**: Declare `allocated_by_Σ(π, a)` as a primitive relation (its mechanism is out of scope per the ASN's own scope declaration, but its signature must be stated). Add it to the Properties Introduced table alongside `delegated_Σ`.

### Issue 3: O12 motivation overstates orphaning risk

**ASN-0042, State Axioms (O12)**: "removing the principal would orphan its domain with no effective owner, violating O4 below"

**Problem**: When nesting exists, removing a principal does not orphan its domain — the parent principal (whose prefix is shorter) still covers every address, and `ω` reverts to the parent. The orphaning claim holds only when the removed principal is the sole covering principal (i.e., no higher-level principal exists). The actual formal reasons O12 is needed: removal would allow `ω` to decrease in specificity (violating O3's monotonic refinement) and would reverse a delegation (violating O8's irrevocability). The Nelson/Gregory evidence ("no concept of account revocation," "no deletion path") is correct and sufficient as primary motivation.

**Required**: Correct the orphaning sentence. Either remove it (letting the Nelson/Gregory evidence stand alone) or replace with the accurate formal observation: removing a principal would reverse refinement of `ω` and undo a delegation, effects that O3 and O8 formalize as prohibited.

## OUT_OF_SCOPE

(None beyond the open questions already identified by the ASN.)

VERDICT: REVISE
