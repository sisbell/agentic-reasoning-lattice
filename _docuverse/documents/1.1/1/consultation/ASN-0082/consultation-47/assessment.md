# Channel Assignment — ASN-0082 review-47

**Date:** 2026-05-30 08:59

## Issue 1: I3-S(a) and D-S(a) end in ✓ but rest on an ℕ-arithmetic fact the foundation does not supply
Reason: The fix is a mathematical/internal matter — either prove commutativity and associativity of ℕ `+` locally from NAT-wellorder by induction, restructure to avoid reordering summands, or downgrade the ✓ to an open obligation. The reviewer already enumerates the available NAT-* axioms, so no design-intent or implementation evidence is required; this is resolvable from the ASN and ASN-0034's stated axiom set.

## Issue 2: D-CTG is restated with a dropped conjunct, strengthening the cited foundation invariant
Reason: The fix is to quote D-CTG verbatim with its `zeros(v) = 0` guard and have D-SEP(b) discharge `zeros(r) = 0`. The reviewer supplies the correct foundation form, and `r = [1, p₂+c]` is zero-free by construction within the ASN — fully derivable from the ASN's own content.

## Issue 3: D-SEQ-post relies on proof-internal "Step 1/2/3" of ASN-0036, not on its contract
Reason: The fix is to delete the decorative references to ASN-0036's internal step numbering and keep the self-contained local replay, which the reviewer confirms already stands alone. Purely editorial and internal.

## Issue 4: The depth scoping axiom is justified twice in near-identical prose
Reason: The fix is to collapse two adjacent paragraphs making the identical TA4/S8a-collision argument into a single statement. Purely an editorial deduplication, derivable from the ASN's own text.

## Issue 5: I3-V is explained three times in prose beyond its worked-example trace
Reason: The fix is to keep the tightest single statement (the I3-CS corollary derivation) plus the worked-example trace and remove the two redundant expositions. Purely an editorial deduplication, internal to the ASN.
