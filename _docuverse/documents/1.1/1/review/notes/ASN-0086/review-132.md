# Review of ASN-0086

## REVISE

### Issue 1: WP Case 2's "weakest precondition" is invalid over Emit_K's declared domain

**ASN-0086, Weakest-Precondition Analysis, Case 2 (Result/Derivation)**: "`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible`" with derivation "the fresh `a = a_emit(Σ, d)` is prefix-incomparable with every such `b` by K.λ's emission rule together with R0a, so `a ∉ coverage(G')` for any pre-existing retraction."

**Problem**: The sufficiency step ("`a ∉ nullified(Σ')`") invokes R0a's antichain at Σ'. R0a holds **only at substrate-conforming states**. But Emit_K's domain is explicitly declared (Definition — Emit_K) as "the state-local-conforming sub-space ... which ... admits the antichain-violating non-conforming states besides." Over that declared domain the stated wp is **not even a valid precondition**, let alone the weakest:

Take a state-local-conforming but non-substrate-conforming Σ of the kind the note itself constructs (Definition — state-local-conforming state: emit `a'' = inc(a, 1)` at an existing home, yielding a nested pair). Let `b'` be a pre-existing link at home `d` with `#b' < #ℓ_prev` and `b' ≼ ℓ_prev`, where `b'` is the target of a pre-existing unit-depth retraction. The subsequent-branch emission `a = a_emit(Σ, d) = inc(ℓ_prev, 0)` preserves positions `1..#ℓ_prev − 1`, so `b' ≼ a`, hence `a ∈ coverage({(b', δ(1, #b'))})` and `a ∈ nullified(Σ')`. Then `(a, F, G) ∉ A_K^{Σ'}` even though `d ∈ dom(Σ.M) ∧ K ∈ T_admissible` both hold. The wp fails on a state in its own declared domain.

The derivation patches this by appealing to "the relational layer is substrate-conforming ... so R0a's antichain ... is available at its call sites" — smuggling substrate-conformance in as an ambient fact rather than a precondition conjunct. This is exactly the inconsistency Case 1 avoids: Case 1 carries PC (`Σ substrate-conforming`) as an explicit conjunct and then proves non-weakestness. Case 2 silently drops the analogous conjunct.

**Required**: Reconcile the domain. Either (a) add a substrate-conformance conjunct to the Case 2 wp (`d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ Σ substrate-conforming`), acknowledging it no longer collapses to the two operation-preconditions; or (b) explicitly restrict the domain over which Case 2's wp is asserted to substrate-conforming Σ and state that restriction at the point of the claim — matching Case 1's treatment. As written, "Result" asserts a weakest precondition over a domain on which it is false.

### Issue 2: Dangling "(i)–(iii)" reference in the state-transition section

**ASN-0086, State transition relation**: "By the frame conditions of (i)–(iii) stated above, `Σ →* Σ'` entails `dom(Σ.C) ⊆ dom(Σ'.C)` ..."

**Problem**: There is no enumerated list `(i)`, `(ii)`, `(iii)` above this sentence. The preceding "Concretely, each `→`-step is one of:" introduces a single bullet that names K.σ/K.α/K.λ without numeric labels. The reference points at labels that do not exist.

**Required**: Either label the three step-types `(i)/(ii)/(iii)` at their introduction, or replace "(i)–(iii)" with "the K.σ/K.α/K.λ frame conditions."

### Issue 3: Redundant restatement of the single-fresh-home / n=1 decomposition in R7a

**ASN-0086, R7a (statement paragraph and post-proof paragraph)**: The statement contains "When an `↝`-step is itself a primitive adding a single fresh key ... the sequence has length 1; a composite that simultaneously adds fresh document and link keys decomposes into K.λ-extensions, each prefixed by the K.σ-step ..."; the paragraph after the proof restates "The single-fresh-home case is the `n = 1` collapse: a composite that allocates one fresh document `d_new` and emits one link ... decomposes into the length-2 sequence ..."

**Problem**: These two passages assert the same decomposition fact (single-key/single-fresh-home reduces to a short K.σ-then-K.λ sequence), with the post-proof paragraph adding nothing the statement and discharge (4)(iii) did not already establish. This is the duplicated-paragraph pattern the anti-bloat classifier flags.

**Required**: Keep one. The discharge (4)(iii) argument already covers the general case; delete the trailing recap (or fold its one novel token — the explicit length-2 count — into discharge (4)).

### Issue 4: Repeated boilerplate clarifications across sections

**ASN-0086, multiple sites**:
- The phrase "well-definedness ... rests on L-fin and T1 trichotomy alone" / "the unique T1-extremum of a finite (L-fin) ... set, by T1 ... trichotomy alone" recurs in Definition — `a_emit`, Lemma — Emit_K function-ness, and wp Case 2 "Result."
- The "usage discipline, not the operation's own domain" clarification appears both in Definition — Nullify (*Single-tuple scope under R0a*) and again in wp Case 1 (*Domain of quantification*: "describes the relational layer's usage discipline, ... not the operation's own domain").

**Problem**: `a_emit`'s well-definedness is established once at its definition; re-deriving the same L-fin/T1 justification at each consumer is use-site repetition. The usage-discipline-vs-domain distinction is stated twice in near-identical words across two sections (the "two paragraphs say the same thing in different words" pattern).

**Required**: State each fact once at its definitional home and cite it thereafter ("`a_emit` well-defined by its Definition"; the usage-discipline distinction belongs at Definition — Nullify, referenced — not restated — in wp Case 1).

## OUT_OF_SCOPE

### Topic 1: Substrate-level enforcement of the unit-depth retraction discipline
**Why out of scope**: Open Question 7 already frames whether `L_R` to-span shape should become a substrate guarantee via a dedicated K-operation. That is a design decision for a future ASN (a new substrate operation), not a defect in this note's layer-convention framing. The note correctly marks the discipline as a layer commitment that direct K.λ callers can bypass.

### Topic 2: Higher-arity typed relations and binary projections
**Why out of scope**: The note explicitly restricts `L_K`/`A_K` to arity-3 links and defers `|Σ.L(a)| > 3` (Open Questions). Building the `L_K^{(n)}` machinery is new territory for a later ASN.

VERDICT: REVISE
