# Citation Resolve — ASN-0036/NAT-induction — run 1

*2026-06-29T14:29:42Z*
*Model: sonnet*

## Output

The D-INJ proof confirms the real names of the NAT-* labels. Now I can analyze what's unclassified in the prose.

The prose mentions five labels not in the currently-classified lists: **NAT-order**, **NAT-discrete**, **NAT-wellorder**, **NAT-cancel**, **NAT-addcompat** — all appearing as parenthetical identifiers of existing NAT-* axioms the claim supplements, not as logical inputs to NAT-induction's correctness. The Formal Contract explicitly lists only NAT-carrier, NAT-zero, NAT-closure as Depends; the other five are background context for the reader. All currently-classified entries remain valid.

```
CLASSIFICATIONS:
- label: NAT-order
  direction: forward
  bullet: "- NAT-order (NatStrictTotalOrder, ASN-0034) — named as an existing NAT-* group axiom in the motivating context; cited alongside NAT-discrete and NAT-wellorder to show what the group already supplies (strict total order), emphasising by contrast that generation-from-`0` is the missing piece; the claim's axiom does not rest on it"

- label: NAT-discrete
  direction: forward
  bullet: "- NAT-discrete (NatDiscreteness, ASN-0034) — named as an existing NAT-* group axiom in the motivating context; cited as part of the completeness picture of what NAT-* covers (the discretely well-ordered carrier) to frame what NAT-induction adds; the claim's axiom does not rest on it"

- label: NAT-wellorder
  direction: forward
  bullet: "- NAT-wellorder (NatWellOrdering, ASN-0034) — named centrally in the motivating argument; the prose exhibits the `ω · 2` counterexample to show that well-ordering alone does not exclude successor-unreachable elements and hence does not underwrite induction, making explicit why NAT-induction is a genuinely new posit; the claim's axiom does not rest on it"

- label: NAT-cancel
  direction: forward
  bullet: "- NAT-cancel (NatAdditionCancellation, ASN-0034) — named as an existing NAT-* group axiom in the motivating context; cited as part of the cancellative-addition cluster to show the group's existing coverage and frame what NAT-induction augments; the claim's axiom does not rest on it"

- label: NAT-addcompat
  direction: forward
  bullet: "- NAT-addcompat (NatAdditionOrderAndSuccessor, ASN-0034) — named as an existing NAT-* group axiom in the motivating context; cited alongside NAT-cancel, NAT-closure, and NAT-zero as the ordered-cancellative-addition axioms the NAT-* group already covers; the claim's axiom does not rest on it"

RETRACTIONS: []
```
