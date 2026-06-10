# Review of ASN-0126

This is a careful, largely sound note. The projection-bridge machinery (B1/B2), the effect-identity refinement, the R-Scope transfer to the Binary wrapper, the wp derivation (C3 going live), and the "born nullified" worked example all check out under scrutiny — I verified the addresses, the half-open coverage of `G_rng`, the `a_emit` chain, and the frame-the-two-post-states argument, and they hold. The findings below are a foundation miscitation and accretion flagged by the anti-bloat classifier.

## REVISE

### Issue 1: "a single span covers only a contiguous T1-interval (a subtree, by PrefixSpanCoverage)" — miscited foundation, false in general

**ASN-0126, Single-source**: "a single span covers only a *contiguous* T1-interval (a subtree, by PrefixSpanCoverage, ASN-0043), so a source spanning *disjoint* passages … needs `|F| ≥ 2`, and the framework gates no such multi-span source."

**Problem**: Two precision defects in one sentence.

1. *The "(a subtree)" gloss is wrong, and PrefixSpanCoverage does not support it.* PrefixSpanCoverage (ASN-0043) establishes subtree coverage only for the **unit-depth** span `(x, δ(1, #x))`, whose coverage is `{t : x ≼ t}`. A general single span `(s, ℓ)` covers the half-open T1-interval `{t : s ≤ t < s ⊕ ℓ}`, which is **not** a subtree. The note contradicts its own gloss two sections later: in *Worked illustration → Born nullified* it uses the single span `G_rng = {(g, δ(3, #g))}`, whose coverage is "a contiguous range of three link siblings and their subtrees" — a union of three subtrees, not one. So a single span does not in general cover a subtree, and citing PrefixSpanCoverage (a unit-depth result) for the general claim is a misapplication of the foundation.

2. *"disjoint passages need `|F| ≥ 2`" understates what the gate excludes.* The gate measures **span count**, not contiguity — as *Shape-conformance* correctly states: "a source presenting one contiguous extent as two abutting spans … has `|F| = 2` and fails every shape even though its coverage equals that of the conformant one-span F." So `|F| ≥ 2` is not the "disjoint source" case; it is the *multi-span* case, which also includes contiguous sources the app expressed with more than one span. OQ6 itself names "a multi-span source," not a disjoint one. Single-source's motivation is the only place that conflates the two.

**Required**: Drop "(a subtree)" or qualify it to the unit-depth case (the load-bearing claim — "a single span covers a contiguous T1-interval" — is correct and follows from the `coverage` definition + T1, not from PrefixSpanCoverage). Reword "disjoint passages … such multi-span source" so the motivation matches the span-count gate of *Shape-conformance* and OQ6 — the gate excludes every `|F| ≥ 2` source, contiguous or not, because conformance is sensitive to span decomposition, not coverage.

### Issue 2: Forward-reference / meta-prose accretion

The note carries the anti-bloat classifier; these are the genuine instances. Each is mild, but they are the kind that compound across cycles.

- **Single-source** — "This expressiveness — from-*span-count* `|F| ≥ 2`, distinct from richer *arity* — is deferred to Open Question 6." The em-dash aside pre-explains the `|F| ≥ 2`-vs-arity distinction that is exactly OQ6's job to draw. A bare deferral (or none — the limitation is already evident) suffices here; the distinction belongs at OQ6.

- **The registry → Worked illustration** — the point "any human-readable label … is an app-side convention over addresses, not substrate state" (The registry) is restated as "the readable labels … are the app's own (app-side, not substrate state — The registry)" (Worked illustration). The second is a back-referenced reminder duplicating the first; two paragraphs say the same thing.

- **Retraction as an attributed Binary** — "We take this whole-document from deliberately, not as a placeholder." is a defensive justification (preempting "isn't `r` just padding?"). Note: the surrounding Nelson citations [LM 4/41, 4/12, 4/52–4/53] and the statements of what `Observe_R` now matches are load-bearing primary-source attribution and operation-behavior — keep those; only the defensive framing is the accretion.

**Required**: Trim the Single-source aside to a bare deferral or remove it; drop the duplicated label-reminder in Worked illustration (the back-reference is enough); remove the "deliberately, not as a placeholder" defensiveness while preserving the citations and the Observe_R behavior statement.

## OUT_OF_SCOPE

### Topic 1: Runtime / dynamic type registration
**Why out of scope**: The note commits the registry to immutability (P1, written only at `Σ_init` construction). An app that needs to register a new type after the dynamics begin would require a registry-extending transition — a different transition relation that contradicts P1. That is a successor framework, not a defect here; this note is internally complete for the fixed-vocabulary design it states (it even handles the empty-registry, link-inert boundary).

### Topic 2: Operational semantics of the shapes (OQ1–5) and the coverage-vs-span-count design choice
**Why out of scope**: Idem semantics, behavior catalogs, default/composed predicates, and standard registrations are correctly deferred by the note's own Open Questions. The decision to gate on span count rather than coverage (so conformance is representation-sensitive) is an owned design choice the note states plainly in *Shape-conformance*; revisiting whether the gate should instead be coverage-based, or whether every intended contiguous source admits a single-span normal form, is OQ6-adjacent expressiveness territory, not an error in this note.

VERDICT: REVISE
