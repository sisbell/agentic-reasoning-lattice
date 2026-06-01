# Review of ASN-0086

I checked the proofs against the foundation contracts (ASN-0034/0036/0040/0043/0093 are all in the verified foundation set, so cross-references to them are in-bounds). The core argument chain — L-ContiguousPrefix → R0a antichain → R-Scope, R0 freshness in both emission branches, the wp Case 2 derivation, and R7a's K-op decomposition — is sound and free of circularity (L-ContiguousPrefix inducts on clauses (b)/(c) without invoking R0a; R0a then consumes it). The Worked Sketch verifies R0–R3, R5, R6a–c, and the wp Case 2 false branch against concrete tumblers. No correctness defect surfaced.

The note carries `review-mode.anti-bloat`, and the findings below are meta-prose around the partial-operation contract that a precise reader must route around.

## REVISE

### Issue 1: Emit_K partiality passage restates and forward-defers rather than advancing
**ASN-0086, Definition — Emit_K**: "The partiality is located by K.λ's "produced by `A_L(d)`" gate, not by `a_emit`, which is itself total (Definition — `a_emit`)" … "*(Defined direction.)* … *(Undefined direction.)* … The two directions together give: Emit_K is undefined exactly where the chain frontier is ill-formed."

**Problem**: This passage (a) restates `a_emit`'s totality, already established at Definition — `a_emit`; (b) forward-defers to "the P0f condition (Definition — Nullify)" while *fully stating* the contiguous-chain-prefix condition in place — the named predicate is defined downstream but its content lives here; (c) wraps a one-line iff in "Defined direction / Undefined direction / The two directions together give" essay framing. The operative content reduces to a single clause.

**Required**: Compress to: "Emit_K is defined iff `d`'s homed-set is a contiguous chain prefix of `A_L(d)` (the P0f condition); where it fails — e.g. the NestedLinkWitness construction — `inc(ℓ_prev, 0)` is off-chain and Emit_K is undefined." Drop the `a_emit`-totality restatement and the directional framing.

### Issue 2: wp Result explains why a conjunct is absent rather than stating the wp
**ASN-0086, Weakest-Precondition Analysis, Result**: "The index membership `K ∈ T_admissible` is presupposed in naming `Emit_K` (there is no operation `Emit_∅`), not a wp conjunct: the wp's free variables are `(Σ, d, F, G)`, and the type-index K enters the body only through the genuinely call-dependent relation `K ≁ R`."

**Problem**: This is justification of a conjunct's *absence* — meta-prose about the wp's shape, not a step in computing it. It matches the flagged pattern "new prose explains why [something] is needed rather than what it says."

**Required**: Remove, or fold into a parenthetical at the formula (`K` is an index, not a free wp variable).

### Issue 3: wp Case 1 "Domain of quantification" re-exposits the partial-operation convention
**ASN-0086, Weakest-Precondition Analysis, Case 1, "Domain of quantification"**: "since the internal `Emit_R` is partial there and total only over the substrate-conforming sub-domain (Definition — Emit_K), the wp is read with the standard partial-operation convention — at a Σ where the operation does not execute … the postcondition is unreachable, the non-execution mode discussed below."

**Problem**: This paragraph defers to Definition — Emit_K for partiality (re-established in Issue 1) and restates the partial-operation reading that the load-bearingness analysis already exercises when it drops P0. It is scaffolding the reader skips past.

**Required**: Delete; the P0-drop case in the load-bearingness paragraph already carries the non-execution semantics.

## OUT_OF_SCOPE

### Topic 1: `↝`/substrate-conforming-layer apparatus for hypothetical higher layers
R6d and R7a prove guarantees over the categorical relation `↝` and arbitrary conforming layers. These are forward-looking (no such layer exists yet in the substrate), but they state genuine invariant-preservation guarantees ("no conforming higher-layer op un-nullifies a tuple"), so they are a legitimate guarantee to fix now rather than an error.

META: The ASN remains in-spec — it defines abstract relational state (`L_K`, `A_K`, `nullified`), three operations, and their invariants, all stated implementation-independently; the meta-prose is local accretion, not drift.

VERDICT: REVISE
