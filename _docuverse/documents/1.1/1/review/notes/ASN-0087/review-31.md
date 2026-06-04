# Review of ASN-0087

## REVISE

### Issue 1: The v_ℓ freshness argument is given twice
**ASN-0087, "Freshness of the Allocation" and "Per-State Invariants at Σ'" (S2)**: The freshness section already states both halves of the argument — "K.μ⁺_L's positioning rule combined with D-SEQ★ ... supplies the within-subspace half" and "full freshness additionally requires the cross-subspace exclusion `v_ℓ ∉ V_{s_C}(d)`, which holds at position 1" — and then says "Both halves are discharged in full in the S2 verification of the post-state invariants below." The S2 verification then restates the identical two-part split (within-subspace via D-SEQ★, cross-subspace via position 1 / SC-NEQ).
**Problem**: The same proof appears in two sections, with the first deferring to the second even though it has already made the argument. This is duplicate prose plus a forward pointer to a location that adds nothing the first passage omitted.
**Required**: State the two-part freshness argument once (S2 is the natural home), and in the freshness section either drop the V-position discussion or reduce it to a one-line cite of S2.

### Issue 2: "Transfers verbatim" meta-prose narrating non-derivation, repeated
**ASN-0087, "Freshness of the Allocation"**: "We do not re-derive this from the underlying chain lemmas; ASN-0093 already packages the guarantee for every emission of `A_L(d)`, and MAKELINK introduces no allocation step beyond the K.λ it composes, so the result transfers verbatim" — and the subsequent-emission bullet's closing "so the layered argument lives in the foundation, not here."
**ASN-0087, "Per-State Invariants at Σ'" (L1c)**: "We discharge it by the same transfer discipline used for freshness above, and for the same reason: ASN-0093 already establishes a T10a-conforming chain for *every* emission ... MAKELINK introduces no allocation step beyond the K.λ it composes, so the conformance result transfers verbatim — no re-derivation of the chain is needed."
**Problem**: Both passages explain *why the author is not deriving something* rather than deriving it or simply citing it, and they say the same meta-thing ("ASN-0093 packages it; MAKELINK adds no allocation step; transfers verbatim") in two places. This is the explain-why-not-what pattern compounded by cross-section duplication.
**Required**: Replace each with a bare cite of the relevant ASN-0093 lemma (FirstEmissionFreshness / SubsequentEmissionFreshness for freshness; ChainMembershipForOrigin / ChainDiscipline for L1c). Drop the "we do not re-derive," "transfers verbatim," and "lives in the foundation, not here" narration.

### Issue 3: M-DepthConv carries rationale prose about a sibling primitive
**ASN-0087, Inputs (M-DepthConv)**: "This is MAKELINK's normative commitment, not a system-wide invariant; the general `m_L(d)` reading is retained downstream, since K.μ⁺_L is a standalone substrate primitive that may be invoked outside MAKELINK."
**Problem**: The trailing clause justifies *why* the general reading is retained by appeal to K.μ⁺_L's standalone status — rationale prose that does not advance the convention's content.
**Required**: State the commitment ("MAKELINK first links are placed at m = 2; S8-depth then pins m_L(d) = 2 for that document") and drop the justification clause.

### Issue 4: Defensive "not over dom(C)" prose on S7d
**ASN-0087, "Per-State Invariants at Σ'" (S7d)**: "S7d quantifies over *document tumblers* (each `d` has `zeros(d) = 2` ...) — *not* over `dom(C)`. MAKELINK registers no new document ..."
**Problem**: The emphasized "*not* over `dom(C)`" reads as a correction relocated from a prior misreading rather than as forward-moving content; the surrounding S4/S7a/S7b/C1b/C1c items already establish the dom(C)-unchanged fact.
**Required**: Reduce to "S7d: document set unchanged (`dom(Σ'.M) = dom(Σ.M)`); preserved by inheritance."

### Issue 5: Repetitive frame-inheritance justification across many invariants
**ASN-0087, "Per-State Invariants at Σ'"**: S4, S7a, S7b, C1b, C1c, P6, P7, P8, NodeLineage, ActivatedEmission each carry a near-identical clause of the form "preserved by inheritance (no new `dom(C)`/`E` entries) since `Σ'.C = Σ.C` ... quantifies over `dom(C)`/`E`, which is unchanged."
**Problem**: A dozen conjuncts repeat the same justification in slightly varied words. Every conjunct must be named (rigor), but the per-item prose is the duplication the anti-bloat pass targets.
**Required**: Group the frame-unchanged components once ("every invariant quantifying solely over `C`, `E`, `R`, or the document set `dom(M)`, all frame-fixed, is preserved by inheritance: S4, S7a, S7b, C1b, C1c, C-fin, P6, P7, P8, M0, NodeLineage, ActivatedEmission") and drop the per-item restatement.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets (Open Question 1)
**Why out of scope**: Constraints on endsets whose spans reference not-yet-allocated I-addresses are correctly left to a future endset-well-formedness ASN; the note flags it as an open question rather than asserting a claim.

### Topic 2: Protocol-layer composite atomicity (Open Question 2 / M-CompAtomicity)
**Why out of scope**: M-CompAtomicity correctly establishes that the substrate provides no composite atomicity and locates the guarantee at the protocol layer; the enforcing mechanism belongs to that higher layer, not this ASN.

VERDICT: REVISE
