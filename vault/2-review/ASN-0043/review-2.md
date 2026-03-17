# Review of ASN-0043

## REVISE

### Issue 1: L13 — Span `(b, [1])` analysis is wrong
**ASN-0043, Reflexive Addressing**: "`(b, [1])` is a well-formed span referencing exactly the link at address b"
**Problem**: The displacement `[1]` is a single-component tumbler with action point `k = 1`. By TumblerAdd (ASN-0034), `b ⊕ [1] = [b₁ + 1]` — a single-component result. The span `(b, [1])` therefore covers `{t ∈ T : b ≤ t < [b₁ + 1]}`, which is every tumbler from `b` up to the next node boundary — potentially all remaining users, documents, and content under node `b₁`. The claim that this references "exactly" one link is wrong by orders of magnitude.

A secondary issue: no span in the tumbler ordering covers exactly one point. The ordering is dense — between any address `a` and any `a'` where `a ≼ a'`, there exist infinitely many tumblers (extensions of `a`). Even with a corrected displacement (action point at `#b`), the span `(b, ℓ)` covers `b` and all its extensions.

**Required**: Use a displacement with action point at `#b` (e.g., `ℓ` with `#ℓ = #b`, zero everywhere except position `#b` where the value is 1). Retract the "exactly" claim — state instead that the span's coverage includes `b`, and define what it means for an endset to reference a single entity when spans are interval-based.

### Issue 2: L10 — Derivation gap from contiguity to span expressibility
**ASN-0043, The Type Endset**: "By T5 (ContiguousSubtrees, ASN-0034), `subtypes(p)` is a contiguous interval under T1. Therefore there exists a span `(p, ℓ)` such that: `(A c : p ≼ c : c ∈ coverage({(p, ℓ)}))`"
**Problem**: T5 establishes that the prefix set is contiguous. The existence of a covering span requires additional steps: (1) the upper bound of `{t : p ≼ t}` under T1 is `inc(p, 0)` (TA5(c)); (2) this equals `p ⊕ ℓ` where `ℓ` has action point at `sig(p)` with value 1; (3) the resulting span is well-formed by T12. The Gregory example (FOOTNOTE at `1.0.2.6`, MARGIN at `1.0.2.6.2`, query range `[1.0.2.6, 1.0.2.7)`) concretely demonstrates the claim but does not substitute for the derivation.
**Required**: Show the construction. Identify the upper bound as `inc(p, 0)`, express it as `p ⊕ ℓ` for a specific `ℓ`, and verify T12.

### Issue 3: L9 is a consequence of L4 but presented as independent
**ASN-0043, The Type Endset**: "The type endset may reference addresses at which no content exists: `¬ [(A a ∈ dom(Σ.L), (s, ℓ) ∈ Σ.L(a).type :: coverage({(s, ℓ)}) ⊆ dom(Σ.C))]`"
**Problem**: L4 already establishes that the only structural constraint on any endset span (including type endset spans) is T12 well-formedness. L4's prose explicitly states "no constraint confining spans to ... addresses at which content currently exists." L9 is a direct consequence of L4 applied to the type endset, but is presented as an independent property without derivation.
**Required**: Either derive L9 from L4 (one sentence: "By L4, no existence constraint governs endset spans; for the type endset specifically, this permits ghost addresses") or merge L9 into L4 as a noted consequence.

### Issue 4: L7 is a design principle, not a formalizable property
**ASN-0043, Slot Distinction and Directionality**: "The semantic interpretation of from-endset versus to-endset is a function of the link type, not a fixed property of the link structure."
**Problem**: The specification models state and invariants, not "semantic interpretation." L7 cannot be checked against a state or state transition. Yet it appears in the formal properties table alongside checkable invariants like L6 and L8.
**Required**: Reformulate as a negative property of the specification itself: "The invariants L0–L14 impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure." This says the same thing but is verifiable by inspection of the invariant set.

## OUT_OF_SCOPE

### Topic 1: Compound link well-formedness
**Why out of scope**: L13 establishes that links can reference other links, enabling compound structures. The ASN's Open Questions acknowledge that well-formedness constraints for such structures (cycle avoidance, depth bounds, interpretability) are unaddressed. This is new structural territory beyond what the ontology needs to establish — the ontology says compound links are *possible*; a future ASN should say which compound forms are *valid*.

### Topic 2: Coverage equivalence and query semantics
**Why out of scope**: The ASN correctly notes that distinct endsets can have identical coverage, and the Open Questions ask when coverage-equivalent endsets should be treated as equal. This is a question about the query interface, not the ontological structure. L8's `same_type` uses span-set equality, which is the right choice at the structural level; whether a more relaxed notion is needed for search belongs in a query-semantics ASN.

VERDICT: REVISE
