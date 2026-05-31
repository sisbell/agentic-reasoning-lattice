# Review of ASN-0093

## REVISE

### Issue 1: The load-bearing fact `M(d) = ∅` is asserted in prose but never enumerated or inductively discharged

**ASN-0093, Scope / Arrangement-function invariants**: "arrangement-side invariants from ASN-0036 (S2, S3, S8a, S8-depth, S8-fin, D-CTG, D-MIN) hold vacuously here since `M(d) = ∅` for every `d ∈ dom(M)`."

**Problem**: The vacuous satisfaction of the entire ASN-0036 arrangement-invariant family rests on the proposition `(A d ∈ dom(M) :: M(d) = ∅)`. That proposition is genuinely true under the substrate (`K.σ` sets `M'(d) = ∅`; `K.α`/`K.λ` hold `M` in frame), but it is never given an invariant ID, never appears in the *Properties Introduced* table, and never appears as a row in the discharge matrix. M0 and M1 constrain only `dom(M)`, not the per-document arrangement value. A reader cannot verify the vacuity claim without reconstructing an induction the note declines to state. By the standard that every load-bearing invariant must be discharged, the proposition the vacuity rests on must itself be a proved invariant, not a parenthetical.

**Required**: Add an invariant (e.g. `M2 (EmptyArrangement): (A d ∈ dom(M) :: M(d) = ∅)`) with base case `Σ₀.M = ∅` and a one-line matrix row (K.σ: discharged at the new key by the effect clause `M'(d) = ∅`; K.α/K.λ: preserved, `M` in frame). Then cite M2 as the explicit ground for the vacuity of S2/S3/S8a/S8-depth/S8-fin/D-CTG/D-MIN.

### Issue 2: SD invariant carries naming-justification meta-prose

**ASN-0093, L-fin / SD (StoreDisjointness)**: "We use the fresh ID `SD` rather than reusing ASN-0043's `L14` (DualPrimitive), which the foundation binds to a different invariant: SD strengthens DualPrimitive's disjointness clause from the `s_C`-sliced `dom(L) ∩ dom(C)|_{s_C} = ∅` to the full `dom(C) ∩ dom(L) = ∅`..."

**Problem**: This is exactly the accretion pattern the anti-bloat mode flags — prose justifying an ID choice rather than advancing the invariant. The substantive content (SD strengthens the disjointness to the full union, valid because every content address resides in `s_C`) is worth keeping; the ID-selection rationale ("We use the fresh ID SD rather than reusing L14...") is meta-commentary about the document's relationship to the foundation, not about the system.

**Required**: State SD and its derivation (`L0 + SC-NEQ + StoreT4Validity + T7`, full union justified by `C1 + L0`'s C-clause). Drop the "we use the fresh ID rather than..." framing; at most one clause noting SD is strictly stronger than ASN-0043's L14.

### Issue 3: Freshness lemmas appear as circular rows in the lemma-preservation matrix

**ASN-0093, Discharge — "Lemma preservation across transitions" table**: rows **FirstEmissionFreshness** ("Discharged at the K.α event when the first-emit predicate fires, by FirstEmissionFreshness (lemma above)") and **SubsequentEmissionFreshness** (analogous).

**Problem**: These two rows discharge a property by citing the lemma of the same name. The row advances no reasoning — it restates that the lemma exists. Unlike ChainMembershipForOrigin and StoreT4Validity (which are state invariants genuinely re-established at each transition), FirstEmissionFreshness/SubsequentEmissionFreshness are event-local discharges of a single emission's freshness; they are not state properties that need per-transition preservation rows. The matrix slot makes them look like inductive obligations when they are one-shot applications already fully proved in their own lemmas.

**Required**: Remove these two rows from the lemma-preservation matrix (the freshness obligations are already discharged at the K.α/K.λ binding preconditions and the SD matrix row, both of which already cite the lemmas), or replace the self-referential entry with the actual hypothesis-discharge (which pre-state IH the lemma consumes), not the lemma's own name.

### Issue 4: Scope "Entity allocation" bullet enumerates a downstream primitive's internal composition

**ASN-0093, Scope — Deferred**: "A higher-layer document-introduction primitive rebuilds itself as `K.σ` plus entity-set tracking, lineage discipline, and version-allocator activation."

**Problem**: The deferral is legitimate; the enumeration of *how a future primitive will be composed* is speculative downstream detail that does not advance the substrate's reasoning. This is the "enumerates downstream consumers" pattern.

**Required**: State that entity allocation (the entity-hierarchy machinery layered on `K.σ`) is deferred, without specifying the future primitive's component list.

## OUT_OF_SCOPE

### Topic 1: Spelling the `k = 1 ⟹ zeros ≤ 3` side condition in C1c/L1c
The substrate's C1c/L1c parenthetical spells only the `k = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` constraint where ASN-0043's L1c spells both. "T4-validity preservation" subsumes the `k = 1` case, so this is a wording choice, not an error — not a revision item.

VERDICT: REVISE
