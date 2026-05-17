# Channel Assignment — ASN-0086 review-13

**Date:** 2026-05-16 20:33

## Issue 1: Unexplained "S" labels in Consequences sections
Reason: Pure editorial/structural fix about naming convention within this note. Either introduce S-numbering at first use or drop the labels — derivable from the ASN's own content.

## Issue 2: `inc` iteration composition asserted without justification in R0a Sub-case B
Reason: The fix is citing existing ASN-0034 lemmas (TA5-SigValid, TA5a at k=0, TA5(c)) which the note already depends on. Internal proof tightening, no external channel needed.

## Issue 3: Hand-wave on remaining S-invariants in R0 Step 4
Reason: The S-invariants are defined in ASN-0036 (already a dependency); the fix is either enumeration or a meta-argument about class-(iii) Frame fixing Σ.C and Σ.M pointwise. Derivable from the ASN's stated Frame conditions.

## Issue 4: "Subspace distinctness consumed at R5" — direct vs. inherited
Reason: Pure editorial fix in the Properties Introduced table. R5's actual dependence (indirect via R0) is already correctly stated in its section header; the table just needs to match.

## Issue 5: R6c's broader transition extension rests on an uncharacterized parallel vocabulary
Reason: Arrangement-modification frame semantics live in ASN-0036; the fix is either stating the frame explicitly in this note's Frame subsection or adding an ASN-0036 citation. Derivable from the existing dependency.
