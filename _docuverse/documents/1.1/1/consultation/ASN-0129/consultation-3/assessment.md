# Channel Assignment — ASN-0129 review-3

**Date:** 2026-06-11 12:30

## Issue 1: "exactly as conjectural as C-reach" misstates the logical relationship — with inverted polarity
Reason: Internal. The error is a logical mis-statement about the relationship between PC6's relativized ceiling and C-reach, both of which are this note's own constructs; the corrected entailment (unrestricted ceiling ⟹ ¬C-reach, so conjecturing C-reach means conjecturing the unrestricted ceiling fails) follows from the note's existing feedback-decides-reach argument with no design-intent or implementation input.

## Issue 2: FP's per-atom table contradicts PD2's use of it for behavior atoms at the default view
Reason: Internal. UV — the note's own definition — already fixes which atoms are rewritten at the default view (collections yes; verdicts, Booleans, Map_fin no), and the filter footprint `⋃_{J ∈ Φ}(L_J ∪ L_R)` is already stated in FP's core-atom row; the fix is propagating that increment uniformly across FP's collection-returning rows so the table matches PD2's already-correct claim.

## Issue 3: QD-fin cites L-fin at extended-record states without the transfer chain the note requires of itself elsewhere
Reason: Internal. The review's recommended discharge is self-contained in the note's own proof: `Σ_init.L = ∅` (R-VAL) is already invoked in the H-init paragraph, and the reaching-derivation induction already run for `dom(Σ.C)` and `dom(Σ.M)` extends to `dom(Σ.L)` with one fresh key per step — no upstream evidence or intent needed.

## Issue 4: PC6's converse discharges registry-lookup leaves "by admission," but no registry-reading atom is admitted
Reason: Internal. The cheap fix the review identifies — discharging registry-lookup leaves by R1 constant-folding rather than admission — uses only R1 (already cited throughout the note) and preserves the existing "exactly four admissions" bookkeeping and the note's established stance that PL reads no registry data beyond `Reg`; no new atom, hence no design or evidence question, is required.

## Issue 5: V-IDX's static expansion is undefined when the body's vocabulary is not attached at every registered class
Reason: Internal. The required clause — a `Reg`-quantified term is well-formed iff each expansion instance is a PL term — is fully determined by the note's own machinery: the registry is static (V-STAT, R1, C0), so the finitely many instances are checkable at construction, and the fix is a definitional well-formedness condition on this note's own term former.

## Issue 6: no composed predicate is ever evaluated at a concrete state; the PD1 oscillation is asserted, not traced
Reason: Internal. The trace is a mechanical exercise of semantics already on the page: `OPEN(t)`'s definition, the cmt/res registrations, and Nullify_Binary's stated effect (removes from `A_K` while `L_K` retains) determine every evaluation at Σ₁–Σ₃, and the optional audit-view PD0 term locks ⊤ by PD0's own ground.
