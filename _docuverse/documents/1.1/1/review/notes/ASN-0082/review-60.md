# Review of ASN-0082

The arrangement-layer mathematics here is sound. I checked the displacement algebra (OrdAddHom, OrdinalExceedsDisplacement, the TA4/ReverseInverse round-trips), the three-region partition, gap-closure (D-SEP), and the invariant-preservation lemmas against the foundation contracts and the worked examples; the chains discharge correctly, the boundary cases (L=∅, R=∅, full deletion, insert-at-start/end, empty document) are covered, and the depth-1 ℕ-subtraction identity in D-S is properly reduced to ReverseInverse + TA4 rather than hand-waved. No correctness defect found.

This note carries `review-mode.anti-bloat`. The remaining issues are accreted meta-prose: justification in structural slots, duplicated passages, and prose imagining excluded cases.

## REVISE

### Issue 1: Justification embedded in a postcondition slot (D-SEP)
**ASN-0082, D-SEP postcondition (b)**: "by D-CTG, r = min(R) — the last element of X and some v ∈ R bracket r in V_1(d), so contiguity forces r ∈ V_1(d). Then σ(r) is well-defined and ord(σ(r)) = ord(p)..."
**Problem**: The postcondition slot states a claim; here it carries its own proof sketch ("the last element of X and some v ∈ R bracket r... so contiguity forces..."). That argument is then given again, in full, in *Proof of (b)* directly below. The reader must reconcile the inline sketch against the real proof. This is essay content in a structural slot duplicating downstream work.
**Required**: Reduce (b) to the bare claim (e.g. "When R ≠ ∅: r ∈ V_1(d), r = min(R), and ord(σ(r)) = ord(p)"); leave the bracketing/contiguity argument to the proof.

### Issue 2: wp prose imagines preconditions the carrier already supplies
**ASN-0082, Weakest-precondition analysis (I3-VP), conjunct 1**: "The wp pinpoints why I3 needs `v ∈ dom(M(d))` (already given by the quantifier in I3): without that membership we would have no S8a hypothesis on v and the wp obligation would be open."
**Problem**: The clause parenthetically concedes the precondition is already given, then spends a sentence imagining its absence. The same pattern recurs in the S8a-post wp analysis conjunct 3, which imagines `#p > 2` — a case the depth scoping axiom `#p = 2` excludes — to explain why the restriction exists. Imagining a case the carrier/precondition already rules out is noise the reader skips past.
**Required**: State the discharge directly ("conjunct 1 is S8a on v, supplied by `v ∈ dom(M(d))`"). The genuine design insight in conjunct 3 (why depth-1 is required) belongs in the Open Questions item on depth generalization, not inside the wp walk-through.

### Issue 3: Duplicated cross-subspace closing prose
**ASN-0082, insertion worked example**: "The link-subspace positions, having subspace identifier 2 ≠ 1, lie outside the quantifier ranges of I3 and I3-V, so the sparse V_2(d) with its tombstone gap is unaffected by the text-subspace insertion."
**ASN-0082, contraction worked example**: "The link-subspace positions, having subspace identifier 2 ≠ 1, lie outside the quantifier ranges of D-SHIFT and D-L; D-CS pins both their position set and their I-address mappings to the pre-state."
**Problem**: Two paragraphs in the same document say the same thing in different words (plus the matched table-prefix "Cross-subspace preservation: text {insertion,contraction} leaves link subspace untouched" and the repeated "tombstone gap remains" remarks). The verification tables already show the link rows unchanged.
**Required**: Keep one statement of the cross-subspace invariance principle; let the second example's table stand on its own.

### Issue 4: Scope paragraphs explain rationale rather than state the operation
**ASN-0082, contraction Scope**: "Unlike the insertion shift sub-operation — which opens a gap that a composing INSERT must later fill — contraction is a *complete V-arrangement transformation* of DELETE: it removes the deleted range, slides the right region back, re-establishes the foundation's contiguity invariants, and requires no composing operation."
**Problem**: The contrast against insertion and the "requires no composing operation" justification is rationale about document structure, not a statement of what contraction does. The object-level content (contraction modifies only M(d), C unchanged) is already recorded at D-I. The parallel insertion Scope paragraph mixes one rationale sentence ("not the full INSERT operation") with its object content.
**Required**: Reduce each Scope note to its object-level content (what the sub-operation transforms, what it leaves fixed). Drop the insertion-vs-contraction contrast.

### Issue 5: D-SHIFT prose restates the postcondition
**ASN-0082, after D-SHIFT**: "What the shift preserves and changes: D-SHIFT changes the V-ordinal of each right-region position but preserves the I-address. The position in the permanent content store is unchanged; the position in the document's arrangement shifts to close the gap."
**Problem**: D-SHIFT (`M'(d)(σ(v)) = M(d)(v)`) already says exactly this — same I-address, shifted V-position. The paragraph re-narrates the postcondition before adding the Nelson quote. The matching I3 paragraph ("The I-address is unchanged — only the V-position moves") does the same on the insertion side.
**Required**: Drop the restatement; if the Nelson grounding is wanted, attach the quote to the postcondition in one line rather than re-deriving the postcondition in prose.

## OUT_OF_SCOPE

### Topic 1: NAT-CA (ℕ commutativity/associativity) belongs in the foundation
**ASN-0082, Ordinal Shift**: "NAT-CA — *CarrierAdditionCommutativityAssociativity* (introduced locally)."
**Why out of scope**: The introduction and its uses (I3-S, D-S) are correct, and the foundation's extracted NAT-* axioms (NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder) genuinely omit commutativity and associativity — so this is not reinvention of an existing foundation fact. But a fundamental ℕ-arithmetic axiom is foundation territory (ASN-0034), not strand-projection territory. Adding it to ASN-0034's NAT-* set is a foundation revision, not a defect in this ASN.

### Topic 2: Depth-generalization of D-SEP/D-DP
**Why out of scope**: Already correctly recorded as an Open Question. The depth scoping axiom `#p = 2` is load-bearing (TA4's zero-prefix precondition conflicts with S8a positivity at intermediate components); generalizing to deeper ordinals is future work, not a gap in the present claims.

VERDICT: REVISE
