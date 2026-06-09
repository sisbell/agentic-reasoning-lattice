# Channel Assignment — ASN-0116 review-42

**Date:** 2026-06-09 11:38

## Issue 1: Duplicated RAN-coupling reasoning across two sections
Reason: Purely structural deduplication — the fix removes a re-derivation that the ASN already states verbatim in the valid-composite clause 2. No design intent or implementation evidence is needed; both passages are internal to the ASN.

## Issue 2: Anticipatory use-site justifications in the precondition slot
Reason: Editorial relocation — the precondition clauses and their downstream consumers (P7a, K.α typing) are already present in the ASN; the fix only moves justifications to their points of use. Fully derivable from the ASN's own content.
