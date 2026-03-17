# Review of ASN-0047

## REVISE

### Issue 1: Temporal decomposition claim is ambiguous between elementary and composite transitions
**ASN-0047, Temporal decomposition**: "No transition modifies all three layers simultaneously."
**Problem**: The preceding sentence establishes context ("The decomposition constrains the elementary transitions cleanly"), but the claim itself uses unqualified "transition." Composite transitions routinely span all three layers — insertion is K.α (existential) + K.μ⁺ (presentational) + K.ρ (historical). A reader who takes the sentence at face value for composites finds it contradicted by the ASN's own coupling constraints (J0 couples K.α with K.μ⁺; J1 couples K.μ⁺ with K.ρ). A formal specification should not require contextual inference to disambiguate a universal claim.
**Required**: "No *elementary* transition modifies all three layers simultaneously." Alternatively, add a sentence noting that composite transitions can and do span layers — the point is that each elementary step touches at most one.

### Issue 2: K.μ⁻ arrangement invariant preservation is asserted but not shown
**ASN-0047, K.μ⁻ (Arrangement contraction)**: "A general constraint applies to all transitions that modify arrangements: the ASN-0036 arrangement invariants — S2 (functional), S3 (referential integrity), S8a (V-position well-formedness), S8-depth (uniform depth within subspace), S8-fin (finite domain) — must hold at the final state of every composite transition."
**Problem**: K.μ⁺ explicitly addresses all five invariants in its precondition block (S3 for new mappings, S8a and S8-depth for new V-positions, S8-fin for the result). K.μ~ addresses S8a and S8-depth as preconditions. K.μ⁻ lists only `d ∈ E_doc` as a precondition and says nothing about invariant preservation. The preservation is trivially true — removing entries from a valid partial function preserves functionality (S2), referential integrity of survivors (S3, since C' = C), well-formedness (S8a), uniform depth (S8-depth), and finiteness (S8-fin) — but the ASN sets a standard of explicit verification with K.μ⁺ and then drops it for K.μ⁻. One sentence noting that contraction trivially preserves all five invariants (subset of a valid arrangement is valid) would close this.
**Required**: Add a brief note to K.μ⁻ stating that removing mappings from a valid arrangement trivially preserves S2, S3, S8a, S8-depth, and S8-fin, since the surviving arrangement is a restriction of the pre-state arrangement.

### Issue 3: K.δ spans two layers but the temporal decomposition table classifies it as purely existential
**ASN-0047, Temporal decomposition table**: K.δ is listed solely in the existential row (C, E).
**Problem**: When IsDocument(e), K.δ initializes M'(e) = ∅ — extending the domain of M, which is a presentational-layer component. The text correctly describes this effect in the K.δ definition, and the broader claim ("No transition modifies all three layers simultaneously") remains true even accounting for this. But the table says the existential layer's elementary transitions are {K.α, K.δ} and the presentational layer's are {K.μ⁺, K.μ⁻, K.μ~}, placing K.δ exclusively in one row. A reader consulting only the table would miss that document creation touches M.
**Required**: Either add a footnote/parenthetical to the table noting that K.δ for documents also initializes M(e) = ∅, or add K.δ to the presentational row with a qualifier. The distinction between "extending M's domain with an empty entry" and "mutating an existing arrangement" is worth one sentence.

## OUT_OF_SCOPE

### Topic 1: Content orphaning after universal deletion
After K.μ⁻ removes an I-address `a` from every arrangement that references it, `a` persists in dom(C) (P0) with stale provenance in R (P2), but appears in no arrangement. The ASN correctly allows this state — J0 constrains allocation, not subsequent liveness. What guarantees, if any, the system provides about discovering or recovering such orphaned content is a question for a provenance query or garbage collection ASN.
**Why out of scope**: This ASN establishes transition mechanics and invariants. Query semantics and content lifecycle beyond transitions are separate concerns.

### Topic 2: Commutativity of elementary transitions within composites
Which elementary transitions can be reordered within a composite without changing the net effect? K.α must precede K.μ⁺ (S3 requires the I-address in dom(C)), K.δ must precede K.μ⁺ for freshly created documents, but K.α and K.δ on unrelated entities commute. A commutativity analysis would clarify which composite orderings are equivalent.
**Why out of scope**: The ASN defines the sequential composition model and coupling constraints. Equivalence classes of orderings are an optimization/analysis concern for a future ASN.

### Topic 3: J0 does not require placement in the origin document
J0 requires freshly allocated content to appear in *some* arrangement, not necessarily the origin document's. Content allocated under d₁'s prefix could be placed only in d₂'s arrangement (direct transclusion at allocation time). Whether this is intentional or should be further constrained is a design question for the named-operations ASN.
**Why out of scope**: J0 captures the minimal constraint (no orphan content at birth). Tighter placement constraints depend on operation semantics not yet specified.

VERDICT: REVISE
