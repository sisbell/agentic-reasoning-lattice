# Channel Assignment — ASN-0094 review-2

**Date:** 2026-05-19 19:41

```
## Issue 1: Sh-conf scope ambiguous (Emit_K vs K.λ)
Reason: This is a design-intent question about where the substrate/layer boundary sits for conformance enforcement. The proofs cite K.λ but Sh-conf is stated against Emit_K; resolving requires knowing the intended binding level.
Nelson question: Was shape-conformance intended to be enforced at the substrate primitive K.λ directly (rejecting any class-(iii) emission of a registered type with non-conformant F/G), or as a relational-layer commitment that all class-(iii) emissions of registered types route through Emit_K?
```

```
## Issue 2: Sh4 enforcement strategy not formalized
Reason: Whether idempotency should be lifted to a substrate axiom or remain a layer discipline is both a design-intent question (Nelson: what was intended) and an evidence question (Gregory: how udanax-green handles single-active-duplicate constraints).
Nelson question: For `idem = ⊤` shapes, was duplicate-suppression intended to be a substrate-level rejection at emission time, or a higher-layer policy that the substrate trusts but does not check?
Gregory question: Does udanax-green enforce any single-active-duplicate constraint at the link-store layer for relation-like structures, or is duplicate-suppression handled entirely by callers above the link store?
```

```
## Issue 3: AllocatedAddressAntichain Case 3 dependencies
Reason: The fix is a citation-discipline adjustment — state the content-side properties as preconditions of the lemma or restructure the case analysis. Derivable from the ASN's own framing without external input.
```

```
## Issue 4: Cross-ASN references to ASN-0093 throughout
Reason: Citation-discipline fix; the ASN can lift the needed scaffolding into a preamble or consume properties through ASN-0086's interface. Internal to the document.
```

```
## Issue 5: Multi-arity scope not declared
Reason: ASN-0086 already restricts L^Σ to arity-3 links and explicitly excludes higher-arity links from scope. The shape framework inherits this; the fix is a one-sentence scope statement derivable from the foundation list.
```

```
## Issue 6: Worked example shows only successful emissions
Reason: The rejection cases are constructible directly from Sh-conf's clauses (non-canonical span, cardinality mismatch, unallocated target). No external input needed to draft the new cases.
```

```
## Issue 7: Sh0/Sh1 verification in worked example is hand-wavy
Reason: Expanding the "by direct check ✓" into explicit per-tuple verification uses only data already in the example. Internal.
```

```
## Issue 8: Coverage shape from-slot semantics under-explained
Reason: The from-slot's semantic role in Coverage relations is a design-intent question — why does a (1, 1, A_doc, A_doc, ⊥) Coverage shape require a from-slot that no template consumes? Nelson can clarify the intended attribution.
Nelson question: For Coverage-shaped relations whose templates (`latest_K_for_addr`) do not consume the from-slot, what was the from-slot intended to identify — the witness/reviewer document, the home document, or something else — and why is it required rather than `c_F = 0`?
```

```
## Issue 9: Comment-Resolution co-registration not formalized
Reason: How a Comment relation pairs with its Resolution relation is a design choice — co-registration in the shape registry vs explicit parameter vs default semantics. Nelson's intent determines which formulation matches the framework's design.
Nelson question: For a Comment-shaped relation K paired with a Resolution-shaped relation K_res, was the design intent that K declare K_res in the shape registry (per-K co-registration), that K_res be an explicit parameter to templates like `unresolved_K_comments_via(K_res, d)`, or that all active Resolution tuples targeting τ count as resolving it?
```

```
## Issue 10: Conformance monotone-discharge argument leans on unstated content-store monotonicity
Reason: Same citation-discipline fix as Issues 3/4 — the content-store monotonicity precondition can be stated as an assumed substrate invariant in ASN-0094's own preamble. Internal.
```
