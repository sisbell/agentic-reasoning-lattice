# Review of ASN-0036

## REVISE

### Issue 1: `δ` overloaded against foundation notation
**ASN-0036, S7c / subspace_I / ShiftPreservation / S8 corollary**: S7c writes "the content ordinal `[E(a)₂, ..., E(a)_δ]`" and "Gregory's evidence confirms `δ = 2`"; ShiftPreservation opens "Let `δ = #E(a)`" and three sentences later invokes "the displacement `δ(k, #a) = [0, …, 0, k]`"; S8's corollary uses "`#E(aⱼ) = δⱼ ≥ 2`."
**Problem**: ASN-0034 reserves `δ` for `OrdinalDisplacement` — the function `δ(n, m)`. This ASN simultaneously uses bare `δ` (and subscripted `δⱼ`) as a *scalar* denoting element-field depth `#E(a)`. In the ShiftPreservation proof both meanings appear within a few lines: `δ` the number and `δ(k, #a)` the displacement. A reader cannot disambiguate by symbol alone. Standard 7 forbids reinventing/colliding with foundation notation.
**Required**: Rename the element-field-depth scalar (e.g., `δ_E` or `ℓ_E`, or just write `#E(a)` / `#E(aⱼ)` everywhere) and reserve `δ(·,·)` exclusively for the foundation's ordinal displacement.

### Issue 2: `w_ord` cites the wrong (and omits the right) dependency
**ASN-0036, w_ord (OrdinalDisplacementProjection), Depends**: "`TumblerAdd (ASN-0034) — for the actionPoint relationship`."
**Problem**: The postcondition `actionPoint(w_ord) = actionPoint(w) − 1` is established purely from `ActionPoint`'s definition applied to the index-shifted sequence `(w_ord)ⱼ = w_{j+1}` — TumblerAdd plays no role. Worse, `ActionPoint` does not appear in `w_ord`'s Depends list at all, even though the postcondition rests on it.
**Required**: Replace the TumblerAdd citation with `ActionPoint (ASN-0034)`; remove TumblerAdd from `w_ord`'s Depends unless another postcondition actually uses it.

### Issue 3: S9 is S0 restated; its proof says so
**ASN-0036, S9 proof**: "S9 carries no formal content beyond S0: its consequent is verbatim S0's, and its antecedent ... merely restricts S0's universal quantification ... to the arrangement-modifying ones."
**Problem**: This is the `review-mode.anti-bloat` pattern of two passages saying the same thing in different words. The proof spends a paragraph conceding the claim adds nothing formal, then re-derives it trivially. The directional *reading* ("arrangement edits cannot reach into C") is worth one sentence; the surrounding apparatus (separate Formal Contract, Depends, "a fortiori" derivation) is meta-prose around a non-claim.
**Required**: Collapse S9 to a one-line named corollary of S0 (the directional reading), and delete the proof's self-referential commentary about its own lack of content.

### Issue 4: Protocol rationale embedded in the S3 axiom slot
**ASN-0036, S3 Formal Contract, Axiom**: "Nelson asserts the canonical-order mandate ... Changes are 'instantaneous' [LM 1/34] and the system is defined by the commands to which it responds [LM 4/61], so the invariant is asserted of the quiescent states between operations, not of any mid-operation interior — which lies outside Nelson's observable model."
**Problem**: This is rationale explaining *when/why* the invariant is asserted rather than stating the invariant. It is the "Protocol rationale in a structural slot" pattern the anti-bloat classifier asks to surface. The same "quiescent states between operations" point is then re-raised as an Open Question, so the prose is also a duplicated forward defer.
**Required**: Reduce the axiom to its formal statement; move any genuinely needed quiescence caveat to a single location (the Open Question already present).

### Issue 5: Repeated boilerplate Depends clause
**ASN-0036, S7a, S7b, S7c, subspace_I, ShiftPreservation, S7**: each Depends list repeats verbatim "`S0 (content immutability) — fixes a's components, so allocation-time structure persists`."
**Problem**: Six identical justification clauses. The fact that S0 freezes a tumbler's components is stated once and then copied; it does not advance any of the individual contracts. This is accumulated meta-prose the precise reader must skip past.
**Required**: State the S0-fixes-components consequence once (e.g., at S7b where the element-level structure is first pinned) and cite it by reference, or drop the clause from the contracts where it is mere boilerplate.

### Issue 6: State-component "proofs" are modeling rationale ending in ∎
**ASN-0036, Σ.C and Σ.M(d) justification paragraphs**: "Σ.C is a definition, not a derived property. We justify the modelling choice. ... The content store is the first of two state components ... ∎"
**Problem**: These paragraphs explain *why a partial function is the natural object* — modeling rationale — yet close with ∎ as though a theorem were proved. Nothing is derived. The "explains why X is needed rather than what it says" pattern, dressed as a proof.
**Required**: Drop the ∎ and the "we justify the modelling choice" framing; keep only the definitional statement plus, at most, a one-line note that these are axiomatic state components.

## OUT_OF_SCOPE

### Topic 1: ValidInsertionPosition / ValidFirstInsertionPosition as INSERT scaffolding
**Why out of scope**: These predicates characterize where INSERT may legally place content and where the first position of an empty subspace lands — operation preconditions for INSERT. The scope list excludes "operation-specific effects (INSERT ... frame conditions and postconditions)." The ASN itself defers the operative content to Open Questions ("What invariants must the displacement mechanism satisfy so that insertion at a ValidInsertionPosition preserves D-CTG..."). The structural predicate is defensible as state-derived, but the depth-choice discussion ("Basic INSERT typically commits to m = 2") is INSERT-operation territory and belongs in the operations ASN, not here.

### Topic 2: Link-subspace contiguity semantics
**Why out of scope**: Correctly deferred. Note, however, that the deferral is repeated across the Arrangement-contiguity preamble, the S8a Remark, and the Open Questions — three passages pointing to the same future ASN. Consolidating to one defer would remove the forward-reference accretion the classifier flags, without changing scope.

VERDICT: REVISE
