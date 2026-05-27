# Review of ASN-0099

## REVISE

### Issue 1: F4 missing from numbering

**ASN-0099, Claims Introduced table and body text**: Claims numbered F1, F2, F3, F5, F6, ..., F20 — F4 is absent.

**Problem**: The numbering jumps from F3 (Soundness) directly to F5 (IdentityNotValue) without an F4. The Claims Introduced table at the end also omits F4. Downstream ASNs that reference these claims would have no target for "F4". This is either a labeling artifact from a dropped claim or an oversight in renumbering.

**Required**: Either (a) restore F4 with a labeled claim if one was intended (perhaps an explicit "result equality" or "set-uniqueness" claim derived from F2 ∧ F3), or (b) renumber F5–F20 to close the gap so the claim sequence is contiguous F1–F19. Either way, the Claims Introduced table must agree with the body text.

### Issue 2: Worked example does not exercise cross-document T1 case (ii)

**ASN-0099, F10 derivation and Worked Example**: F10's derivation handles both T1 case (i) (component divergence) and T1 case (ii) (version-extension via K.δ at k=1, where `d₁ ≺ d₂`) for the cross-document T1 ordering of link anchors. The Worked Example uses `d_a` and `d_b` as siblings under a single account (Case (i)).

**Problem**: The version-extension case is treated only theoretically. Since K.δ at k=1 creates a version `d_new = inc(d_src, 1)` with `d_src ≺ d_new` — exactly the T1 case (ii) shape — and since this is the routine ordering relationship between a document and its versions, a corpus with version chains will exercise this case constantly. The example's "we assume d_a was allocated before d_b under the same account" sidesteps the version case entirely.

**Required**: Either extend the Worked Example with a third document `d_c = inc(d_a, 1)` (a version of `d_a`) with its own link `ℓ''`, and verify F10 places `ℓ` before `ℓ''` under T1 via the appended-zero argument at position `#d_a + 1` — or explicitly justify in F10's prose why exercising Case (i) suffices to demonstrate the lemma's correctness across both cases.

### Issue 3: F9-cor's coverage of K.δ-IsDocument is not made explicit

**ASN-0099, F9-cor derivation**: "K.σ, K.α, K.δ, K.μ~, and K.μ⁺_L each name `L' = L` directly in the published frame; K.μ⁺, K.μ⁻, and K.ρ omit `L` from the published frame..."

**Problem**: K.δ has three sub-cases (IsNode, IsAccount, IsDocument), each with potentially distinct frame consequences for `M`. ASN-0047's K.δ frame lists `C' = C; L' = L; R' = R` uniformly, but the K.δ-IsDocument sub-case also affects `M(d_new)` (sets it to ∅). The derivation lumps K.δ as a single case without addressing whether the IsDocument variant's M-modification might affect `findlinks` via the V-side. For F9-cor's conclusion `findlinks(I, Σ) = findlinks(I, Σ')` this is fine because `findlinks` (without the V prefix) consults only `Σ.L`, but the bookkeeping should be explicit.

**Required**: In F9-cor's derivation, add one sentence clarifying that even at the K.δ-IsDocument sub-case where `M'(d_new) = ∅` introduces a new document with empty arrangement, `findlinks(I, Σ)` is unaffected because the comprehension consults only `dom(Σ.L)` and the link values, not `Σ.M`. (The companion LP8 from ASN-0098 already discharges the V-side, but F9-cor should not silently rely on this.)

### Issue 4: F1's "design constraint on conforming implementations" is normative content without numbered status

**ASN-0099, "The Match Predicate" section**: "F1's slot-existential together with its intersection (rather than containment) form is exactly the minimal sufficient match condition... We surface it here as a *design constraint on conforming implementations*: the match cannot require full overlap, near-overlap, majority overlap, or any other strengthened condition on either side."

**Problem**: This is a substantive normative claim — that no strengthening of the match predicate is permitted — but it has no claim label and is buried in prose. The Claims Introduced table does not list it. Downstream conformance arguments would need to reference this constraint, but there is no handle to cite. This is a precise companion to F2 ∧ F3 (which pin `result` to `findlinks`) but stronger: it forbids alternative match formulas, not just non-conforming outputs against the chosen formula.

**Required**: Either elevate this to a labeled claim (e.g., "F4: MatchFormulaUniqueness") with explicit statement and derivation, or fold the constraint into F2/F3's "single conforming output set" prose so the absence of a separate label is clear. If labeled, this could absorb the missing F4 slot.

### Issue 5: A1's vocabulary-closure clause is brittle under future revision

**ASN-0099, A1 (EffectClauseExhaustivity)**: "Vocabulary closure (scope of the contract): The operation vocabulary of the substrate is exactly the published set V = {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ} as enumerated across ASN-0047 and ASN-0093 at the time this ASN was written. No operation outside V exists in the substrate."

**Problem**: The "at the time this ASN was written" clause makes A1 frozen against substrate evolution. If ASN-0047 or ASN-0093 is later revised to add an operation, A1 — by its own text — does not apply to the new operation, and a hostile reading would say the new operation may modify `Σ.L` arbitrarily without violating A1. The ASN's own text under "Second, A1 propagates as a binding obligation on any future revision" attempts to address this, but the vocabulary-closure clause directly contradicts the propagation clause.

**Required**: Either remove the "at the time this ASN was written" temporal qualifier (so A1 binds the substrate's current vocabulary whatever it may be), or strengthen the propagation clause to override the closure clause explicitly: "If V is extended by future revision, A1's exhaustivity obligation applies to every operation in the revised vocabulary; the listed set in this clause is illustrative, not constraining."

### Issue 6: F11's value-equality vs. tuple-component step is glossed

**ASN-0099, F11 derivation**: "Component-wise tuple equality on `Link` values (L6, ASN-0043) extracts per-slot endset equality from value equality: `|Σ.L(a)| = |Σ'.L(a)|` (so the slot-range of the match predicate's existential is the same at the two states) and `Σ.L(a).eᵢ = Σ'.L(a).eᵢ` for every `i ∈ {1, …, |Σ.L(a)|}`."

