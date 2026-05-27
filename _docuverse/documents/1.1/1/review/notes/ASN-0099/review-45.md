# Review of ASN-0099

## REVISE

### Issue 1: F4's spans-monotonicity prose conflates two distinct failure modes

**ASN-0099, F4 (MatchFormulaDesignJustification), "Structural consequence of Layer 2"**: "Predicates that fold the spans of an endset into a universal or aggregate constraint (containment `coverage(eᵢ) ⊆ I`, reverse containment, quantitative thresholds) break this monotonicity: adding a non-witnessing span can violate the universal or fail to advance the aggregate."

**Problem**: The claim that all three alternatives "break this monotonicity" is imprecise. Spans-monotonicity is introduced as the property that "adding a non-witnessing span to an endset that already has a witnessing span cannot suppress the existing witness — the existential survives." Under this definition:

- *Containment* `coverage(eᵢ) ⊆ I` genuinely breaks it: adding a non-conforming span (outside I) violates the per-span universal, losing the satisfying state.
- *Reverse containment* `I ⊆ coverage(eᵢ)`: adding a span enlarges coverage; if `I ⊆ coverage` held before, it still holds after. Witness preservation is maintained — the predicate is in fact monotone in spans.
- *Cardinality threshold* `|coverage ∩ I| ≥ k`: adding a span can only grow `|coverage ∩ I|` (or leave it unchanged); existing satisfaction is preserved. Also monotone.

The text uses "violate the universal or fail to advance the aggregate" to gesture at two failure modes, but "fail to advance" is not a violation of monotonicity — it is a separate property (whether non-witnessing spans help). Reverse containment and cardinality preserve witnesses; only containment loses them.

**Required**: Tighten the discussion to (a) restrict the spans-monotonicity violation claim to containment alone, and (b) reframe the distinguishing property between F1 and aggregates more precisely (F1 is a per-span existential; reverse containment / cardinality are aggregates with different compositional semantics — neither lose witnesses, but neither admits the per-span witness structure that makes F1 robust to adversarial junk-span insertion). The load-bearing operational distinguishability claim — anchored by the realizability witnesses — is not affected; this is a precision issue in supplementary rationale.

### Issue 2: Strengthening 3's witness construction is underspecified

**ASN-0099, F4 realizability discharge, *Strengthening 3***: "Witness: link `a` with one canonical span `(α, δ(1, #α))` at some slot (other slots arbitrary; the link-level existential `(E i : |coverage(eᵢ) ∩ I| ≥ k)` for `k > 1` fails on empty slots since `|∅ ∩ I| = 0 < k`)."

**Problem**: "Other slots arbitrary" is too loose. The argument requires that no other slot also satisfy the cardinality threshold, but does not constrain the construction to ensure this. If "other slots arbitrary" admits a slot whose coverage happens to have `≥ k` elements in `I`, the strengthening would admit the link via that slot, and the distinction from F1 would not be witnessed by this construction.

The parenthetical about empty slots covers the empty case but not the "non-empty with large overlap" case. Strengthenings 1 and 2 are explicit about avoiding analogous loopholes (Strengthening 1 says "Populating all three slots is essential"; Strengthening 2 says "Placing the witness at slot 3 is essential"); Strengthening 3 deserves the same explicit construction.

**Required**: Restate the witness as "witness at slot 3 carrying `(α, δ(1, #α))` (satisfying L3's non-empty requirement); slots 1 and 2 empty (admissible by L3 for non-type slots, with `|∅ ∩ I| = 0 < k`)". This pins down a concrete construction where the strengthening rejects on every slot.

### Issue 3: F4 marks F12 as both definition and citation handle without clearly distinguishing the dual role

**ASN-0099, F12 (TwoPhaseFactoring)**: "F12 (TwoPhaseFactoring) — DEFINITION of findlinks_V: ... F12 is a definition; the 'F12' label is a citation handle so downstream derivations can name the definitional unfolding."

**Problem**: This dual labeling — F12 as both the definition of `findlinks_V` and a citation handle for "the definitional unfolding equation" — creates ambiguity when downstream claims cite "F12". The Claims Introduced table compounds this: it lists `findlinks_V(R, d, Σ)` as a "definition" referring to F12, and separately lists F12 as "TwoPhaseFactoring: `findlinks_V` definitional unfolding | definition". The two table entries appear to refer to the same object via different names.

In the worked example (Query 1), the text says "By F12, both V-side queries unfold to findlinks({α}, Σ)" — this is the definitional unfolding usage. But F12 is also the operation definition itself. Citations elsewhere should distinguish whether they invoke the operation's existence or the unfolding identity.

**Required**: Either (a) separate the operation definition from the unfolding lemma into two distinct labels (e.g., a "Definition — findlinks_V" entry without an F-label, and "F12 (TwoPhaseFactoring)" as the unfolding identity), or (b) explicitly note in the Claims table that the `findlinks_V` row and F12 row refer to the same artifact under two labels for two purposes.

### Issue 4: Coverage definition restated rather than imported

**ASN-0099, "Definition — Coverage"**: The coverage definition is restated verbatim from ASN-0043 ("Definition — Coverage"), with the same notation.

**Problem**: While restating is permitted by the convention ("ASNs may use foundation definitions without restating them"), restating verbatim creates drift risk: if the foundation definition is later refined, this ASN's copy will not automatically update. The restatement adds rationale ("Coverage is a purely combinatorial property...") that goes beyond pure citation but doesn't redefine the operator.

**Required**: Either cite ASN-0043's definition by reference (e.g., "coverage(e) as defined in ASN-0043") without restating, or explicitly mark the restatement as a convenience reproduction and commit to keeping it synchronized with the foundation. The current presentation reads as if ASN-0099 is introducing the definition, which it isn't.

## OUT_OF_SCOPE

None. The ASN stays within FINDLINKS scope and properly references substrate operations (K.σ, K.α, K.λ, K.δ, K.μ-family, K.ρ) from foundation ASNs without re-specifying their mechanics. The "Open Questions" section identifies future work (multi-instance/replication, access control, FOLLOWLINK inverse, audit witnesses, timing bounds) without claiming results in those areas.

VERDICT: REVISE
