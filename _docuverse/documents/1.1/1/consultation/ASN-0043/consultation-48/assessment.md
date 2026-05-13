# Channel Assignment — ASN-0043 review-48

**Date:** 2026-05-13 09:30

## Issue 1: T7 cited under reinvented name "SubspaceDisjointness"
Reason: Pure citation/naming correction — the foundation name (FirstElementFieldDistinction) and its postcondition are already established. The lift from pairwise to set disjointness is a standard logical step derivable from the ASN's own quantification.

## Issue 2: `fields(·)` notation reinvents T4b's projections
Reason: Notational alignment with foundation T4b and ASN-0036's existing conventions. Derivable entirely from documents already cited in the ASN.

## Issue 3: `fields(a).E₁` competes with ASN-0036's `subspace_I(a)`
Reason: Internal notational choice between two already-defined foundation/ASN-0036 spellings. No external evidence needed.

## Issue 4: L11a conflates uniqueness with permanence
Reason: Logical split of an over-bundled conclusion — uniqueness comes from GlobalUniqueness (already cited), permanence from L12 (already established in this ASN). Internal fix.

## Issue 5: L8 uses `.type` notation inconsistent with L3's `.eᵢ`
Reason: Internal notational definition — either define `.type ≡ .e₃` under StandardTriple or substitute throughout. The slot-3 type convention is already established by L3.

## Issue 6: L5's formal statement is tautological
Reason: Formal restatement of substantive content already in the prose. The set-equality predicate and absence of positional accessor are internal commitments of this ASN.

## Issue 7: L1a's formal predicate is informal
Reason: Formalize using `home(a)` (already defined) and T10a's spawning relation (foundation, already cited). The substantive content is already stated; the fix is making the predicate machine-checkable.

## Issue 8: PrefixSpanCoverage proof lacks explicit foundation citations
Reason: Adding foundation citations (Divergence, NAT-discrete, TA-strict) to existing proof steps. Purely foundation-internal.

## Issue 9: L0 set-disjointness derivation jumps from pairwise to set
Reason: Make the universal instantiation over `dom(Σ.L) × dom(Σ.C)` explicit. Standard logical lift from pairwise T7 to set disjointness — internal.

## Issue 10: Worked example does not demonstrate higher-arity links
Reason: Construct an arity-4 example using the ASN's own structure (N ≥ 3 endsets, slot 3 is type). Nelson's design intent for n-sets is already cited [LM 4/79] and Gregory's N=3 hardcoding already noted; no new external evidence is needed to build the example.
