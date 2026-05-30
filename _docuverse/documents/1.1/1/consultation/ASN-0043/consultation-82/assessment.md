# Channel Assignment — ASN-0043 review-82

**Date:** 2026-05-30 09:44

## Issue 1: L1c axiom wrapped in rationale prose
Reason: Pure deletion of rationale prose; the formal chain statement already present in the ASN carries the axiom's content. No design-intent or implementation evidence is needed to remove explanatory text.

## Issue 2: L9 and L11b duplicate the entire "fresh sibling preserves all invariants" verification
Reason: Both proofs already exist in the ASN; the fix factors the shared sibling-allocation argument into one lemma and cites it. This is internal proof restructuring requiring no external evidence.

## Issue 3: Worked example re-lists the full state-local invariant set five times
Reason: Collapsing repeated one-line confirmations into a single shared statement is an editorial deduplication using arguments already present in the worked example. Derivable from the ASN alone.

## Issue 4: PrefixSpanCoverage asserted as an axiom but derivable from the foundation
Reason: The required derivation cites only ASN-0034 foundation results (OrdinalShift, T12, T5, T1 case ii), all available within the spec. Reclassifying and proving it is internal mathematics needing no design-intent or implementation input.

## Issue 5: L2's two-state framing contradicts L12
Reason: Restating L2 as `home` being a T4 projection on the address alone follows directly from the `home(a) = N(a).0.U(a).0.D(a)` definition already in the ASN. Purely internal reframing.
