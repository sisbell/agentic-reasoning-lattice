# Channel Assignment — ASN-0047 review-250

**Date:** 2026-06-01 13:39

## Issue 1: J4 fork — k=0 subsequent-version content source asserted but unverified, no concrete example
Reason: The fix requires deciding whether a new version forks the base document or its immediate predecessor's content — a design-intent question (Nelson) confirmed against what the implementation's version-creation actually copies (Gregory). The ASN itself cannot resolve which behavior is correct, only formalize it once known.
Nelson question: When a new version is created from a prior version (CREATENEWVERSION on an already-edited version), is the new version intended to inherit the prior version's edited content, or to re-fork the original base document's content?
Gregory question: When `docreatenewversion` is invoked on a document that is itself a version with edits not present in its ancestor, does the vspan retrieval (`doretrievedocvspanfoo`) copy the immediate source's current content including those edits, or the ancestor's original content?

## Issue 2: Operational-depth paragraph restates the re-pinning fact three times
Reason: Purely an editorial anti-bloat collapse of three restatements of one rule into a single statement; the substantive content (definedness only while `V_S(d) ≠ ∅`, re-pinning to any `m ≥ 2` after clearance) is already fully present in the ASN.
