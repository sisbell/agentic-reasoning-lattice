# Review of ASN-0082

## REVISE

### Issue 1: S8a restated incorrectly from foundation

**ASN-0082, Foundation Invariants**: "S8a — VPositionWellFormedness (cited, ASN-0036). `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`"

**Problem**: The foundation S8a in ASN-0036 reads `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`. The cited version drops the `#v ≥ 2` clause entirely and replaces componentwise positivity with the weaker `v > 0` (tumbler ordering). The `#v ≥ 2` clause is load-bearing — without it, the subspace-preservation argument at `m = 1` would fail to be excluded by S8a, requiring it to be excluded only by operation precondition.

**Required**: Restate S8a faithfully from ASN-0036, or cite without restating.

### Issue 2: Redundant redefinition of ord, vpos, w_ord

**ASN-0082, Ordinal Extraction section**: introduces `ord(v)`, `vpos(S, o)`, `w_ord` with full definitions, marked "(introduced)" in the statement registry.

**Problem**: ASN-0036 already defines all three (OrdinalExtraction, VPositionReconstruction, OrdinalDisplacementProjection). Per Standard 7, foundation definitions must be cited rather than reinvented. The shared vocabulary confirms these are in ASN-0036.

**Required**: Cite the ASN-0036 definitions. Retain only the order-equivalence postcondition `v₁ < v₂ ⟺ ord(v₁) < ord(v₂)` as a derived property — that part is new and useful.

### Issue 3: Redundant lemma OrdinalAdditiveCompatibility

**ASN-0082, Ordinal Extraction**: "Lemma — OrdinalAdditiveCompatibility. ... ord(p ⊕ w) = ord(p) ⊕ w_ord"

**Problem**: This is exactly postcondition (a) of OrdAddHom (OrdinalAdditionHomomorphism) in ASN-0036, with identical preconditions (`#p = m ≥ 2`, `w₁ = 0`, `#w = m`, `Pos(w)` ≡ `w > 0`). The ASN reproves it from scratch. OrdAddHom additionally gives (b) `subspace(v ⊕ w) = subspace(v)` and (c) the vpos reconstruction identity, both of which the ASN uses implicitly.

**Required**: Cite OrdAddHom from ASN-0036. The full three-part contract simplifies several downstream arguments (subspace preservation in I3-VP, V-position reconstruction in D-SHIFT).

### Issue 4: Asymmetry in depth coverage between insertion and contraction

**ASN-0082, Post-Contraction Shift**: "Throughout this section, V-positions have depth #p = 2 (ordinal depth 1). This restricts the analysis to single-component ordinals, where TA4's zero-prefix condition is vacuously satisfied and TA3-strict's equal-length precondition holds trivially."

**Problem**: I3 (insertion) is proved at arbitrary `m ≥ 2`, but contraction is restricted to `m = 2`. The two operations are structurally dual; the asymmetry is unmotivated beyond "TA4's zero-prefix condition is vacuously satisfied at depth 1." TA4's actual precondition `(A i : 1 ≤ i < k : aᵢ = 0)` is satisfied for `a = ord(p)` at any depth iff `ord(p)` has zeros at positions 1 through k−1, where k = actionPoint(w_ord). For contraction widths that act only at the deepest position (the natural analogue of ordinal-level spans in I3-S), this holds vacuously at any depth — not just at depth 1.

**Required**: Either generalize the contraction analysis to arbitrary `m ≥ 2` for ordinal-level widths (where actionPoint(w_ord) = #ord(p)), matching the scope of I3, or justify why the asymmetry is intentional. The current scoping axiom appears to be a conservative restriction rather than a structural necessity.

### Issue 5: Postcondition vs lemma labeling inconsistency

**ASN-0082, Structural preservation**: I3-VD, I3-VP, I3-S3, I3-S2, I3-fin are labeled "(POSTCONDITION, introduced)" but each is followed by a proof from other postconditions and foundation invariants.

**Problem**: A statement that is asserted as part of an operation's contract is a postcondition; a statement proved from other postconditions is a derived lemma. The current labeling conflates these. By contrast, the contraction section labels structurally identical statements (S2-post, S3-post, D-CTG-post, etc.) as "(LEMMA, introduced)" — the correct categorization.

**Required**: Re-label I3-VD, I3-VP, I3-S3, I3-S2, I3-fin as `(LEMMA, derived)` or `(LEMMA, introduced)` to match the contraction-section convention and reflect that they are proved from I3, I3-L, I3-X, I3-D, I3-V, I3-C, I3-CS, I3-CX.

### Issue 6: D-DOM closure direction not derived

**ASN-0082, Post-Contraction**: D-DOM `{v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ Q₃` is listed as a postcondition.

**Problem**: For insertion, the equivalent closure facts I3-CS and I3-CX are explicitly justified with the note that "without these clauses, the assignment and vacating postconditions constrain only positions that were in dom(M(d)) — an M'(d) satisfying them could contain additional positions at arbitrary depth, leaving dom(M'(d)) underdetermined." D-DOM serves the same role for contraction but is presented without this justification.

**Required**: Add a parallel justification for D-DOM, paralleling I3-CS/I3-CX in the insertion section, so the reader can see why D-L + D-SHIFT alone do not suffice.

### Issue 7: I3-VP appeals to "all components positive" without restating it

**ASN-0082, I3-VP proof**: "shift copies positions 1 through m − 1 from v (all nonzero by S8a on M(d))"

**Problem**: The ASN's own restated S8a (Issue 1) does not include "all components nonzero" — it has `zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0`. The proof appeals to "all nonzero by S8a" — a property that follows from `zeros(v) = 0` plus typing, but the chain is not stated. With the foundation S8a correctly cited (Issue 1 fix), this becomes direct.

**Required**: Either (a) fix Issue 1 so the citation supplies the property directly, or (b) explicitly derive componentwise positivity from `zeros(v) = 0` plus ℕ-typing of components in the proof.

## OUT_OF_SCOPE

### Topic 1: Spans straddling the insertion point
**Why out of scope**: I3-S addresses spans entirely in the shifted region (s ≥ p). A span with start(σ) < p and reach(σ) > p would fragment under shift. This is properly the concern of an INSERT operation that composes the shift with span-tracking logic, not the shift itself.

### Topic 2: Deeper-ordinal generalization for contraction
**Why out of scope**: Explicitly noted as an open question. Generalization requires showing TA4's zero-prefix condition and TA3-strict's equal-length precondition hold for the appropriate width class at deeper ordinals — non-trivial new analysis.

### Topic 3: Composite INSERT/DELETE operations
**Why out of scope**: This ASN specifies the shift component of insertion and contraction. Content allocation (extending dom(C)) and span placement are deferred to operation-level ASNs that compose these shifts with allocation logic.

VERDICT: REVISE
