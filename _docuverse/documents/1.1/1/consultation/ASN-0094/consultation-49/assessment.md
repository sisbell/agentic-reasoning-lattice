# Channel Assignment — ASN-0094 review-49

**Date:** 2026-05-24 00:24

## Issue 1: BundledDirectedPair walkthrough — BDP0/BDP1 chaining inconsistency
Reason: Pure self-consistency issue within the walkthrough — the framework must pick one path (γ_0 in scope or not) and update the table accordingly. Derivable from the ASN's own walkthrough content.

## Issue 2: AllocatedAddressAntichain Sub-case 3b discharged "by symmetry" without explicit steps
Reason: Proof-completeness issue. Both options (write 3.3b out explicitly, or strengthen Case-symmetry preamble to enumerate Step 3.3's symmetric dependence on `s_L ≠ s_C`) are derivable from the existing proof structure. No external evidence needed.

## Issue 3: Coverage-equality decidability asserted but not shown
Reason: The decidability claim rests on ASN-0043's coverage definition (PrefixSpanCoverage, L5) which is part of this ASN's foundation. The fix — supply a derivation routing to a decidable comparison on finite span sets, or restrict the representative list to canonical-slot — is derivable from the cited ASN-0043 content.

## Issue 4: Per-shape uniformity downgrade weakens the catalog without procedural compensation
Reason: Self-consistency issue about this framework's META-level discipline. The fix is to reconcile two wordings ("mechanically" vs "aspiration") consistently — internal to Sh5(a)/(b) and the catalog row structure paragraphs.

## Issue 5: Sh4 Case A's case-equation closure obscured by expository framing
Reason: Proof-clarity issue. Either drop the non-load-bearing R2/LinkStoreInvariance citations from Case A or clarify their role with respect to the case-equation. Derivable from the proof's existing structure.

## Issue 6: NullifyActiveSubsetCompatibility Case B's witness extraction
Reason: Pure proof-clarity fix — add a single existential-elimination line. Derivable from the corollary's existing argument.

## Issue 7: BundledDirectedPair admits c_G = 0 but consequence for pair_K(a, ∅) not exercised
Reason: Walkthrough-completion issue. The template evaluation is mechanical once Issue 1 resolves the state question. Derivable from the catalog's own template definitions.
