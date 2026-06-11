# Review of ASN-0121

## REVISE

### Issue 1: FL-JUNK's claims-table row drops the load-bearing no-retraction hypothesis
**ASN-0121, Claims Introduced table, FL-JUNK row**: "Non-impedance — the result is invariant under addition of non-matching links and unaffected by their quantity; match status is decided per link"
**Problem**: The body's FL-JUNK is correctly hypothesized: it requires *both* `nullified(Σ') = nullified(Σ)` ("retracts nothing") *and* that the added links fail the request. The table row states only the second hypothesis. Read standalone — and these tables are what gets extracted as claim statements for downstream ASNs — the row is false. Counterexample: a single K.λ adds a retraction link `b = (∅, G', Θ_R)` with a current member `a ∈ findlinks(q, Σ)` in `coverage(G')`, where `b` itself fails `q` (e.g., `q.F` constrained, so `lift(∅, q.F) = false` by FL-EMP). The step adds one non-matching link, yet `a ∈ nullified(Σ')` by the ASN's own case-(c) membership equation, so `a` exits the answer. "Invariant under addition of non-matching links" does not hold without the nullified-equality conjunct.
**Required**: Carry the hypothesis into the row, e.g., "across any sequence with `nullified(Σ') = nullified(Σ)` whose added links all fail the request, the result is invariant; match status is decided per link."

### Issue 2: FL-DEC is stated and proven two sections before its ingredients exist
**ASN-0121, "What is being matched"**: "consequently `sat(a, q, Σ)` is decidable per link, and `findlinks(q, Σ)` is a finite, computable set. … The *addressability filter* over which FL-DEF ranges is computable by exactly ASN-0086's ActiveSubset argument…"
**Problem**: At this point in the document, `sat` (next section), `nullified`/`addressable`, and FL-DEF ("The answer is forced," two sections later) are all undefined. The proof of FL-DEC consumes every one of them: it asserts decidability of a predicate not yet written down and computability of a filter whose definition has not yet been given. A reader verifying FL-DEC at its location cannot discharge it; the same lead-in sentence ("`touch` must be decidable for `findlinks` to be a realisable query") references the operation before it is defined.
**Required**: Restrict FL-DEC at this location to what is definable here — decidability of `touch` and `athome` — and state the corollary (per-link decidability of `sat`, finiteness and computability of `findlinks` via the addressability filter and L-fin) immediately after FL-DEF, where its terms exist. Alternatively move FL-DEC wholesale after FL-DEF.

### Issue 3: "`L_R^Σ ⊆ Σ.L`" is type-incorrect (three occurrences)
**ASN-0121, "The answer is forced"** ("the retraction relation `L_R^Σ`, which is itself a subset of the link store"), **FL-LOC proof** ("the retraction relation `L_R^Σ ⊆ Σ.L`"), and **claims table, FL-LOC row** ("defined through `L_R^Σ ⊆ Σ.L`")
**Problem**: By ASN-0086's definition, `L_R^Σ` is a set of triples `(a, F, G)` — the slot-3 endset is dropped and the value is reshaped — while `Σ.L` is a partial function `T ⇀ Link` (as a graph, a set of pairs `(a, (e₁, …, e_N))`). No member of `L_R^Σ` is a member of `Σ.L`, so the inclusion `L_R^Σ ⊆ Σ.L` is a category error. The conclusion being justified (that `nullified` is a function of `Σ.L` alone) is correct, but the stated justification commits the error in formal notation, and the error is propagated into the claims table.
**Required**: Replace all three occurrences with a correct formulation, e.g., "`L_R^Σ` is determined by `Σ.L` — it is selected from `dom(Σ.L)` by the arity-3 and slot-3 coverage tests on stored values" or "a projection of the arity-3 slice of the link store."

### Issue 4: Precedent-defense meta-prose accreted around FL-WP
**ASN-0121, "The only result-changing transition" / FL-WP**:
- "(For the bare, unfiltered existence query, ASN-0127's F-LAMBDA already characterises the K.λ step — … the cases below refine that per-step increment through the four-slot `sat` and the addressability filter, neither of which F-LAMBDA carries.)"
- Case (a): "This is the direct analogue of the third conjunct ASN-0086 deliberately carries in its wp Case 2 (EmitKWeakestPrecondition), `¬(E (b, F', G') ∈ L_R^Σ :: a_emit(Σ, d) ∈ coverage(G'))`, and for the same reason —"
- "The second case is not idle: …"
- Scope note: "(cf. LP12a, ASN-0098; wp Case 2, ASN-0086)"

**Problem**: These passages justify the section's existence and its parentage rather than advance the derivation: why FL-WP is not redundant with F-LAMBDA, that ASN-0086 "deliberately carries" the same conjunct, that case (b) is "not idle." The reader must skip past them to follow the wp derivations, which are complete without them. The load-bearing content nearby is different and should stay: (i) the scoping fact that this ASN works over the full ASN-0047 vocabulary with no retraction discipline, so the addressability conjunct is not dischargeable; (ii) the Nelson grounding that retraction links are first-class searchable, which fixes case (b)'s semantics.
**Required**: Cut the F-LAMBDA positioning parenthetical, the "direct analogue … deliberately carries … for the same reason" framing, the "not idle" defense, and the `cf.` citation; retain the no-discipline scoping sentence and the first-class-searchability grounding as plain statements.

### Issue 5: FL-CUR is a fourth label on the same set equality
**ASN-0121, "The result is a current snapshot"**: "The biconditional is FL-DEF restated as a membership test — FL-SND forward, FL-CMP backward."
**Problem**: The paragraph confesses its own redundancy. FL-DEF, FL-SND, FL-CMP, and FL-CUR are four named claims for one set equality: FL-SND and FL-CMP are the two demands that force FL-DEF, and FL-CUR is exactly their conjunction, restated. The remainder of the FL-CUR paragraph is forward pointers (to the K.λ analysis, R6a, FL-JUNK); the subsection's only new content is FL-MON. This is the duplicate-paragraph pattern: two places in the document saying the same thing in different words, with the duplicate promoted to a claims-table row that downstream readers must reconcile with FL-DEF.
**Required**: Fold the currency reading into FL-DEF's section (a sentence noting the snapshot interpretation suffices) and remove FL-CUR as a separate claim, or give FL-CUR content distinct from FL-SND ∧ FL-CMP. The "Two stability facts" lead-in and FL-MON stand on their own.

## OUT_OF_SCOPE

### Topic 1: Result ordering and enumeration
Nelson's text says the operation "returns a list"; the ASN specifies a set. Whether and how results are ordered or enumerated is unaddressed.
**Why out of scope**: Enumeration order and incremental delivery belong with the paginated retrieval operation (FINDNEXTNLINKSFROMTOTHREE), which is explicitly outside this ASN's scope; set semantics is the right abstraction for the one-shot query.

### Topic 2: Requests constraining endsets beyond the third
Higher-arity links are matched on their first three slots, but no request form constrains `e₄ … eₙ`, though Nelson (4/79) calls for n-set support in link *search* as well as storage.
**Why out of scope**: The operation specified is FROMTOTHREE by name and contract; an n-slot request grammar is a future operation, not an error here.

VERDICT: REVISE
