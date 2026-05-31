# Review of ASN-0043

I reviewed the link-model invariants L0–L14a, the local lemmas (CPP, FSP, FSE, PrefixSpanCoverage, DocVal), and the worked example against the ASN-0034/ASN-0036 foundations. I checked each derivation, the boundary cases, and the forward-reference/anti-bloat patterns flagged for this note.

## REVISE

No REVISE items.

The places where these notes usually fail are all covered here:

- **Boundaries are exercised, not asserted.** Empty from/to endsets with non-empty type (L9 witness `(∅, ∅, {(g,…)})`), arity 3 *and* arity 4 (Steps 3–6), documents with and without prior link allocations (L9 Case A vs Case B), and the singleton-vs-multi-span distinction that L5/L8 actually turn on (Steps 5–6). The L8 *coverage-vs-decomposition* crux — `Θ_split = {(g,δ(1,8)),(g',δ(1,8))}` and `Θ_single = {(g,δ(2,8))}` having equal coverage `[g,h)` but unequal span sets — is the right discriminating test, and the half-open-interval union is checked by trichotomy, not waved through.
- **The L1c chain's strong conjuncts (`k₁=2`, `#tᵢ > #s`) are derived**, not assumed: only `inc(·,2)` moves `zeros` from 2→3, it must be first, and CPP fixes `1..#s` to pin `s = home(a)`. The CPP precondition (`#tᵢ₋₁ > p` on sibling advances) is discharged correctly in each of its three call sites (L1c, FSE, L9 Case A).
- **L11a** correctly grounds in GlobalUniqueness by routing every link chain through a single allocator tree 𝒯 seeded at a T10a document node; the at-most-once child-spawn constraint is respected because content and links share one `inc(d,2)` child allocator and branch only at distinct `(t,1)` pairs.
- **L14a/L14** disjointness is honestly scoped to the `s_C`-resident slice, with the global-constant gap acknowledged in Open Questions rather than papered over.
- `subspace_I` is a genuinely distinct projection from ASN-0036's `subspace` (element-field first component vs whole-tumbler first component), explicitly distinguished — not reinvented foundation notation.

On the anti-bloat axis: the L1b grounding, the L1c postcondition prose, and the FSP bullet structure are all load-bearing on inspection (e.g., L1c's `home(a)`-well-definedness feeds its own next paragraph; L0b's restatement is the canonical citable invariant). I found no forward-reference meta-prose, no document-ordering justifications, and no duplicated paragraphs that survive scrutiny — consistent with the recent rationale-stripping cleanup.

## OUT_OF_SCOPE

None to add. The note already routes operations, transclusion consistency, compound-link well-formedness, and the global content-subspace constant to Open Questions, which is the correct disposition.

VERDICT: CONVERGED
