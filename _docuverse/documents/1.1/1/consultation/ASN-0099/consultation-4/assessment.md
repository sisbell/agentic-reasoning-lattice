# Channel Assignment — ASN-0099 review-4

**Date:** 2026-05-26 17:03

## Issue 1: F9 derivation relies on an unstated "standing convention"
Reason: The fix is internal — the reviewer offers three concrete options (state the convention here, enumerate K-operations to argue completeness, or defer to an ASN-0047 revision), all of which are formal-spec-craft moves derivable from the ASN's own operation enumeration and the foundation ASNs already cited.

## Issue 2: Worked example mis-computes coverage of canonical spans
Reason: The fix is a straightforward mathematical correction using PrefixSpanCoverage from ASN-0043, which is already referenced. Rewriting the worked example with `{t : α ≼ t}` in place of `{α}` is purely internal.

## Issue 3: Slot-out-of-range convention is not folded into the definition
Reason: The fix is a one-line edit folding the discussed convention (`i ≤ |Σ.L(a)|`) into the conjunct. The convention is already articulated in the surrounding prose; only the formal definition needs to absorb it.

## Issue 4: F12 preconditions should be stated explicitly
Reason: The fix is to add a `defined when` clause to F12 mirroring `image`'s presentation. Both `image`'s and F12's preconditions are already established in the ASN; this is presentational hygiene.

## Issue 5: Finite-non-empty terms in the filter recovery should be noted
Reason: The fix is one observational sentence appealing to L-fin (ASN-0093) and L3 (ASN-0043), both already referenced in the ASN. Internal clarification only.
