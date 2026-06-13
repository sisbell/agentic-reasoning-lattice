# Review of ASN-0133

This is a careful note. The conditional-termination framing is honest, the H-W-as-foil argument is correct, Q-FLIP's `target_of` re-arm counterexample checks out, and the worked composition's single-view classification and Q5a bound are sound. Two issues remain, one substantive.

## REVISE

### Issue 1: Q3's "registration-checkable" extinction discipline is asserted against the note's own reachability standard, without a decision procedure

**ASN-0133, Q3 (StaticCheckability)**: "ρ's extinction discipline is verifiable at registration time, without executing any body: the implication ranges over PL-typed objects and the surface's emission forms."

And the load-bearing use, **ASN-0133, Q6**: "at-most-once-per-argument (Q-EXT, checkable at registration from *both* the SF spelling, via the spelling class, and the extinction discipline, via a strong-enough contract, Q3) ... That at-most-once half is registration-checkable; bounded domain growth is itself reachability-quantified".

**Problem**: The note draws its own checkable/meta-level line by one criterion — quantification over reachable states. It disqualifies H-W ("its statement quantifies over the states reachable by fire sequences ... PL deliberately cannot express") and bounded domain growth ("`|⋃_k [D_ρ]_{Σ_k}| < ∞` quantifies over all reachable states and is as meta-level as H-W"). But Q3's *defining* condition for "strong enough" is itself a universally-quantified semantic implication: "every emission set satisfying it at a trigger-true `(x, Σ)` produces a post-state falsifying `T_ρ(x, ·)`." Read over reachable `(x, Σ)`, this quantifies over reachable states exactly as H-W does, and by the note's own standard should be "as meta-level" — not "checkable." Read over *all* states (schema-level), the note never says so, and even then validity of "every Post-satisfying deposit falsifies this PL trigger" is a validity question over PL (which carries quantifiers and aggregates, PC1/PC2a) plus the emission semantics — not shown decidable, and given no checking procedure. The justification offered ("ranges over PL-typed objects and the surface's emission forms") establishes only that the obligation is *static*, not that it is *effective*. By contrast the SF half genuinely is decidable (PD0's ST/SF rules are syntax-directed, like WT), and ASN-0130's `certify_pd_stable` exhibits an actual checker (PD0's rules on `expand(a)`). Pairing the decidable SF check and the unspecified Q3 obligation under one banner — "registration-checkable" — overstates what is delivered and undercuts the "at-most-once is a registration-time *fact*" payoff that Q5a/Q6 and the abstract rest on.

**Required**: State which quantification "strong enough" carries.
- If schema-level: say so, argue (or bound to a decidable fragment) the schema-validity check, and note it is a sound over-approximation (it may reject a contract disciplined only on reachable states).
- If reachable-level: reclassify Q3 alongside bounded domain growth as meta-level, and revise "at-most-once is a registration-time fact" accordingly.

In either case, make explicit that for the load-bearing negated-existential marker pattern the check *does* reduce to a decidable syntactic match — the fire deposits exactly the witness the trigger's `∃` quantifies over (`Post_P` emits a `cmt` covering `t`; the audit `L_cmt` grows; the trigger flips) — so the checkability claim is sound *there* even where the general Q3 statement is not. Scope the claim to where the check is actually effective.

### Issue 2: Q6's termination proof presumes a last real fire exists; the zero-real-fire boundary is not shown

**ASN-0133, Q6 (TerminationUnderFairness)**: "H-RF bounds the real fires, so σ has a last real fire; no fire after it can be real ... The state is therefore constant past the last real fire."

**Problem**: H-RF permits *zero* real fires, and that case is reachable under Q6's hypotheses (e.g. a registry already quiescent at Σ₀: zero real fires, H-FAIR vacuous). With no real fire there is no "last real fire," and "constant past the last real fire" has no referent — the proof as phrased does not cover its own zero boundary. The conclusion still holds (the constant tail is all of σ from Σ₀, and the same H-FAIR step forces Σ₀ quiescent), but the standard requires the zero case be shown, not left to the reader to subsume.

**Required**: One clause: "if σ has no real fire, the constant tail is all of σ from Σ₀, and the H-FAIR argument below applies verbatim at Σ₀." Soundness is unaffected; this is a proof-completeness gap, not an error.

## OUT_OF_SCOPE

### Topic 1: Unconditional termination and a concrete fair scheduler
The note proves termination only conditionally (H-RF + H-FAIR) and constructs no scheduler discharging H-FAIR. This *looks* like a gap but is correctly out of scope: the note's thesis is precisely that unconditional termination is unprovable for forward-chaining systems, and scheduler construction ("scheduling disciplines, their fairness proofs ... violation policy") is explicitly deferred to the operational layer. Naming H-FAIR as an undischarged hypothesis is the right move, not an omission.

### Topic 2: Per-scope termination and bounded re-entry
Q7–Q9 give per-scope *recognizability and absorption* but stop short of per-scope *termination*, and Q8's re-entry (an out-of-scope fire un-quiescing an inner scope) is left unbounded. This is new territory (the note flags it as Open Questions 3–4), not a defect in the global result: Q6's termination is stated at scope `⊤`, where no fire is out-of-scope and re-entry cannot arise.

META: not applicable — the note specifies contracts and guarantees of the coordination layer (recognizability, absorption, conditional termination) abstractly, with rule bodies deliberately opaque, so it stays on the system-guarantee side rather than drifting into algorithm mechanics.

VERDICT: REVISE
