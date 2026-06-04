# Review of ASN-0077

## REVISE

### Issue 1: K.μ~ worked-example admissibility check omits three of five clauses
**ASN-0077, "Alternative transition Σ₁ → Σ₁' (... exhibiting K.μ~)"**: "K.μ~'s admissibility imposes three obligations on the (Σ, π) pair: (a) the precondition `|dom_C(M(d₃))| ≥ 2`, (b) the bijection is non-identity `π ≠ id`, and (c) the induced post-state satisfies the listed invariants ... All three obligations (a), (b), (c) are discharged; K.μ~ is admissible at this scenario."

**Problem**: Foundation K.μ~ (ASN-0047) lists *five* admissibility clauses on π: (i) invariant package, (ii) `M'(d) ≠ M(d)`, (iii) length-preserving, (iv) subspace-preserving, (v) link-subspace fixing — plus the named precondition. The example discharges only the precondition (a), clause (i) (as (c)), and a misstatement of clause (ii) (as (b)). Two further defects:
- Obligation (b) cites "non-identity `π ≠ id`," but clause (ii) is the *net-effect* condition `M'(d) ≠ M(d)`. `π ≠ id` does not entail `M'(d) ≠ M(d)` in general (a swap of two V-positions carrying equal I-values is invisible). Here it happens to hold because the swapped values differ, but the obligation is mislabeled.
- Clauses (iii) length-preservation, (iv) subspace-preservation, (v) link-subspace fixing are never discharged. They hold (both swapped positions are depth-3, subspace s_C, no link positions), but the claim "All three obligations are discharged; K.μ~ is admissible" overstates a verification that skips them.

**Required**: Enumerate all five K.μ~ admissibility clauses, discharge (iii)–(v) explicitly (one line each), and restate (ii) as the net-effect condition `M'(d) ≠ M(d)` rather than `π ≠ id`.

### Issue 2: O11★ and O11'★ are redundant specializations of O11★★
**ASN-0077, O11★ / O11'★**: "Such a chain is the special case of O11★★ in which sub-case (ii) never fires; O11★★ applies directly." / "... sub-case (i) never fires ..."

**Problem**: O11★★ is the general mixed-chain lemma; O11★ and O11'★ are stated as labeled claims whose entire derivation is "specialize O11★★." Three labeled multi-step preservation claims exist where one suffices. The only use is the worked example, which could cite O11★★ directly on each segment. This is claim accretion.

**Required**: Collapse O11★ and O11'★ into O11★★ (they can remain as a parenthetical "pure-K.μ⁺ / pure-K.μ⁺_L chains are the obvious specializations"), and have the worked example cite O11★★.

### Issue 3: Meta-prose / forward-reference accretion around the extension lemmas
The note carries `review-mode.anti-bloat`. Several passages explain why claims exist or preview downstream use rather than advancing reasoning:

- **O11.1 introduction**: "To chain these single-step claims into multi-step lemmas — *and to make available a citable handle for callers chaining queries across post-states* — we extract ..." — the bracketed clause is rationale for the corollary's existence.
- **After O11'★**: "The worked example below exercises the K.μ⁺ branch (via O11★) and the K.μ⁺_L branch (via O11'★) on disjoint chain segments; a mixed-chain witness ... would route through O11★★ ..." — a use-site preview of the worked example.
- **Before O13/O14**: "We record the failure modes as labeled negative claims *so that future ASNs do not mistakenly assume monotonicity-under-arrangement-modification* ..." — justification for why the negative claims are present (the claims themselves are legitimate content; the framing is not).
- **"We deliberately work with C1a's block decomposition rather than ASN-0058's `resolve` function ..."** — borderline: it conveys a real constraint (resolve's C1 asserts dom(C), wrong for links), but is framed as a defense of an authorial choice. Tighten to a one-line statement of the constraint.

**Required**: Delete the existence/preview rationales; retain only the object-level content.

VERDICT: REVISE
