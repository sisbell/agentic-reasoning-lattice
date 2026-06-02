# Review of ASN-0086

## REVISE

### Issue 1: Retraction silently excludes higher-arity links
**ASN-0086, Definition — Nullified / Definition — TypedRelation**: "`nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}`"

**Problem**: `L_R^Σ = L_K^Σ` at `K = R`, and `L_K^Σ` carries the conjunct `|Σ.L(a)| = 3`. So only standard-triple links can be *retractors*. The note explicitly admits `N > 3` links (L3, NEndsetStructure) and states they "inhabit `A_rel^Σ` but index no tuple of any `L_K`" — hence a 4-endset link with slot-3 coverage equal to `coverage(R)` and its target in slot 2 has **no** nullifying effect whatsoever. Given the note foregrounds `N ≥ 3` support (and quotes Nelson on n-sets), a reader will reasonably expect a retraction-typed higher-arity link to retract. The asymmetry is real and unaddressed: it is neither stated as deliberate nor justified.

**Required**: State explicitly that retraction is standard-triple-only and give the reason (e.g., slot-2 to-set is only convention-fixed for triples), or extend `nullified` to range over retraction-typed links of any arity. Either way the current silent exclusion must be made visible.

### Issue 2: R5 *Consequence* previews the retraction mechanism before it is defined
**ASN-0086, R5 Consequence**: "self-targeting enables retraction without mutation: a tuple in a designated relation `L_R` whose to-set contains the address of the tuple being nullified ... mutation becomes Emit, and `L_K` is never modified (R3)."

**Problem**: R5 establishes only that the unit-depth span `(a, δ(1, #a))` is an admissible endset member. This *Consequence* paragraph instead asserts the entire downstream retraction design — `L_R`, the designated type `R`, "mutation becomes Emit" — none of which is defined until "The Active Subset" several sections later (`L_R`, RetractionType, nullified) and "Three Operations" (Nullify). This is relocated design essay sitting in R5's consequence slot; it advances none of R5's own reasoning and forward-references machinery the reader cannot yet evaluate. Exactly the forward-reference accretion the anti-bloat classifier targets.

**Required**: Reduce to a one-line pointer ("self-targeting is what makes the Nullify operation of *Three Operations* possible") or delete; let the retraction design appear where it is defined.

### Issue 3: Mutual wp ↔ Worked-Sketch cross-pointer adds no reasoning
**ASN-0086, wp Case 1 self-emit branch**: "This is the same self-emit configuration constructed in Worked Sketch Step 4 (`a₃ = a_emit(Σ_3, d)`)." — paired with Worked Sketch Step 4: "verifies the wp Case 2 false branch ... the concrete instance of the disjunction's false branch."

**Problem**: The wp derivation is self-contained (it establishes the self-emit branch directly via R0a). The forward pointer to Step 4, which itself points back to the wp, is a bidirectional cross-reference that carries no part of either argument. A reader following the wp proof does not need Step 4; a reader following Step 4 already has the wp result above.

**Required**: Drop the wp-side pointer. The worked sketch may cite the wp (a concrete example referencing the general claim is fine); the general proof should not lean on the example.

## OUT_OF_SCOPE

### Topic 1: Cardinality bound on `nullified(Σ)` relative to `dom(Σ.L)`
Whether unbounded retraction is permitted or some structural ratio must hold is genuinely new territory — correctly deferred to the Open Questions, not an error here.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate guarantee
The convention-vs-guarantee status of the discipline (and whether a dedicated retraction K-operation should enforce unit-depth shape) is a substrate-design decision for a future ASN; the note correctly scopes it as a layer commitment and flags it as open.

VERDICT: REVISE
