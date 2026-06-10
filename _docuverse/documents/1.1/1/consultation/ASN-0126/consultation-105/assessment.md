# Channel Assignment — ASN-0126 review-105

**Date:** 2026-06-10 12:44

## Issue 1: T4-validity of the chain elements is hypothesized, never discharged
Reason: The fix is internal — the review prescribes the exact discharge (T10a.4 propagation across sibling advances, seeded at the T4-valid document node via DocVal/S7d, induction on j), and every lemma it invokes (T10a, L1c, TA5(c), FSE pattern) already exists in the cited dependency ASNs 0034/0043. This is a proof-obligation gap in the note's own formalism, not a question of design intent or implementation behavior.

## Issue 2: The Observe_R claim quantifies over retractions the wrapper does not produce
Reason: The fix is internal — the note's own worked illustration supplies the counterexample (a gate-clearing retraction with `F = [c₁]` that the under-`d_retr` pattern misses), and both repair options the review offers (scope the quantifier to wrapper-routed retractions, or declare the canonical from-fill normative for `Nullify_Binary`) are conventions of this note's own wrapper construction, already grounded in the LM 4/52–4/53 citation it carries. No new design-intent or implementation evidence is required to execute either.
