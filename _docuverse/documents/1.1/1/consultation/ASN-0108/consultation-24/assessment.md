# Channel Assignment — ASN-0108 review-24

**Date:** 2026-06-13 00:41

## Issue 1: "Never reused" miscited to T8; address-key stability is definitional, not an allocation consequence
Reason: Fully internal. The fix is a re-attribution among foundation claims already in the lattice — swap "never reused (T8)" to GlobalUniqueness (ASN-0034), keep T8/LP13 for the cursor address remaining a valid cut-point — and ground state-stability in the observation that `κ(a) = a` is a state-independent function (`κ_Σ(a) = κ_{Σ'}(a) = a`), a mathematical fact derivable from the address-key definition already stated. No design intent or implementation evidence is at issue; the review itself names which claim discharges which fact.

## Issue 2: Essay-length entries in the "Claims Introduced" table
Reason: Internal formatting fix. Reducing the W5/W9/W9b rows to one-line summaries restates content already present in the claim bodies; nothing about design intent or implementation evidence is consulted.

## Issue 3: Self-acknowledged cross-section duplication (W5 ↔ W9d)
Reason: Internal editing fix. Consolidating the free-tail-permutation walk to one location and replacing the other with a label citation is a structural deduplication of the note's own prose; no external channel bears on it.

## Issue 4: Defensive meta-prose justifying authorial choices rather than stating claim content
Reason: Internal editing fix. Cutting the justificatory tails from W10 and W3 removes reviewer-facing editorializing while leaving the substantive guarantees (already stated) intact; neither design intent nor implementation evidence is needed.
