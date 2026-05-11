# Channel Assignment — ASN-0036 review-73

**Date:** 2026-05-10 23:10

## Issue 1: Undefined `fields(a)` notation
Reason: Pure notation fix — T4b in the foundation already provides `N(t), U(t), D(t), E(t)` projections. Replacement is mechanical per standard 7; no external context needed.

## Issue 2: Ambiguous `v > 0` notation
Reason: Pure notation fix — TA7a's set `S` is the foundation-supplied form, and the redundancy with `zeros(v) = 0` is derivable from T0 and NAT-zero. Internal cleanup only.

## Issue 3: `ord(v)` precondition mismatch with V-position guarantees
Reason: The fix requires committing to whether V-positions are universally `#v ≥ 2`. The ASN already cites Gregory's depth-2 evidence for the text subspace and ValidInsertionPosition encodes `m ≥ 2`; strengthening S8a uses reasoning already present. Internal.

## Issue 4: D-SEQ depth precondition not enforced by S8-depth
Reason: Same coupling as Issue 3 — strengthening S8-depth to require `#v ≥ 2` is consistent with the ValidInsertionPosition empty-case construction and Gregory's cited depth-2 evidence already in the ASN. Internal.

## Issue 5: D-CTG applicability to link subspace not addressed
Reason: The ASN explicitly defers link-subspace semantics but uses universal quantification over `S` in D-CTG/D-MIN/D-SEQ. Scoping requires knowing Nelson's design intent for link arrangement structure and Gregory's evidence on how the link subspace is actually populated.
Nelson question: Did Nelson intend the link subspace's V-positions to be dense and contiguous (like the text subspace), or sparse/keyed by some other principle that would make D-CTG and D-MIN inapplicable?
Gregory question: In udanax-green, does the link subspace populate V-positions contiguously starting at ordinal 1 (like text), or does it use some other allocation pattern (sparse, keyed, addressed by content)?

## Issue 6: `m = 1` case glossed in S8 within-subspace uniqueness
Reason: Pure proof-completeness fix — at `m = 1`, V_S(d) ⊆ {[S]} is immediate from T3, making within-subspace uniqueness vacuous. The edge case is derivable from existing ASN content.

## Issue 7: `+ k` notation overloaded with NAT addition
Reason: Notational disambiguation only — the ASN already defines `shift(v, k)` and `v ⊕ δ(k, m)` as alternatives. Internal cleanup.

## Issue 8: T5 cited under non-canonical name
Reason: Citation fix — foundation's canonical name is `ContiguousSubtrees`; the change is mechanical per standard 7. Internal.
