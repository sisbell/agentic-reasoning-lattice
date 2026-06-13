# Channel Assignment — ASN-0108 review-37

**Date:** 2026-06-13 05:15

## Issue 1: The "allocation is orthogonal" argument is stated in W5, then restated-and-deferred in W8, then pointed at again from the Claims table
Reason: Pure deduplication/restructuring. The orthogonality argument, value-totality, and the "computable on held value with no state lookup" property are all already stated in the ASN; the fix consolidates the point in W5 and trims the W8 deferral and table parenthetical to the substantive content W8 adds. No design intent or implementation evidence is needed.

## Issue 2: Key-trichotomy meta-synthesis and cross-claim deferrals recur as accretion
Reason: Internal editorial trim. Removing W6's forward reference to W8's hazard, dropping the "(comparison's home)" parenthetical, and reducing the glossary to its genuinely new dichotomy all operate on content already established at the relevant use sites (W6's allocation-monotonicity, W2/W8's computability and value-totality); nothing new must be derived from design intent or the implementation.
