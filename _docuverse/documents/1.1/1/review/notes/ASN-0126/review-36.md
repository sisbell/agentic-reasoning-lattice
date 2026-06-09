# Review of ASN-0126

The mathematics is careful: the projection bridge, the wp refinement, P6's lift, and the born-nullified worked example all hold up under scrutiny, and the address arithmetic in the illustration checks out. My findings are confined to the anti-bloat surface this note is flagged for — accumulated meta-prose and duplicated argument.

## REVISE

### Issue 1: The Sh-conf state-independence counterfactual is stated twice in near-identical form
**ASN-0126, Shape-conformance**: "Were it to, a ghost reference at one state and a stored reference at a later state would yield different verdicts, destroying the state-independence we want (P5)."
**ASN-0126, Worked illustration (State-independence, with ghosts)**: "Had `Sh-conf` enforced a residence domain, the ghost references at `Σ` would have flipped the verdict to `⊥` while `Σ'` returned `⊤`, contradicting P5."
**Problem**: These are the same counterfactual ("if Sh-conf consulted residence → P5 breaks") in different words — the pattern "two paragraphs say the same thing." The worked illustration's *concrete instantiation* (citation over `c₁/c₂/c₃` at `Σ`/`Σ'`) is valuable and should stay; the abstract counterfactual sentence inside it merely re-litigates the Shape-conformance design decision.
**Required**: Keep the counterfactual in Shape-conformance (where the decision is made). In the worked illustration, state only the concrete result — Sh-conf returns ⊤ at both states — and drop the "Had Sh-conf enforced a residence domain…" restatement.

### Issue 2: Single-source carries defensive framing and introduces a structural property (P7) in a discursive aside
**ASN-0126, Single-source**: "This is a genuine, narrow loss of expressiveness." … "What is *not* lost is attribution… so the framework can supply a one-span source in place of the empty one and lose nothing." … "the reachable-state conformance invariant we raise to P7."
**Problem**: The "genuine narrow loss" / "lose nothing" prose is defensive justification of a design tradeoff, not reasoning that advances the construction — the load-bearing content is just the wrapper `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})` and `R` being Binary. Separately, P7 (a structural property with its own slot in Properties established) is named and motivated here, far from its statement — essay content occupying the retraction discussion.
**Required**: Reduce the retraction reconciliation to the construction itself (empty-F Nullify has no `→_sh` image; the canonical fill is `r = (d_retr, δ(1, #d_retr))`; R is registered Binary; `nullified`/`L_R` read only `coverage(G')` so they carry over). Drop the "lose nothing"/"genuine narrow loss" framing and let P7 be introduced where it is stated.

## OUT_OF_SCOPE

### Topic 1: Idem-flag operational semantics
**Why out of scope**: The note registers the `idem` field and proves its stability (P3) without assigning it behavior. Defining the registry structure now and deferring "same-as-active" semantics to the successor note (Open question 1) is the correct boundary, not a defect — P3 is the same argument as P2 applied to the field, and that is all this framework needs.

META: not applicable — the ASN defines a state component (registry), a refined operation (the gated emit), and state invariants (P1–P7) at the right level of abstraction; it has not drifted into implementation mechanics.

VERDICT: REVISE
