# Channel Assignment — ASN-0082 review-25

**Date:** 2026-05-15 08:23

```
## Issue 1: Foundation invariants D-CTG, D-MIN, D-SEQ restated in generalized form inconsistent with foundation
Reason: The reviewer explicitly notes that the generalization-with-justification path would contradict the foundation's "sparse with tombstones" frame note, leaving only the path of restating exactly as the foundation has them — a citation-correction internal to the ASN ecosystem. No design intent or implementation evidence is needed; the fix is to read ASN-0036 and reproduce its qualifiers verbatim.
```

```
## Issue 2: Contraction operation depends on the generalized invariants without justification
Reason: Follows directly from Issue 1's resolution. The ASN already cites Literary Machines establishing that DELETEVSPAN is byte-stream-only (in the scoping axiom discussion), so restricting the contraction's preconditions to S = 1 is derivable from material already present in the ASN.
```

```
## Issue 3: D-MIN-post over-asserts for subspaces where D-MIN doesn't apply
Reason: Mechanical consequence of Issue 1 — once D-MIN is restored to its text-only foundation form, D-MIN-post must mirror that restriction. The proof's "L ≠ ∅" case cites D-MIN, so the scope of the lemma simply tracks the scope of the cited invariant.
```

```
## Issue 4: D-BJ proof references "established above" without explicit derivation in proof
Reason: Pure proof-rewriting task. The chain `ord(v) ≥ ord(r) = ord(p) ⊕ w_ord ≥ w_ord` is assembled from already-cited foundation lemmas (OrdinalOrderEquivalence, OrdAddHom, plus TA-dom/NAT-addbound from ASN-0034); inlining requires no external context.
```

```
## Issue 5: I3-C frame is incompatible with any operation that actually adds content
Reason: The ASN itself resolves the framing question by stating "the content-placement postcondition is an operation-level concern deferred to a future INSERT ASN." The fix is to align the setup prose with this existing scoping decision, scoping I3 as the shift sub-operation — entirely internal.
```

```
## Issue 6: Worked example doesn't include a non-text subspace case
Reason: A multi-subspace pre-state can be constructed abstractly from the ASN's own definitions (V-positions are tumblers [S, ordinal] with S ≥ 1) without needing implementation specifics. The verification of I3-X is structural — any link-subspace position mapped to any I-address suffices to demonstrate preservation.
```

```
## Issue 7: No weakest-precondition analysis for any of the introduced lemmas
Reason: WP analysis is a proof technique applied backwards from postconditions through the operation's effect. All the inputs needed (I3, I3-VP, shift definition, S8a) are already present in the ASN; the calculation is mechanical predicate transformation, not requiring external evidence or intent.
```

```
## Issue 8: D-SEQ-post relies on the D-SEQ derivation in ASN-0036 without confirming preconditions in the post-state
Reason: The missing fourth precondition (S8a) is established as S8a-post in the same ASN — citation is purely internal bookkeeping. The general-S concern reduces to Issue 1's foundation-matching fix.
```
