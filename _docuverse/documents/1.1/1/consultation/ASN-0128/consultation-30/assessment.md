# Channel Assignment — ASN-0128 review-30

**Date:** 2026-06-11 08:38

## Issue 1: BH1's Effect line states denotation-level exclusion while `is_filtered` is coverage-level
Reason: The formal predicate and the note's own AD assertion doctrine both point toward coverage-scoped filtering, but the review explicitly offers two divergent resolutions (align prose vs. redefine the predicate), and choosing between them turns on whether a lifecycle mark on a containing address was *meant* to hide its sub-entities — a design-intent question the ASN's internal content cannot settle. Gregory is not needed: the implementation's coverage-native query evidence is already cited in AM and would not distinguish the two readings for a filter mark.
Nelson question: When a containing entity (e.g., a whole document) is marked as lifecycle-retired or hidden, does the design intend that its contained parts and sub-addresses also vanish from default presentation, or does retirement apply only to the marked entity itself?

## Issue 2: The attainability-convention sentence is duplicated verbatim in I6 and DR
Reason: Purely editorial deduplication — the convention statement is stated once and cited from the second site, with each site's distinct necessity argument retained; no design intent or implementation evidence bears on it.
