# Review of ASN-0082

## REVISE

### Issue 1: "Why the axiom is needed" essay around NAT-comm
**ASN-0082, The Ordinal Shift / pre–Span-Width-Preservation block**: 

> "**Commutativity** (`m + n = n + m`) is *not* supplied by any foundation statement. ASN-0034's arithmetic extraction names NAT-addcompat (order-compatibility, strict successor), NAT-closure (closure, additive identity), NAT-discrete, NAT-order, and NAT-wellorder, and none of these asserts commutativity; nor is it derivable from them, since `+` is given as a primitive binary operation with no successor-recursive characterization (the extraction supplies `0 + n = n` but not `n + 0 = n`, and no `n + (m + 1) = (n + m) + 1`)."

and

> "This is a standard property of the standard natural numbers that T0 (ASN-0034) fixes as the carrier; we introduce it here as a clearly-labeled local axiom rather than cite a foundation statement that does not assert it."

**Problem**: This is the flagged anti-bloat pattern — prose around an axiom that explains *why the axiom is needed* and *why it is posited locally* rather than what it says. The non-derivability argument (primitive `+`, no successor-recursion, "`0 + n = n` but not `n + 0 = n`") and the closing justification-of-choice sentence do not advance any proof. The leading sentence "We source each precisely rather than attribute both to T0, whose axiom fixes only the carrier..." is also citation-hygiene meta-prose.
**Required**: Reduce to the axiom statement plus one sourcing sentence (e.g., "ASN-0034's NAT-* axioms do not include commutativity, so we posit it locally"). Keep the **Associativity** paragraph — its depth-1 specialization of TA-assoc is load-bearing — but drop the derivation-impossibility argument and the standard-property justification.

## OUT_OF_SCOPE

### Topic 1: ℕ commutativity belongs in the foundation, not a downstream local axiom
**Why out of scope**: The carrier ℕ and its arithmetic are fixed by ASN-0034 (T0 + the NAT-* extraction). If commutativity is genuinely needed and genuinely absent, the architecturally correct home is ASN-0034's NAT-* set — otherwise every downstream ASN that touches ℕ addition must re-axiomatize it. Adding NAT-comm to the foundation is an ASN-0034 change, not a revision to ASN-0082; the local axiom here is an acceptable stopgap but flags a foundation gap to route upstream.

### Topic 2: Depth > 1 ordinal generalization
**Why out of scope**: The contraction half is scoped to `#p = 2` (single-component ordinals) by the depth axiom, and the ASN's Open Questions already record the depth->1 generalization (TA4's zero-prefix precondition colliding with S8a positivity at intermediate components). Correctly deferred.

---

The mathematics is sound throughout: I3/I3-V consistency (injectivity via TS2, strict advance via TS4), the ord/vpos homomorphism (OrdAddHom), gap-closure (D-SEP via TA4 at depth 1), the cardinality chain in D-SEQ-post (|L∪Q₃| = N − c), and both span-width derivations (I3-S, D-S) all check out, and the boundary coverage (insert-at-start/end/empty, contraction L=∅/R=∅/full-deletion, cross-subspace) is comprehensive. The sole finding is prose accretion around the NAT-comm axiom.

VERDICT: REVISE
