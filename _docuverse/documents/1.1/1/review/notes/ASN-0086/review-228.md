# Review of ASN-0086

The mathematical core is sound. I checked R0/R0a (prefix-antichain), R-Scope, R6a–c, and both weakest-precondition derivations against the foundation contracts and found no correctness defect — the self-emit slack in wp Case 1 and the self-nullification escape in wp Case 2 are both correctly identified and shown weakest. The findings below are accretion (the note carries `review-mode.anti-bloat`) plus one compressed inductive claim.

## REVISE

### Issue 1: The "post-state membership" clarification of the unit-depth discipline is stated three times
**ASN-0086, Definition — Unit-depth retraction discipline / Definition — relational layer / Worked Sketch Step 4**: the clause "Membership `t ∈ A_rel^Σ` is evaluated at the state Σ in question, not at any producing call's pre-state" (discipline def) reappears verbatim-in-substance in the relational-layer definition — "(the Membership clause of *Definition — Unit-depth retraction discipline* evaluates `t ∈ A_rel^Σ` at the state in question, not at the producing call's pre-state)" — and a third time in Step 4 — "maintains the unit-depth retraction discipline because the deposited retractor at `a₃` lands in `A_rel^{Σ_4}`".

**Problem**: The same subtlety (evaluate target-residency at post-state, not pre-state) is re-explained at each site. A reader following the self-emit branch must reconcile three statements of one fact. This is the cross-section accretion the classifier names.

**Required**: State the post-state-evaluation convention once (in the discipline definition) and cite it; drop the re-explanations in the relational-layer definition and Step 4.

### Issue 2: "Definition — relational layer" carries defensive meta-prose and conflates the operation with its wp-cases
**ASN-0086, Definition — relational layer**: "the layer never invokes `Emit_K` at a type index `K ~ R` except through the `Nullify` alias — at either of `Nullify`'s two branches, a P1 target ... or the self-emit branch ... The 'at a P1 target' qualifier alone would be stronger than the discipline requires. With both branches admitted, the layer satisfies the *unit-depth retraction discipline*."

**Problem**: Two issues. (a) `Nullify(Σ, d_retr, a)` is a *single* operation emitting one fixed `Emit_R` call; "Nullify's two branches" are wp-analysis cases (whether `a` pre-exists), not operational branches — describing the layer's permitted *invocations* as occurring "at either of Nullify's two branches" muddles operation and analysis. (b) "The 'at a P1 target' qualifier alone would be stronger than the discipline requires" is a defensive justification of the definition's shape — essay content explaining why the definition is drawn this way rather than stating what the commitment is.

**Required**: State the commitment plainly ("the layer emits type-`R` tuples only via `Nullify`"); move the branch-sufficiency reasoning to where it is used (wp Case 1), and drop the "would be stronger" aside.

### Issue 3: Worked Sketch Step 4's parenthetical re-derives the entire layer-commitment apparatus
**ASN-0086, Worked Sketch, Step 4**: the bracketed passage "(This is the *self-emit branch* of `Nullify` ... The step is therefore a layer operation, not a direct substrate caller ... Only P0 ... governs execution; P1 ... conditions the R-Scope postcondition, not admissibility. Here P0 holds while P1 is false ..., so the call executes as the self-emit instance of wp Case 1 ... Σ_3 lies within the wp's domain by its own pre-state properties ...)".

**Problem**: Step 4's job is to exhibit one concrete instance of wp Case 2's false branch. The parenthetical instead re-states the self-emit branch, the P0/P1 role split, and the domain-membership argument — all already established in *Definition — Nullify*, *Definition — relational layer*, and the wp section. The reader must skip past a re-derivation to reach the actual numeric check (`a₃ = 1.0.1.0.1.0.2.5`, `coverage` contains `a₃`, both disjuncts fail).

**Required**: Reduce the parenthetical to a single pointer ("this is the self-emit branch admitted by *Definition — relational layer*; P1 is false but P0 holds") and keep the concrete computation.

### Issue 4: "The layer satisfies the unit-depth retraction discipline" is asserted without the base+step induction
**ASN-0086, Definition — relational layer**: "With both branches admitted, the layer satisfies the *unit-depth retraction discipline* (Definition — Unit-depth retraction discipline)."

**Problem**: The discipline quantifies over *every state the layer reaches*. The definition shows only that a single `Nullify` emission is disciplined at its post-state. The discharge of the universal requires an explicit induction: base — `Σ_init.L = ∅` so `L_R = ∅` vacuously; step — `Emit_K` at `K ≁ R` leaves `L_R` unchanged, and every `K ~ R` emission is (by the commitment) a `Nullify`, whose added tuple is unit-depth with target in `A_rel^{Σ'}`, preserved in `A_rel` thereafter by L12a. The claim "X follows" is given in one sentence where the carrier is a multi-state invariant.

**Required**: State the two-case induction (base on the empty seed, step over `→`-transitions split into `K ≁ R` and `Nullify`), citing L12a monotonicity for target persistence.

## OUT_OF_SCOPE

### Topic 1: Higher-arity links as nullification targets
A link with `|Σ.L(a)| > 3` lies in `A_rel` and can be a target collected into `nullified(Σ)`, yet indexes no tuple in any `L_K`, so its nullification has no effect on any active subset. This consequence is consistent with the definitions but unexplored. The note's Open Questions already gestures at multi-arity projections — the interaction with nullification belongs there, not in this ASN.

### Topic 2: Elevating the unit-depth discipline to a substrate guarantee
The discipline is a layer convention because `Emit_K`/`K.λ` fix emission address but not endset shape, so a direct substrate caller at `K ~ R` can emit a crafted wide span. Whether to introduce a substrate-level retraction K-operation with a shape constraint is correctly listed as an Open Question.

VERDICT: REVISE
