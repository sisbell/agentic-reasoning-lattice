# Review of ASN-0126

I worked the load-bearing arguments before commenting on prose. The technical spine is sound: I checked the P5 lifting argument (apply `Emit_K` at `π(Σ)`, re-adjoin the framed registry, re-verify (0)/(i)/(ii)), the R-Scope transfer in *Retraction as an attributed Binary* (the "frame the two post-states together" step — both emits call `a_emit` on the same `(π(Σ), d_retr)`, so `dom(π(Σ').L) = dom(Ψ.L)` and the value difference in slot 1 is invisible to `A_rel` and to `{t : a ≼ t}`), and the P6 induction (new tuple by P3; old tuple by L12 + P1 + P4). Boundary handling is unusually complete — `|F|=0`, `|G|≥2`, `N>3`, unregistered K, empty registry, self-nullification, ghost targets, and the interior-prefix target `a = d_retr.0.s_L` (with `zeros=3`, `#E=1`) are all addressed. The cross-references stay within the foundations (ASN-0034/0036/0043/0086/0093). The findings below are accreted prose, which this note's classifier asks be surfaced at source.

## REVISE

### Issue 1: Tangential R0 aside misstates its own proof
**ASN-0126, Gate realizability**: "(This is also why R0 (TupleAddressFreshness, ASN-0086), itself an existence-of-successor result, is reached here by lifting rather than by B2 transfer.)"
**Problem**: This parenthetical does not match the P5 proof it sits inside. The existence-of-successor in P5 is supplied by `Emit_K`'s contract (which is what is lifted), and R0 enters the proof *only* through its value-shape consequence to discharge L3 — a static fact about the triple `(F, G, K)`, not an existence claim "reached by lifting." So the aside both characterizes R0's role incorrectly and digresses into methodology the surrounding sentences ("does not come from B2…", "We establish it directly, by applying ASN-0086's `Emit_K`…") have already settled. A precise reader has to reconcile "R0 reached by lifting" against the actual use of R0 two paragraphs later (value-shape, cited statically), and the two do not line up.
**Required**: Delete the parenthetical. If a methodological note about B2's limits is wanted, it is already carried by "does not come from B2, which yields no `→_sh`-successors"; nothing about R0 needs restating here.

### Issue 2: Closing "safety/liveness" paragraph restates settled results
**ASN-0126, Weakest precondition of the shape-gated emit**: "The dual reading is liveness. Where P3 guarantees every tuple a `→_sh`-step deposits conforms, its liveness dual **P5 (GateRealizability)** — established above (Gate realizability) — guarantees the converse… Safety (P3) and realizability (P5) together pin down exactly which emits the gate admits."
**Problem**: The wp section's work is the refinement of ASN-0086's Case-2 wp and the isolation of C3 as the newly-live conjunct. This paragraph adds no derivation: P3 and P5 are both proven before this point, the wp derivation does not depend on the "safety/liveness duality" framing, and nothing downstream consumes it. It is a thematic bow appended to a derivation slot — the reader skips it to follow the argument, which is the accretion signature.
**Required**: Cut the paragraph. The section should end at the C2/C3 analysis ("…C2's self-nullification, by contrast, is inherited from ASN-0086 and already live there.").

## OUT_OF_SCOPE

### Topic 1: Semantics of the mandated non-empty from-set for retraction
The `|F|=1` rule converts ASN-0086's *optional* retraction attribution (`RetractionDirectionality` permits an empty from-set) into a mandatory canonical fill `r = (d_retr, δ(1, #d_retr))`, whose coverage `{t : d_retr ≼ t}` blankets the entire home-document subtree — including the retraction's own address and every co-homed link. Nullification is unaffected (it reads `coverage(G')` only, as the note correctly establishes), but a from-patterned `Observe_R` would now match this fill uniformly, making from-side filtering of retractions vacuous.
**Why out of scope**: This is a consequence for `Observe` behavior, which the note explicitly defers to the behavior catalog (Open Question 2). It is not a defect in the gate or in this framework's invariants — single-tuple-scope still transfers, as the R-Scope argument shows.

VERDICT: REVISE
