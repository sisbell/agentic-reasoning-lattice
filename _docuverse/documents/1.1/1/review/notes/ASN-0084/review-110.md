# Review of ASN-0084

## REVISE

### Issue 1: "Collapse of R-PRE(iv)" is unused meta-prose about precondition economy
**ASN-0084, "Consequences of R-PRE," *Collapse of R-PRE(iv) to a single ordinal bound***: "Under D-SEQ, R-PRE(iv) carries no content beyond one inequality on the rightmost cut. … Thus R-PRE(iv) adds precisely the requirement that the affected range not exceed the existing content by more than one position; the EXT-VAC case … is its boundary."

**Problem**: This paragraph derives `ord(c_{n−1}) ≤ N + 1` but the result is never consumed downstream. EXT-VAC independently establishes the only boundary fact actually used in R-BLK (`c_{n−1} ∉ V_S(d) ⟹ c_{n−1} ∉ dom(M(d))`, empty right exterior), and the boundary worked example reaches `[S, N+1]` directly from D-SEQ. The paragraph is commentary on *what R-PRE(iv) means* / *why it is economical* rather than a step any later claim needs — precisely the "explains why rather than what" pattern the anti-bloat classifier targets. It also restates EXT-VAC's boundary content in different words.

**Required**: Delete the *Collapse of R-PRE(iv)* paragraph, or fold its one load-bearing fact (the boundary `ord(c_{n−1}) = N+1`) into EXT-VAC where it is used.

### Issue 2: Width-positivity paragraph re-derives the singleton-tumbler identification already established in the State section
**ASN-0084, "Consequences of R-PRE," *Width positivity***: "For each adjacent cut pair (c_i, c_{i+1}): by CS5, ord(c_i), ord(c_{i+1}) ∈ ℕ⁺, so both cut ordinals lie in the domain of the singleton-tumbler identification; by CS2 and T1, c_i < c_{i+1}, which under that identification coincides with ord(c_i) < ord(c_{i+1})…" and "…the shared leading component S cancels and the singleton-ordinal coincidence established above gives `c_i ≤ v < c_{i+1} ⟺ ord(c_i) ≤ ord(v) < ord(c_{i+1})`."

**Problem**: The State section's *Identification of singleton tumblers with natural numbers* paragraph already proves that T1 order on singletons coincides with `<` on ℕ⁺ and that the leading component cancels. Width positivity re-walks this machinery instead of citing it, so the reader re-reads an established equivalence to follow a one-line count. This is re-derivation noise of the kind the classifier flags ("two paragraphs say the same thing in different words").

**Required**: Replace the re-derivation with a citation to the State-section identification, leaving only the new content (`w_α = ord(c₁) − ord(c₀) ≥ 1`, etc., and the count of V-positions per interval).

## OUT_OF_SCOPE

### Topic 1: k > 4 cut rearrangements and composition of rearrangements
**Why out of scope**: Already correctly deferred to the Open Questions; generalizing the pivot/swap to k > 4 and characterizing the closure of REARRANGE under composition is new territory, not a defect in this ASN's three- and four-cut treatment.

VERDICT: REVISE
