# Channel Assignment — ASN-0118 review-26

**Date:** 2026-06-10 18:46

## Issue 1: The operation's frame omits Σ.E entirely and bounds Σ'.R from below only
Reason: The review itself establishes that both closures are derivable from the exhibited composite (no K.δ step runs, and J1'★ pins `R' ∖ R` to the range-new pairs of `d`); the fix is to promote already-derived facts to operation-level clauses, matching the standard CP3c already sets. No design-intent or implementation question is open.

## Issue 2: Claims-table gloss for CP2 calls the placement positions "fresh"
Reason: The body text already states the correct semantics ("bound, in order, to the `W` V-positions starting at `p`") and the worked example exhibits the rebinding of `[1,2]`; this is an internal wording correction to make the table gloss match the ASN's own content.

## Issue 3: Lockstep within runs of the restriction is cited to ASN-0036's S8
Reason: The review identifies the correct authority (ASN-0058 C1a with MaximalRun condition 1 and B3 consistency), which the sentence already partially cites; the fix is a citation swap within the ASN's existing dependency structure, with the conclusion unchanged.

## Issue 4: Duplicated motivation and structural announcements (anti-bloat)
Reason: Pure prose deletion of redundant preview and meta-sentences; the surviving paragraphs already carry the full argument, so no external consultation is needed.
