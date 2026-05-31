# Review of ASN-0093

## REVISE

### Issue 1: T7 cited under a reinvented name
**ASN-0093, multiple sites (L14 derivation, FirstEmissionFreshness, Cross-document disjointness, worked example, Properties table)**: "T7 (FirstElementFieldDistinction, ASN-0034)"
**Problem**: Foundation T7 is named **SubspaceDisjointness**, not "FirstElementFieldDistinction." The ASN consistently substitutes its own label for a foundation property. This is exactly the renaming Standard 7 forbids: use the foundation's name, do not reinvent it. The substance (precondition zeros=3 + T4-validity, postcondition `a.E₁ ≠ b.E₁ ⟹ a ≠ b`) is applied correctly, but the citation name is wrong everywhere it appears.
**Required**: Rename all citations to T7 (SubspaceDisjointness, ASN-0034).

### Issue 2: `b_C(d) = inc(d, 2)` silently assumes `s_C = 1`
**ASN-0093, Address sub-allocators**: "b_C(d) = inc(d, 2) (TA5(d), k = 2)"
**Problem**: `b_C(d)` is *defined* as `[d.0.s_C]`, but TA5(d) at `k=2` produces `[d.0.1]` (k−1 zeros then a final `1`). The equality `inc(d,2) = b_C(d)` holds only because `s_C = 1`. The parallel link step `inc(b_C(d), 0) = b_L(d)` *does* explicitly flag its dependency ("depends substantively on `s_L = s_C + 1`"), but the content-anchor identity leaves the `s_C = 1` dependency on SubspaceConventionAxiom unstated. Inconsistent rigor between two structurally identical anchor-construction steps.
**Required**: Note that `inc(d,2) = [d.0.s_C]` rests on `s_C = 1` (SubspaceConventionAxiom), matching the citation discipline applied to the `b_L(d)` step.

### Issue 3: Duplicated `dom(M') = dom(M)` rationale (anti-bloat)
**ASN-0093, K.α and K.λ Frame paragraphs**: both contain "The explicit `dom(M') = dom(M)` clause makes domain equality unambiguous alongside the pointwise function equality. Under partial-function semantics the two together force `M' = M`, so C2 and L1a at `Σ` transfer to `Σ'` directly..."
**Problem**: The same justification appears verbatim (modulo `a'`/`ℓ'`) in two adjacent operation definitions — two paragraphs saying the same thing. The frame clause `dom(M') = dom(M); (A d' :: M'(d') = M(d'))` is already self-evident; the surrounding prose explains *why the notation is unambiguous* rather than advancing reasoning.
**Required**: State the `M' = M` consequence once (e.g., in the shared primitive preamble) and drop the second copy.

### Issue 4: Downstream-consumer inventory in Cross-document disjointness lemma (anti-bloat)
**ASN-0093, Cross-document disjointness chain**: "...the T10 any-extension claim above is the strictly stronger form, and it is what FirstEmissionFreshness's cross-document branch consumes."
**Problem**: The trailing clause is a use-site inventory — it names a downstream consumer rather than advancing the lemma. This is the flagged pattern "a definition's introduction enumerates downstream consumers." The strength distinction (T10 form vs B7 corollary) is the substantive content; the consumer pointer is not.
**Required**: Drop "and it is what FirstEmissionFreshness's cross-document branch consumes."

### Issue 5: Repeated "state-independent citations need no per-transition discharge" (anti-bloat)
**ASN-0093, Per-chain disciplines intro and Discharge section**: "Their conclusions are determined per-chain and not by system state, so as ASN-0040 citations they require no per-transition discharge" vs. "The chain-indexed disciplines stand apart: they are state-independent ASN-0040 citations, determined per-chain rather than per-transition."
**Problem**: The same claim restated in two sections in different words.
**Required**: Keep one occurrence; remove the other.

### Issue 6: Forward-reference Terminology paragraph (anti-bloat)
**ASN-0093, State model, Terminology**: "A higher-layer entity-hierarchy refinement (e.g., `IsDocument(e) ∧ e ∈ E`) is a strict tightening: every document admitted by that refinement is a substrate document, but the substrate admits documents that may not pass the higher-layer entity-hierarchy discipline."
**Problem**: This is meta-prose about deferred machinery (entity stratification, explicitly out of scope). It explains the substrate's relationship to a future layer rather than advancing the substrate definition. The operative definition ("Document = element of `dom(M)`") stands without it.
**Required**: Remove the higher-layer-refinement sentence; the structural definition suffices.

## OUT_OF_SCOPE

### Topic 1: Document-address allocation discipline
The substrate gates `K.σ` only on `d ∉ dom(M) ∧ T4-valid(d) ∧ zeros(d) = 2`; it imposes no allocator chain on document tumblers themselves (unlike content/link sub-allocators). This is correct for a substrate boundary — node/user-level allocation belongs to a higher layer — not an error here.

### Topic 2: Concurrent emission discipline
SequentialTransitionAxiom forces total ordering; multi-allocator concurrency is correctly listed under Open Questions for a future ASN.

VERDICT: REVISE
