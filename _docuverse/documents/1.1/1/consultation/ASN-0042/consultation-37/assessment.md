# Channel Assignment — ASN-0042 review-37

**Date:** 2026-05-14 04:23

```
## Issue 1: O8 proof — notational error on π's membership
Reason: Pure notational/logical fix internal to the proof. The convention is established in the Delegation Definition, and `π' ∈ Π_{Σ'}` is already a hypothesis of O8 — either delete the redundant derivation or correct the membership step using only existing definitions.
```

```
## Issue 2: O7(c) cites the wrong source for non-extension
Reason: Citation correction internal to the ASN. The correct source — condition (vi) of the delegation relation — is already stated in the Delegation Definition; just swap the citation.
```

```
## Issue 3: NestingByDelegation IH application hand-waves chain preservation
Reason: Proof tightening using facts already present (O13 for prefix immutability, path-prefix preservation of delegation events). No external evidence required.
```

```
## Issue 4: O18 bootstrap clause organization
Reason: Organizational decision about where to place an already-stated bootstrap clause. Either O14's clause list or an explicit sub-axiom of O18 — purely a presentation choice.
```

```
## Issue 5: O11 stated as a "property" but provides no formal contract
Reason: Reframing decision internal to the ASN. The design-intent posture ("Nelson silent on authentication") and implementation evidence (`validaccount` stub) are already cited; the choice between scope note and formal binding relation is a modeling/presentation choice within those constraints.
```

```
## Issue 6: Recursive delegation depth argument cites T0(b) without zero-count refinement
Reason: Internal proof work using T0(a) + T0(b) of ASN-0034 plus the existing zero-count constraint from condition (iv). All ingredients are already in the dependency lattice.
```

```
## Issue 7: O5 well-formedness for prefix not yet in Σ.B
Reason: Internal corollary derivation from O5 + O12 + O13 + O2 — the same combination already exercised in O4's inductive step. Just centralize it or remove the unsupported assertion.
```
