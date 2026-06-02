# Review of ASN-0047

I read the full transition model. The mathematical content is sound: the per-state/composite-boundary partition is well-drawn, the K.μ~ admissibility clauses (iv)/(v) independence arguments are genuine, the K.δ-ID structural identities discharge the parent/zeros side-conditions correctly, and the worked examples exercise the real boundaries (interior replacement, k=0 subsequent-version fork, link suffix contraction, orphan link). Foundation citations are confined to 0034/0036/0043/0045/0093. My findings are confined to the anti-bloat / forward-reference accretion the note's classifier asks me to surface.

## REVISE

### Issue 1: Meta-prose announcing storage location, plus repeated deferral to one downstream section
**ASN-0047, K.δ case (ii)**: "*Per-k freshness mechanism (stated once here).* The freshness conjunct is a caller-checked guard in every sub-case…" and, in the same case-(ii) preamble, "the spawn-admissibility conjuncts … are discharged in §*K.δ case (ii) discharge and parent-allocator activation*."
**Problem**: "(stated once here)" announces *where* content lives rather than advancing the claim — the flagged "stated once" bookkeeping pattern. Worse, two separate paragraphs in the K.δ definition (the case-(ii) intro and the per-k mechanism block) both defer the actual discharge to the same downstream section §*K.δ case (ii) discharge and parent-allocator activation*. A reader following the freshness/spawn argument must hold two forward pointers to one location, the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Either inline the per-sub-case discharge at the K.δ definition or move the whole case-(ii) precondition body into the discharge section, leaving a single pointer — not a meta-announcement plus two deferrals.

### Issue 2: Range-preservation-under-K.μ~ argument restated in three places
**ASN-0047**: The fact that K.μ~ leaves `ran(M(d))` (hence `Contains_C`) unchanged appears three times: (a) J3 — "Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ)"; (b) end of *Decomposition of K.μ~* — "Since K.μ~ preserves ran(M(d)), ran(M'(d)) \ ran(M(d)) is empty, and the J1★ coupling has no new containment pairs to record"; (c) Class (b) P4★ discharge — "K.μ~ preserves Contains_C exactly … applying the bijection equation … gives the range equality … hence Contains_C(Σ') = Contains_C(Σ)."
**Problem**: Three paragraphs in three sections assert the same load-bearing fact, one of them (c) re-deriving it from the bijection equation that (b) already invoked. This is the "two paragraphs say the same thing in different words" pattern, compounded.
**Required**: Derive range-preservation once (the (c) derivation is the complete one), and have J3 and the K.μ~ decomposition note cite that single result rather than re-asserting it.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal (renumbering-aware contraction)
**Why out of scope**: Already correctly logged as an Open Question; K.μ⁻'s suffix-only link contraction is a deliberate scoping choice, with link permanence discharged independently by L12 on `dom(L)`. New territory for a future ASN, not an error here.

VERDICT: REVISE
