# Review of ASN-0086

I checked the proofs of R0, R0a, R-Scope, the wp Case 2 derivation, and the Worked Sketch against the foundation contracts. The mathematical core is sound: R0a's two-case antichain argument (zeros-additivity in the cross-home case, uniform-length + T3 in the same-home case) is correct, the R0 freshness discharge covers both emission branches, and the wp Case 2 biconditional holds over the stated restricted domain. The remaining findings are accretion: the same admissibility argument restated at multiple use sites, and scope caveats repeated across sections.

## REVISE

### Issue 1: The "lands on a genuine chain sibling" admissibility argument is restated three times
**ASN-0086, R0 (subsequent-emission, *On-chain admissibility*), Emit_K definition, Nullify definition (PC parenthetical)**:
- R0: "L-ContiguousPrefix … gives that the homed-set … is a contiguous initial segment … so `a = inc(ℓ_prev, 0) …` is the next element of `A_L(d)`."
- Emit_K: "`Emit_K` is total over →*-reachable Σ (R0): L-ContiguousPrefix guarantees `d`'s homed-set … is a contiguous chain prefix of `A_L(d)`, so `a_emit(Σ, d) = inc(ℓ_prev, 0)` lands on a genuine chain sibling…"
- Nullify: "(Under PC, the internal `Emit_R`'s emission lands on a genuine chain sibling: `d_retr`'s homed link-set is a contiguous chain prefix of `A_L(d_retr)` … by L-ContiguousPrefix.)"

**Problem**: One argument (homed-set is an L-ContiguousPrefix chain prefix ⟹ `a_emit` lands on a real sibling) is re-derived at each consumer. R0 already establishes admissibility; Emit_K's totality and Nullify's PC clause should cite R0/L-ContiguousPrefix, not re-walk the derivation. A reader following Emit_K must skip past a restatement of what R0 just proved.
**Required**: State the chain-sibling-landing once (in R0 or L-ContiguousPrefix) and cite it by name at the two operation definitions.

### Issue 2: Out-of-scope scope caveat repeated across sections
**ASN-0086, "Three Operations" intro**: "(Document allocation K.σ and content emission K.α are also visible substrate changes, but lie outside this note's `Σ.L` scope and outside the three operations.)"
**Problem**: This duplicates the State-transition section's "*Arrangement modification is out of scope*" framing and its surrounding K.σ/K.α scope notes. The parenthetical adds no new content; it is meta-prose restating an already-fixed scope boundary at a second site.
**Required**: Drop the parenthetical (the scope is fixed where `→ ≡ K.σ ∪ K.α ∪ K.λ` is introduced), or replace with a bare cross-reference.

### Issue 3: Mutual deferral between the wp Result and Worked Sketch Step 4
**ASN-0086, wp Result (load-bearingness) and Worked Sketch Step 4**:
- Result: "Necessity … is the necessary direction of the biconditional proved in *Derivation (both directions)* below, witnessed concretely by Step 4 of the Worked Sketch…"
- Step 4: "This is the concrete instance of the disjunction's false branch … exactly as the Result's load-bearingness paragraph asserts."

**Problem**: The necessity is actually established in the *Derivation* paragraph; the pointer to Step 4 and Step 4's pointer back form a mutual deferral that carries no proof weight (the example illustrates, it does not discharge). This is the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Keep the necessity proof in *Derivation*; let Step 4 stand as illustration without the back-reference, and trim the forward pointer in the Result to a single non-circular mention.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations and projections
The `|Σ.L(a)| = 3` restriction in Definition — TypedRelation leaves `|Σ.L(a)| > 3` links indexing no `L_K`. Whether these define binary projections or inhabit `L_K^{(n)}` is correctly deferred to Open Questions.
**Why out of scope**: This is new structure (n-ary relation algebra), not a defect in the standard-triple development this note establishes.

### Topic 2: Atomicity of Emit vs. Observe under concurrency
The active/audit distinction's observable consistency under concurrent Emit/Observe is raised in Open Questions and not resolved here.
**Why out of scope**: A consistency model is a separate concern from the state/operation/invariant content this note specifies.

VERDICT: REVISE
