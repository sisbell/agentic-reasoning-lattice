# Review of ASN-0036

## REVISE

### Issue 1: subspace_I postcondition (c) dependency list incomplete
**ASN-0036, subspace_I Formal Contract, Depends line**: "NAT-sub, NAT-order (ASN-0034) — license the position-arithmetic step `#a − #E(a) + 1 < #a` in postcondition (c)"
**Problem**: The step `#a − #E(a) + 1 < #a` is *not* discharged by NAT-sub and NAT-order alone. To derive it from `#E(a) ≥ 2` one needs at minimum: (a) NAT-addcompat for the strict successor clause `1 < 2` and for left order compatibility lifting `1 ≤ #E(a)` to `(#a − #E(a)) + 1 ≤ (#a − #E(a)) + #E(a)`; (b) NAT-cancel for the strict-to-strict lift (NAT-addcompat alone gives only `≤`-to-`≤`); (c) NAT-closure for the numeral identity `2 = 1 + 1` underlying the `1 < 2` step. The brief two-line gloss `#a − #E(a) + 1 ≤ #a − 1 < #a` also requires anti-monotonicity of subtraction in the subtrahend, which is not directly axiomatised by NAT-sub. S7c's parallel statement `#a − δ + 1 < #a` (Consequence (b)) lists all four axioms explicitly: "NAT-sub, NAT-order, NAT-addcompat, NAT-cancel — license the position-arithmetic step." The omission in subspace_I is an inconsistency within the ASN.
**Required**: Extend subspace_I's dependency list to match S7c (b) — at minimum NAT-addcompat and NAT-cancel; expand the two-line derivation to the cleaner `(#a − #E(a)) + 1 < (#a − #E(a)) + #E(a) = #a` form so it visibly invokes only what NAT-sub directly provides.

### Issue 2: D-CTG-depth alternative-construction parenthetical mislabels NAT-closure identity
**ASN-0036, D-CTG-depth proof, alternative-construction parenthetical**: "which NAT-closure's left identity `(v₁)ⱼ₊₁ + 0 = (v₁)ⱼ₊₁` rewrites to `(v₁)ⱼ₊₁ < (v₁)ⱼ₊₁ + (i + 1)`"
**Problem**: NAT-closure (ASN-0034) axiomatises *two* additive identities: left `0 + n = n` and right `n + 0 = n`. The identity `(v₁)ⱼ₊₁ + 0 = (v₁)ⱼ₊₁` has the literal `0` on the *right* of the operator, so it is the right identity. The proof labels it as "left identity," which is the form `0 + n = n`.
**Required**: Replace "left identity" with "right identity" in this clause.

## OUT_OF_SCOPE

(None — the Scope section and Open Questions list already delimit boundaries cleanly; deferred topics like subspace alignment, link-subspace contiguity, and per-operation D-CTG preservation are explicitly flagged in the body and Open Questions.)

VERDICT: REVISE
