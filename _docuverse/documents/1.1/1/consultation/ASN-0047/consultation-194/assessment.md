# Channel Assignment — ASN-0047 review-194

**Date:** 2026-06-01 01:21

## Issue 1: Meta-prose inventorying where a property is consumed
Reason: Pure editorial deletion of a use-site pointer clause; the TrackedEmission preservation argument already stands alone. Derivable from the ASN.

## Issue 2: P3 / content-store-invariance restated in three locations
Reason: Consolidation of a derivation already present three times into one canonical statement with cross-references. Derivable from the ASN.

## Issue 3: Orphan-link / tombstoning point repeated across four sites
Reason: De-duplication of an architectural claim already stated, with the canonical site and worked-example instance retained. The Nelson LM 4/9 citation is already present; no new design intent is needed.

## Issue 4: P4a mixes state quantification with transition-history quantification
Reason: The well-typing choice is forced internally — the ASN's own staleness design (J2, P4★ divergence, stale entries persisting in R) rules out the state-local current-M form (option a), since R provably retains entries no longer in M; classifying P4a as a trace property (option b) follows from commitments already in the ASN. Derivable from the ASN.
