# Review of ASN-0086

This ASN is rigorous at the proof level — R0a's cross-home zero-counting argument, the wp Case 2 biconditional, and CoverageEqualityDecidable's cell-decomposition all hold up under scrutiny, and the boundary cases (first emission, self-nullification, retraction-of-retractor) are exercised concretely in the Worked Sketch. The findings below are almost entirely the forward-reference/anti-bloat accretion the active classifier asks me to surface, plus one scoped exclusion.

## REVISE

### Issue 1: M2 / empty-arrangement derivation is consumed by no claim
**ASN-0086, "State transition relation" → *Arrangement modification is out of scope***: "ASN-0093's M2 (EmptyArrangement) — `(A d ∈ dom(M) :: M(d) = ∅)` — is the invariant that results: empty initialization plus the absence of any arrangement-modifying operation keeps every arrangement empty at every reachable state."

**Problem**: No definition, operation, or proof in this note consumes M2 or the fact `M(d) = ∅`. R0–R6, Emit/Observe/Nullify, and the wp analysis touch only `Σ.L` and `dom(Σ.M)` (the latter for home-existence, never for arrangement *content*). R6c's persistence is about `nullified`, not arrangements. This is an "out of scope" essay sub-paragraph that re-derives an unused invariant — exactly the structural-slot meta-prose the classifier flags. (Note: this is *not* the previously-declined attribution finding; the attribution is correct. The issue is that the derivation advances nothing.)

**Required**: Delete the M2 derivation. If scoping `→` to the three K-operations needs stating, one sentence ("the substrate exposes no arrangement-modifying transition") suffices and is already present in the preceding paragraph.

### Issue 2: The `a_emit` emission rule is restated in three places
**ASN-0086, "Working domain — `→*`-reachable states"**: "For K.λ, the step lands its single fresh link key at its home's sibling frontier (`[d.0.s_L.1]` for an empty homed-set, else `inc(ℓ_prev, 0)` at the prior T1-maximum)."

**Problem**: This is a verbatim restatement of **Definition — `a_emit`** (Allocator Structure), which formally fixes the same first/subsequent-emission rule, and it recurs again in R0's branch analysis and across the Worked Sketch. Stating the emission rule in the Working-Domain prose *before* its formal definition adds nothing and is the kind of duplication that compounds across cycles.

**Required**: State the rule once, in Definition — `a_emit`, and have the Working-Domain paragraph cite it by name rather than paraphrase it.

### Issue 3: `T_ghost^Σ` is defined but never consumed
**ASN-0086, Definition — GhostAddresses** and the following *Notation* aside ("All four sets are state-dependent … `T_ghost^Σ` shrinks as content and link emissions populate previously-ghost addresses").

**Problem**: `T_ghost^Σ` appears only in its own definition, the *Notation* aside, and the Properties table. No claim, operation, or proof references it — the ghost-targeting discussions in `T_admissible` and `Observe_K`'s pattern domain quantify over `T`, not `T_ghost^Σ`. A defined-but-unconsumed set plus a monotonicity aside about it is bloat.

**Required**: Either fold the ghost notion into the prose where L9 is cited (no standalone state-indexed set), or delete it.

### Issue 4: Forward pointers used where a citation would do
**ASN-0086, Definition — TypedRelation**: "their analogous construction with additional slot positions is not pursued here (Open Questions)"; and **AdmissibleTypes** previews `~` ("Type-equivalence is coverage equality, written `~` (Definition — TypeEquivalence)") ahead of its own definition.

**Problem**: These are "see X below"/"deferred to Y" deflections in definitional slots — the multi-arity deferral adds no content beyond "out of scope," and the `~` preview duplicates the later Definition — TypeEquivalence.

**Required**: Drop the multi-arity parenthetical (the Open Questions list already carries it); remove the inline `~` preview and let Definition — TypeEquivalence stand alone.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations (`|Σ.L(a)| > 3`)
**Why out of scope**: The `|Σ.L(a)| = 3` conjunct in TypedRelation deliberately restricts `L_K` to standard triples, and L3 (ASN-0043) permits `N > 3`. Defining `L_K^{(n)} ⊆ A_rel × ℘(A)^n` is genuinely new relational structure, correctly deferred to the Open Questions rather than treated as a gap in this note's binary-relation model.

### Topic 2: Substrate enforcement of the unit-depth retraction discipline
**Why out of scope**: The wp Case 2 result is weakest only over the unit-depth-disciplined sub-domain, and the note is explicit that this is a layer commitment the substrate does not enforce (the address-vs-shape gap). Whether to add a substrate-level retraction K-operation with a shape constraint is a future design decision, already posed in Open Questions, not an error here.

VERDICT: REVISE
