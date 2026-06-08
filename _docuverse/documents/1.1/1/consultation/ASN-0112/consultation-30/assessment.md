# Channel Assignment — ASN-0112 review-30

**Date:** 2026-06-08 10:24

## Issue 1: V8 cross-state depth invariance is not established by the cited invariant
Reason: Internal. The fix is a citation correction within established spec machinery — replacing the S8-depth attribution with ASN-0047's `m_S(d)` re-pinning discipline, which this note already builds on (D-MIN★/D-SEQ★ are cited from the same source). No external channel adjudicates which invariant grounds cross-state `m_C` constancy.

## Issue 2: V17 is implementation mechanics, not a system invariant
Reason: Internal. The note itself concedes abstract positivity is already V2's, so removing V17 from the table and demoting its content to an evidence remark under V2 is a pure editorial restructuring derivable from the ASN's own admission.

## Issue 3: Defensive reachability construction inlined into V5
Reason: Internal. The fix only requires trimming the operational construction recipe from V5's parenthetical, leaving a bare reachability assertion — an editorial deletion that needs no evidence or design-intent adjudication.
