# Review of ASN-0086

## REVISE

### Issue 1: Non-monotonicity of `A_K` cites the wrong worked-sketch step

**ASN-0086, Consequence after R6c ("A_K is not monotone, though L_K is")**: "the active subset is not — a retraction shrinks `A_K` while a later re-emission grows it at a fresh address (R0), so neither `⊆` nor `⊇` holds in general between `A_K^Σ` and `A_K^{Σ'}`. Worked Sketch Step 3 exhibits the witness."

**Problem**: The cited witness is wrong, and contradicts the sketch's own arithmetic. Worked Sketch Step 3 (retraction of the retractor `b₁`) computes `A_K^{Σ_3} = {(a₂, F₁, G₁)}` and states it is "*unchanged from A_K^{Σ_2}*." A step that leaves `A_K` unchanged satisfies both `⊆` and `⊇` trivially — it is the opposite of a non-monotonicity witness. The transitions that actually witness failure of both inclusions are the ones the same sentence *describes*: Step 1 (Nullify a₁: `A_K^{Σ_0} = {(a₁,F₁,G₁)}` shrinks to `A_K^{Σ_1} = ∅`, so `A_K^{Σ_0} ⊄ A_K^{Σ_1}` — `⊆`-monotonicity fails) and Step 2 (re-emission: `A_K^{Σ_1} = ∅` grows to `A_K^{Σ_2} = {(a₂,F₁,G₁)}`, so `A_K^{Σ_2} ⊄ A_K^{Σ_1}` — `⊇`-monotonicity fails). A reader following the citation to Step 3 finds the claim unsupported.

**Required**: Replace "Worked Sketch Step 3 exhibits the witness" with a citation to Steps 1 and 2 (the retraction-shrink and re-emission-growth transitions), which are the actual witnesses for failure of `⊆` and `⊇` respectively.

### Issue 2: Repeated deferrals to the same downstream location (anti-bloat)

**ASN-0086, multiple sites**: The `review-mode.anti-bloat` pattern "multiple paragraphs in different sections defer to the same downstream location" recurs:
- L-ContiguousPrefix proof ("Extension to substrate-conforming states"): "this inclusion's strictness is recorded at Definition — state-local-conforming state."
- WP "Domain restriction": "this inclusion is strict per Definition — state-local-conforming state."
- Definition — Nullify: "(their roles are analyzed in Weakest-Precondition Analysis, Case 1)" — forward pointer to WP Case 1.
- Consequence after R6c: "Worked Sketch Step 3 exhibits the witness" (also Issue 1).

**Problem**: The strictness of `{substrate-conforming} ⊊ {state-local-conforming}` is established once at its home (Definition — state-local-conforming state) with the NestedLinkWitness; two later proofs pause to re-point at it rather than simply using the fact. The Nullify definition defers its precondition-role analysis forward to the WP section. These cross-references force the reader to navigate away from the live claim to confirm support that is either already established or supplied locally.

**Required**: Drop the back-references to the strictness fact (use it silently — it is already proved at its home), and inline (or remove) the parenthetical forward pointer in Definition — Nullify so each claim is self-supporting at its site.

## OUT_OF_SCOPE

### Topic 1: Elevating the unit-depth retraction discipline to a substrate guarantee
The note correctly treats the unit-depth retraction discipline as a layer convention (and the WP Case 2 domain restriction depends on it). Whether the substrate should instead expose a dedicated retraction K-operation with a value-shape constraint is raised in Open Questions and is genuinely new territory, not a defect here.

### Topic 2: Higher-arity typed relations and dynamic type allocation
The restriction to standard-triple links (`|Σ.L(a)| = 3`) for `L_K` membership, and the coordination question for layers choosing colliding ghost type addresses, are flagged as open questions and belong to a future ASN.

VERDICT: REVISE
