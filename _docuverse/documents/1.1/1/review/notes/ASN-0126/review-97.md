# Review of ASN-0126

The note is rigorous where it does its central work: the registry invariance (P1), the conformance closure (P3/P6), the ProjectionBridge with its carefully scoped B1/B2, and the gate-realizability lift (P5) are all spelled out step by step, and the born-nullified worked illustration checks the gate-vs-landing separation against concrete addresses. I found no hand-waved proof in that machinery. The findings below are a semantic gap the note glosses, one meta-prose accretion the anti-bloat classifier asks me to surface, and an asymmetry in how the note accounts for its own exclusions.

## REVISE

### Issue 1: The from-fill `r` silently converts ASN-0086's *unattributed* retraction into a whole-document attribution

**ASN-0126, Retraction as an attributed Binary**: "`Nullify_Binary(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, {r}, {(a, δ(1, #a))})` — canonical from-fill `r = (d_retr, δ(1, #d_retr))` … The target stays in G, so ASN-0086's `nullified`/`L_R`/active-subset machinery — all reading `coverage(G')` and ignoring F — carries over unchanged."

**Problem**: The "carries over unchanged" claim is correctly scoped to the G-reading machinery, but it glosses a real change in the *attribution* dimension that ASN-0086 explicitly models. ASN-0086's Convention RetractionDirectionality states the from-set "is reserved for attribution-bearing endset content **or is left empty for unattributed retractions**," and its `Nullify` uses `∅` — i.e. ASN-0086's retraction is *unattributed*. Forcing `|F| = 1` does two things the note does not acknowledge:

1. **Unattributed retraction becomes inexpressible.** No registered shape admits `|F| = 0`, so ASN-0086's empty-from (unattributed) retraction has no `→_sh` image at all — a capability ASN-0086 deliberately provides is lost.
2. **The substituted `r` is not inert filler.** `coverage({(d_retr, δ(1, #d_retr))}) = {t : d_retr ≼ t}` by PrefixSpanCoverage — the *entire* document subtree (all versions, all content, all links, including the retraction tuple's own address). ASN-0086's `Observe_R` matches a from-pattern `F̂` against `coverage(F)`, so this from-set is observable and matchable: every retraction homed at `d_retr` now matches every under-`d_retr` from-pattern. The note's own thesis — that span count and coverage diverge (Shape-conformance) — makes this maximal-coverage from-fill exactly the case a careful reader would interrogate, yet the note introduces `r` as "canonical" without examining its coverage.

**Required**: Acknowledge that `|F| = 1` makes ASN-0086's unattributed retraction inexpressible and that the `r` from-fill injects a whole-document attribution observable via `Observe_R`. Either justify why whole-document attribution is acceptable, choose a from-fill whose coverage is defensible as the retraction's attribution, or state plainly that faithful attribution is deferred and the wrapper's `r` is a placeholder with this known consequence.

### Issue 2: Design-rationale reassurance in Shape-conformance (anti-bloat)

**ASN-0126, Shape-conformance**: "The framework deliberately combines a decomposition-blind type identity … with a decomposition-sensitive shape gate that counts the spans of slots 1–2; the two are independent. … an emitter freely chooses K and then supplies conforming F, G, **so the two checks can never be mutually unsatisfiable**."

**Problem**: The two concrete examples immediately preceding this (one-span F with unbounded coverage; two abutting spans with `|F| = 2` and coverage-equal-to-conformant) already establish that span count and coverage are independent measures. The trailing "The framework deliberately combines…" framing and the "can never be mutually unsatisfiable" reassurance add no reasoning the definition needs — no later proof (P5 included) cites non-mutual-unsatisfiability. This is the defensive design-rationale the `review-mode.anti-bloat` classifier flags. (The middle clause — "Slot 3's coverage class *selects* which span-count constraint applies to slots 1–2" — is substantive and should stay.)

**Required**: Drop the "deliberately combines… the two are independent" framing and the satisfiability reassurance; keep the selection mechanism and the two concrete examples.

### Issue 3: The `|F| ≥ 2` exclusion is treated asymmetrically, and OQ6 mislabels it as "arity"

**ASN-0126, Single-source / The shape-gated emit / Open questions**: The note handles two of its three exclusions inline and with care — empty-from (`|F| = 0`) gets a full re-expression as `Nullify_Binary`, and arity `N > 3` gets "every `N > 3` emission has **no** `→_sh` image. The path to richer arity is left to Open Question 6." But the third exclusion — `|F| ≥ 2` — is asserted ("Every typed relation the framework gates has a single-span source: `|F| = 1`") with no parallel acknowledgment.

**Problem**: A single span covers only a *contiguous* range (a T1-interval / subtree), so `|F| = 1` forbids a source spanning disjoint passages (e.g. "these three scattered sentences jointly cite X"), which needs `|F| ≥ 2`. The note never flags that this expressiveness is excluded, in contrast to the explicit inline treatment its other two exclusions receive. OQ6 is the only place it surfaces, and its body mislabels it: "**Extension beyond F=1 and N=3.** What path serves an app that needs richer **arity**?" — but `F = 1 → F ≥ 2` is from-*span-count*, not arity (slot count `N`); "richer arity" describes only the `N > 3` case. An app needing a multi-span arity-3 source is not captured by "richer arity."

**Required**: Add one clause in Single-source noting that `|F| ≥ 2` (disjoint/multi-span sources) is excluded and deferred — mirroring the inline exclusion notes already given for empty-from and `N > 3` — and fix OQ6's body to distinguish from-span-count (`|F|`) from arity (`N`).

## OUT_OF_SCOPE

### Topic 1: Full retraction-attribution semantics
How from-set attribution on retractions should be *queried* and *interpreted* (e.g. what an `Observe_R` from-pattern means once retractions carry attribution) is genuinely new territory for a successor note. Issue 1 asks only that the note acknowledge the shift its `r` introduces, not that it design the attribution model.

### Topic 2: The richer-`F` / richer-`N` extension itself
Loosening `|F| = 1` or `N = 3` is correctly deferred (OQ6). Issue 3 concerns only the note's internal consistency in *accounting* for the `|F| = 1` restriction, not the extension.

VERDICT: REVISE
