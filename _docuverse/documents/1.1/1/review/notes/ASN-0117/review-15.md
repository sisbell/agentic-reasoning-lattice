# Review of ASN-0117

The mathematics is sound. I checked the two-case realisation (K.μ⁻+K.μ⁺ composite for `R ≠ ∅`, lone K.μ⁻ for `R = ∅`) against ASN-0047's ValidComposite definition, verified intermediate-state validity of both steps, confirmed the net effect matches ASN-0082's contraction clauses, re-derived the wp for discoverability preservation, and traced every boundary example (leading-span, suffix, delete-everything, within-document sharing, cross-document transclusion). All hold. The coupling discharges (J0/J1★/J1'★ vacuous; P4★/P7a preserved) are correct. The findings below are anti-bloat duplications — this note carries `review-mode.anti-bloat`.

## REVISE

### Issue 1: Count-vs-per-pair justification stated twice
**ASN-0117, DEL-REMOVE and P1 (ArrangementContraction)**:

DEL-REMOVE: "We state the contraction as a count, plus the vacating of the top `c` position labels, rather than as the absence of each specific old pair — because a deleted-span label `q_k` with `k ≤ N−c` does not vacate the domain... under within-document sharing (S5/M13...) ... the per-pair absence `(q_k, M(d)(q_k)) ∉ M'(d)` fails even though the count contraction still holds."

P1: "We state the contraction as a count rather than as the absence of each old pair, since within-document sharing (S5/M13) can let a shifted reoccupant rebind a deleted-span label to the very same I-address."

**Problem**: The same within-document-sharing rationale for choosing the count form over a per-pair-absence form is given at length in DEL-REMOVE and restated in P1 — two claim statements carrying the same defensive justification.
**Required**: State the rationale once (DEL-REMOVE is the natural site) and let P1 carry only the count claim, or a bare back-reference.

### Issue 2: Entity/provenance frame derivation stated in Effect section and re-stated in DEL-FENT / DEL-FPROV
**ASN-0117, Effect section and clauses DEL-FENT, DEL-FPROV**:

Effect: "Both component steps fix the entity set and the provenance relation (`E' = E`, `R' = R`: K.μ⁻'s frame and K.μ⁺'s frame each list both — clauses DEL-FENT, DEL-FPROV below), so the composite does too..."

DEL-FENT: "Both component steps carry an entity frame `E' = E` (K.μ⁻'s frame and K.μ⁺'s frame, ASN-0047), so their composite fixes `E`."

DEL-FPROV: "Both component steps carry a provenance frame `R' = R` (K.μ⁻'s frame and K.μ⁺'s frame, ASN-0047), so their composite fixes `R`."

**Problem**: The "both component steps carry the frame ⟹ the composite fixes it" derivation appears once for `E` and once for `R` in the Effect section, then is reproduced verbatim-in-substance in DEL-FENT and DEL-FPROV. The Effect paragraph even forward-points to "clauses DEL-FENT, DEL-FPROV below," which then repeat the same reasoning rather than carrying only the bare frame statement. (Contrast the P4★/P7a treatment, which the Effect section proves and DEL-FPROV correctly reduces to a back-reference — that is the pattern the frame clauses should follow.)
**Required**: Establish `E' = E` and `R' = R` once (Effect section) and reduce DEL-FENT/DEL-FPROV to the frame statement plus a back-reference, as already done for P4★/P7a.

## OUT_OF_SCOPE

### Topic 1: Deletion at text depth `m > 2`
**Why out of scope**: The precondition fixes `m = #p = 2`, inheriting ASN-0082's depth-2 contraction. Deeper text arrangements would need a deeper foundation displacement, not a revision here.

VERDICT: REVISE
