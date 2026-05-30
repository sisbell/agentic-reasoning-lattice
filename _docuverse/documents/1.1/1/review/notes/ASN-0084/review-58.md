# Review of ASN-0084

## REVISE

### Issue 1: Dangling reference to a nonexistent "OrdinalShift consumers list"
**ASN-0084, R-COMM proof, 3-cut α case**: "Also π(v) + k = (c₀ + w_β + j') + k = c₀ + w_β + (j' + k) by associativity (Extended Associativity, **recorded in the OrdinalShift consumers list**)."
**Problem**: No "OrdinalShift consumers list" is defined anywhere in this ASN. The annotation appears in exactly one of the seven R-COMM cases; the other six say only "by associativity." It is a dangling pointer the reader must chase and cannot resolve — noise to work around, not reasoning. (The associativity it invokes is just Extended Associativity, already stated.)
**Required**: Delete the parenthetical "recorded in the OrdinalShift consumers list"; cite "Extended Associativity" alone, consistently with the other R-COMM cases.

### Issue 2: Use-site inventory in the Extended Associativity paragraph
**ASN-0084, Extended Associativity**: "The same identity convention extends OrdShiftHom (a) ... to n = 0, since shift(v, 0) = v; **this n = 0 case is the one consumed in Subspace confinement and R-COMM**."
**Problem**: The trailing clause enumerates downstream consumers rather than advancing the definition's meaning — the flagged "definition's introduction enumerates downstream consumers" pattern. The fact that shift(v,0)=v extends OrdShiftHom (a) to n=0 stands on its own; naming the two later sites adds nothing the reader needs at the point of definition.
**Required**: End the sentence at "since shift(v, 0) = v." Drop the consumer list.

### Issue 3: Same foundation-S8 deferral restated across three sections
**ASN-0084, Canonical decomposition / R-BLK / R-SP**: "Existence and uniqueness of this maximal-run partition are exported directly by the foundation: S8..."; "The S8-unique maximal partition of M'(d) is guaranteed to exist by the foundation (S8, ASN-0036)."; "Existence and uniqueness of the maximal decomposition of M'(d) hold by foundation S8..."
**Problem**: Three different sections defer the same maximality claim to the same downstream location (foundation S8), each accompanied by the same caveat that B' is non-maximal. This is the flagged "multiple paragraphs in different sections defer to the same downstream location" pattern; the repetition compounds without adding argument.
**Required**: State the foundation-S8 maximality transport once (in R-SP, where S8 is discharged) and have the other sites reference that discharge rather than re-deriving it.

### Issue 4: Structural-slot justification in Displacement Analysis
**ASN-0084, Displacement Analysis, opening**: "We record the displacement structure **as a remark rather than elevating it to a lemma**, and we introduce no signed-magnitude carrier..."
**Problem**: Prose justifying the structural slot (remark vs. lemma) and a format choice (no signed carrier) is meta-commentary, not content. The displacement directions/distances can be read straight off the formulas without the editorial framing.
**Required**: Open directly with the per-region displacement statement; drop the slot/format justification.

### Issue 5: Redundant "Concrete witnesses" in Width positivity
**ASN-0084, Consequences of R-PRE, Width positivity**: Step 2 already establishes "the count of V-positions in [c_i, c_{i+1}) ... equals ord(c_{i+1}) − ord(c_i) ≥ 1," which is the width-positivity conclusion. The subsequent "*Concrete witnesses*" paragraph then separately shows c_i ∈ [c_i, c_{i+1}) ∩ V_S(d) ≠ ∅.
**Problem**: Nonemptiness is strictly weaker than "count ≥ 1," which Step 1+2 already give. The Concrete-witnesses paragraph re-proves an implied sub-fact in different words — the flagged "two paragraphs say the same thing in different words" pattern.
**Required**: Either drop the Concrete-witnesses paragraph or fold its instantiation (i=0, i=1, i=n−2 ⟹ w_α, w_μ, w_β ≥ 1) into Step 2 as a one-line conclusion.

## OUT_OF_SCOPE

### Topic 1: Rearrangement at text-subspace depth m_1 > 2
**Why out of scope**: The ASN deliberately restricts to m_1 = 2. Lifting the displacement/width arithmetic to deeper ordinals (where ord(v) is a multi-component tumbler, not a singleton) is genuinely new territory, not an error here.

### Topic 2: k-cut rearrangements (k > 4) and composition of rearrangements
**Why out of scope**: Listed in the ASN's own Open Questions; these are future generalizations, not defects in the 3-/4-cut treatment.

VERDICT: REVISE
