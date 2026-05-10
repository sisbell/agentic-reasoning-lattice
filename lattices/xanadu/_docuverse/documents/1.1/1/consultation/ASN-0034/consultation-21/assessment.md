# Revision Categorization — ASN-0034 review-21

**Date:** 2026-03-26 02:56

## Issue 1: TA3 and TA3-strict have no follows_from in the dependency graph
Category: INTERNAL
Reason: The proof text already explicitly names T1, TumblerSub, TA6, and T3 as dependencies. The fix is mechanical extraction from existing content into the dependency graph.

## Issue 2: Three individual dependency graph corrections
Category: INTERNAL
Reason: All three corrections are derivable from the ASN body — (a) the text explicitly says T1 is "a consequence, not an assumption," (b) D0 directly references the Divergence definition, (c) TA-assoc's proof expands TumblerAdd's formulas.

## Issue 3: TA7a name mismatch in dependency graph
Category: INTERNAL
Reason: The body labels the property "TA7a (Subspace closure)." The graph uses a different name. The canonical label is present in the ASN text; aligning is a mechanical edit.

## Issue 4: GlobalUniqueness property table missing T10a
Category: INTERNAL
Reason: The proof text says "By T10a" and the dependency graph already includes T10a. The property table simply omits it. All information needed for the fix is present in the ASN.

## Issue 5: Systematic name mismatches between body labels and dependency graph
Category: INTERNAL
Reason: The body's parenthetical labels (e.g., "Unbounded component values," "Contiguous subtrees," "Strict increase") are the canonical names. The graph entries used the Statement column or paraphrases instead. Alignment requires only reading the existing body text.