**Problem**: L6 in ASN-0043 establishes that the positional accessor `Σ.L(a).eᵢ` is a primitive of the model and that link equality is component-wise tuple equality. But the inference from `Σ'.L(a) = Σ.L(a)` (a value equality) to "arity equality plus per-slot endset equality" requires the further premise that arity `|·|` is determined by the tuple length, which is structural for `Link = {(e₁, …, eₙ) : N ≥ 3, ...}`. This is true but not made explicit. A reader unfamiliar with the encoding might wonder whether arity could differ while values are "equal" under some looser notion.

**Required**: One additional sentence in F11's derivation explicitly noting that the `Link` carrier is a finite sequence under L3, so `|·|` is determined by the underlying sequence length, and thus `Σ'.L(a) = Σ.L(a)` forces `|Σ'.L(a)| = |Σ.L(a)|` and `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` for `i` in the shared (equal) range.

## OUT_OF_SCOPE

### Topic 1: Behavior with addresses outside `dom(Σ.C) ∪ dom(Σ.L)`

**Why out of scope**: The ASN explicitly lists this as an Open Question. The match predicate is mechanically well-defined for any `I ⊆ T`, but the operational meaning of querying with addresses that don't currently host content or links is a separate question — belongs to a future ASN that addresses pre-allocation reservations or query semantics for phantom addresses.

### Topic 2: Multi-instance / partition tolerance

**Why out of scope**: Explicitly deferred via Open Question. The single-state determinism (F8) and the single-state atomicity discussion are correctly scoped to a single logical state. Replication consistency, partition tolerance, and inter-server protocols are downstream concerns.

### Topic 3: Access control composition

**Why out of scope**: The ASN correctly identifies access control as an orthogonal scope filter (composable with `findlinks_scoped`) rather than altering match semantics. Formalizing access control predicates and their interaction with completeness obligations is genuinely a future ASN's territory.

### Topic 4: Latency bounds and indexing strategies

**Why out of scope**: The ASN deliberately specifies the result set rather than the procedure. Latency guarantees, index maintenance protocols, and B-tree / inverted-index strategies are implementation concerns that any conforming implementation may resolve differently while satisfying F2 ∧ F3.

### Topic 5: Inverse direction (FOLLOWLINK / RETRIEVEENDSETS)

**Why out of scope**: Once links are found, resolving their endsets back to V-positions in target documents is the inverse direction and has its own subtleties (handling I-addresses not currently arranged anywhere). This is correctly noted as a separate operation's specification.

VERDICT: REVISE
