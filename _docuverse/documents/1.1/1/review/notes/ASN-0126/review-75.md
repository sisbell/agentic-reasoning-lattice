# Review of ASN-0126

The proofs check out. I worked P1–P6, the ProjectionBridge induction, the B1/B2 split (including the existence-of-successor exclusion), the R-Scope transfer (the frame argument that a_emit's F-blindness makes the wrapper and Nullify share `dom(Σ'.L)`), the wp derivation (g_sh ∧ Case-2 RHS, with (0) absorbed because the A_K postcondition forces the arity-3 slice), Lemma RegisteredAdmissible, and the born-nullified arithmetic in the worked illustration (`a_R = …2.3`, `g = …2.4 ∈ coverage(G_rng)`). All sound. The one finding is accreted prose, which is what this note's anti-bloat mode asks me to surface.

## REVISE

### Issue 1: The registry section restates its two core facts several times each
**ASN-0126, The registry**: The section establishes (a) entries are keyed by coverage class and (b) `name` is opaque — and restates each repeatedly.

Coverage-class keying: "Registration is keyed by *coverage class*, not by raw endset"; then "the key of an entry is the coverage class `[K]`, equivalently, the registry assigns `~`-equal endsets one and the same entry"; then "Each registry entry thus records such a representative endset `K_j`"; then "Equivalently, a well-formed registry *is* a partial function `T_admissible/~ ⇀ (name, shape)`."

Name opacity, four times in one chain: "opaque app-level metadata, uninterpreted by the framework"; "no framework invariant, predicate, or operation reads it"; "carried in the registry tuple only as opaque payload"; "the framework preserves it but never inspects it."

**Problem**: Of the four name clauses, only two carry content — names need not be unique, and names inherit P1's no-drift; the other four merely re-say "uninterpreted." Among the keying clauses, the "equivalently …" sentence and "Each registry entry thus records …" re-fix what the opening sentence already fixed. The precise reader must skip past restatement to reach the few load-bearing points (concrete representative storage; key uniqueness vs. name collision; no-drift inheritance). This is the "two paragraphs say the same thing in different words" pattern, compressed into one section.

**Required**: State each fact once. For keying: "The registry is a partial function `T_admissible/~ ⇀ (name, shape)`; a key is a coverage class `[K_j]`, stored concretely as a representative `K_j ∈ T_admissible` against which CoverageEqualityDecidable settles membership." For name: "a **name** — opaque payload the framework never reads; only keys are constrained unique, so names may collide, and a name never drifts (P1)."

## OUT_OF_SCOPE

### Topic 1: Observational reading of the canonical from-fill
The Binary re-expression of retraction forces a non-empty from-set, filled canonically with `r = (d_retr, δ(1, #d_retr))`, whose coverage is the whole home-document subtree `{t : d_retr ≼ t}`. ASN-0086's `Observe_K` matches on `coverage(F)`, so a from-pattern query would "see" this filler even on retractions the app intends as unattributed. What an observer should make of the canonical filler is operational semantics (Open Question 2), not a gap in this note.

**Why out of scope**: This note specifies the static shape gate and registry invariants; observation behavior is explicitly deferred to the operational-semantics successor.

VERDICT: REVISE
