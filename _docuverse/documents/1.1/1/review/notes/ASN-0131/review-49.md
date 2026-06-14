# Review of ASN-0131

This is a strong, deep note. The core definition (RE-DEF), the touch/overlap discipline, the worked instance, union-distributivity, the one-sided intersection law with its concrete non-injective counterexample, RE-CWP's contraction weakest-precondition, and the retraction deduplication analysis (sole-bearer) all check out under their cited foundation lemmas. I verified the e₃ field-agreement disjointness argument, the `image`-union proof, the RE-SEL reduction to `findlinks_V ∩ addressable`, and the RE-RET forward/backward halves; all are sound. The depth requirements (concrete example, non-trivial wp, derived consequences) are met. Two issues remain.

## REVISE

### Issue 1: The ASN-0086 bridge does not license the two ASN-0086 lemmas it is invoked for

**ASN-0131, "The unit of the answer: anchoring without names"**: "So the link store evolves identically under ASN-0086's transition relation and under ASN-0047's, and every ASN-0086 lemma that constrains `Σ.L` alone holds verbatim at every ASN-0047-reachable state."

**Problem**: The note subsequently rests its entire emission/retraction analysis on two ASN-0086 results that are *not* "Σ.L alone":
- RE-RET cites **R-Scope (SingleTupleScope)**: "a single Nullify contributes *exactly* its target to the nullified set — `{t : ℓ ≼ t} ∩ dom(Σ'.L) = {ℓ}` (R-Scope SingleTupleScope, ASN-0086, arity-independent)". R-Scope's statement quantifies over `d_retr ∈ dom(Σ.M)` and uses `a_emit`.
- The link-emission analysis cites **wp Case 2 (EmitKWeakestPrecondition)**: "settled by `wp` Case 2 (ASN-0086)". Its statement is `wp(Emit_K(Σ, d, F, G), …) ≡ d ∈ dom(Σ.M) ∧ …`, and the derived `a_emit(Σ, d)` is a function of both `Σ.M` and `Σ.L`.

Both lemmas' hypotheses (and `a_emit`) range over `dom(Σ.M)`, so the bridge as written ("constrains Σ.L alone") does not transfer them. The transfer is in fact sound — but only because `dom(Σ.M) = E_doc` is the *same* ASN-0093 document substrate that both ASN-0086 and ASN-0047 extend, so the document operand and `a_emit` read identically under either transition relation. The bridge establishes Σ.L-evolution sameness and stops short of this needed `dom(Σ.M)`-compatibility step, leaving the linchpin of RE-RET and RE-EDIT's emission cases under-justified.

**Required**: Broaden the bridge to cover lemmas whose Σ.L-conclusion follows from the shared `K.λ` semantics, explicitly noting that `dom(Σ.M)` is the common ASN-0093 substrate (so the document operand and `a_emit` are the same object under both relations); or restrict the citations to the Σ.L-only conclusions and re-derive the `dom(Σ.M)`-touching hypotheses inline at the two use sites.

### Issue 2: Forward-reference accretion and defensive scoping prose (anti-bloat)

**ASN-0131, "Composing regions" (RE-UDIST-∩) and "Under retraction"**: the same small sub-fact is reached for by deferring across sections — "(the fresh-`K.λ`-output addressability established under *link emission* below)" and, later, "by the general fresh-`K.λ`-output addressability established under link emission above".

**Problem**: Two paragraphs in different sections defer to the same downstream location for one reusable fact (non-self-targeting fresh `K.λ` output ⟹ addressable in its post-state) — the flagged deferral-chain pattern. A secondary instance is the defensive scoping in the worked instance: "the example needs exactly `coverage(e₃) ∩ dom(Σ.C) = ∅` — and the argument runs over content addresses alone, the only addresses we intersect `coverage(e₃)` with." This explains *why the proof suffices* rather than simply proving the disjointness.

**Required**: Establish the addressability sub-fact once as a named lemma before first use and cite it from both sites (eliminating the below/above pointers); and in the worked instance, state and prove `coverage(e₃) ∩ dom(Σ.C) = ∅` directly, dropping the meta-commentary on sufficiency.

## OUT_OF_SCOPE

The note's Open Questions (rendered-answer mode OQ3, intersection-equality-under-injectivity OQ4, non-co-resident link store OQ5, type-slot-against-content OQ6, link-subspace regions OQ7) correctly defer future territory rather than leaving gaps in RE's specification; none of these is a REVISE item. The conditional insert/delete (ASN-0082) stability analysis reaches slightly beyond ASN-0047's atomic vocabulary, but it is explicitly marked conditional on the natural-lift assumption and serves RE's stability narrative, so it is acceptable in-scope rather than future work.

VERDICT: REVISE
