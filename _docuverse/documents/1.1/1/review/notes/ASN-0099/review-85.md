# Review of ASN-0099

I checked the two-phase factoring (image / findlinks / findlinks_V), the match-predicate individuation (F4), the preservation suite (F8, F9, F9-λ, F11, F19), the additivity/scope results (F13, F14, F15, F20, F20a), and the six-query worked example. The mathematics is sound: the F13 existential-over-disjunction lift is explicit, the F4 strengthening/weakening witnesses check out per slot, the recovery identity (`findlinks` as a union over single-slot filters) is proved per-link with the guard-collapse justified, and the worked example evaluates correctly at each query (including the cross-subspace meta-link in Query 4 and the F9/F11/F9-λ chains in Queries 5–6). Edge cases — empty `I`, empty `dom(Σ.L)`, empty constraint set, empty-target constraint, `R` disjoint from the arrangement — are all covered. All inter-ASN references are to foundation ASNs (0034, 0036, 0043, 0047, 0058, 0093, 0098), so none violate the self-containment rule.

One anti-bloat finding remains.

## REVISE

### Issue 1: "Local Atomicity" section is why-the-axiom-is-needed rationale, not object-level content
**ASN-0099, "Local Atomicity and the Single-State Setting"**: "By SequentialTransitionAxiom (ASN-0093), every state transition is atomic and uninterruptible, so Σ is well-defined at every query point — the single-state reading every claim in this ASN assumes."

**Problem**: This standalone section advances no FINDLINKS claim. It restates a foundation axiom (ASN-0093's atomicity) and concludes that `Σ` is well-defined — a justification for *why* the single-state reading is licensed, rather than a statement of what FINDLINKS does. Every claim in the ASN already quantifies over a fixed `Σ`; none of their correctness derivations invoke this section. This is precisely the flagged accretion pattern — new prose around an axiom explaining why the axiom is needed here. The section is removable without loss to any claim.

**Required**: Delete the section. If the single-state setting must be noted, fold it into a one-clause aside at the point of first use (e.g., where `Σ` is introduced in the Completeness signature), rather than a dedicated section whose only function is axiom rationale.

## OUT_OF_SCOPE

None. The "What We Have Not Specified" list (procedure, replication/consistency, caching, FOLLOWLINK inverse, combined filtered-and-scoped form) correctly defers genuinely new territory, and the Open Questions on auditability and post-K.λ timing are appropriate to leave open.

VERDICT: REVISE
