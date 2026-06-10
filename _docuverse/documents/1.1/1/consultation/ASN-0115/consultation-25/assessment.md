# Channel Assignment — ASN-0115 review-25

**Date:** 2026-06-09 22:22

## Issue 1: R9's provenance clause contradicts the content/link payload asymmetry the ASN itself establishes
Reason: Internal. The contradiction is wholly between R9 and the ASN's own established claims — R1 (content items carry `Σ.C(a)`, not `a`) and R10 (link items carry `a`), with R4+R5 already pinning per-document resolution and ordering. Both repair options (expose the kind asymmetry, or demote the traceability sentence to expository remark deferring inline content-provenance to the existing Open Question) are derivable from the claims already present; no design intent or implementation evidence is at stake in fixing an output-recoverability inconsistency among the ASN's own clauses.

## Issue 2: the subspace-straddling exclusion is stated three times (anti-bloat)
Reason: Internal. Pure editorial deduplication — deleting the §"subspace crossing" parenthetical that restates the §"What a spec-set is" exclusion plus the already-proven Confinement lemma, and letting each scoping concern (straddling, channel faithfulness, inline provenance) sit once with the Open Questions carrying the forward framing. Nothing turns on design intent or implementation behavior.
