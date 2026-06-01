# Channel Assignment — ASN-0086 review-208

**Date:** 2026-06-01 16:10

## Issue 1: "Definition — relational layer" restates the discipline and re-derives its own reduction
Reason: Internal — the fix only trims redundant prose down to the operation set plus the one non-redundant fact (the layer never invokes `Emit_K` at `K ~ R` except via the `Nullify` alias). All referenced facts are already stated in the ASN's own definitions and table.

## Issue 2: EmptyInitialLinkStore justifies the assumption via implementation rather than stating it
Reason: Internal — the required fix is to state the assumption (already fully given in the preceding sentence) and stop, demoting the `initmagicktricks`/`createenf` walkthrough to at most a one-clause citation. No new evidence is needed to remove prose; the assumption stands on its own content.

## Issue 3: "A_rel^Σ names the whole link store, not only the tuples" is pure restatement
Reason: Internal — the fix is deletion; the load-bearing distinction is already carried by the `|Σ.L(a)| = 3` conjunct of `L_K^Σ`. Nothing external is required.

## Issue 4: L-ContiguousPrefix-Cor1 is proved but consumed by no invariant or operation
Reason: Internal — the choice (consume the strict `#E = 2` where proofs currently fall back on `(UL)`/`≥ 2`, or demote the corollary to a remark) is a structural decision fully derivable from the ASN's own proof dependencies; the related Open Question about tightening L1b is not what this revision must resolve.
