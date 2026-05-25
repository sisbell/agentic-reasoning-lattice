# Review of ASN-0075

I worked through the proofs carefully, including verifying both histories in D-DISCR satisfy ValidComposite★, checking the worked example's state evolution against the K.δ/K.α/K.μ⁺/K.μ~/K.μ⁻/K.ρ contracts, and walking through the case analysis in D-ACT's partition argument.

## REVISE

### Issue 1: Edge-case condition is sufficient but mischaracterized as defining

**ASN-0075, Edge Cases, "Documents with no shared content"**: "If for every `a ∈ dom(C)`, `¬((a, d_A) ∈ R ∧ a ∈ ran(M(d_B)))` and `¬((a, d_B) ∈ R ∧ a ∈ ran(M(d_A)))`, then no address satisfies either asymmetric definition."

**Problem**: The DeletedFromAWithB predicate requires `(a, d_A) ∈ R ∧ a ∉ ran(M(d_A)) ∧ a ∈ ran(M(d_B))`. The stated edge-case condition omits the `a ∉ ran(M(d_A))` conjunct, so it is strictly stronger than what emptiness requires — it rules out shared current content, not just deletions-with-witness. A reader checking the boundary against the formal predicate will notice the mismatch.

**Required**: Either weaken the condition to match the predicate exactly (`¬((a, d_A) ∈ R ∧ a ∉ ran(M(d_A)) ∧ a ∈ ran(M(d_B)))`), or explicitly state the condition is *sufficient* (not characterizing) and that it captures the stronger notion of "no shared content history."

### Issue 2: Q0 derivation invokes P4★ on a contradiction-target without naming the composite-boundary hypothesis

**ASN-0075, "Vacuity of both report halves"**: The chain "for the conjunct DELETED(a, d_A) ∧ CURRENT(a, d_B) to hold, CURRENT(a, d_B) requires a ∈ ran(M(d_B))... must satisfy subspace(v) = s_C... by P4★ forces (a, d_B) ∈ R — contradiction."

**Problem**: P4★ is a composite-boundary property, not a per-state invariant (acknowledged in D-EXH). The Q0 wp derivation tacitly evaluates at the pre-state Σ and cites P4★, but does not state the precondition includes "Σ is a reachable state." A reader could apply this wp at an intermediate state where P4★ may fail.

**Required**: Add the reachability hypothesis to the Q0 wp precondition, or reference D-OBS/D-RECONS to argue SHOWDELETIONS is only invoked at composite boundaries (some such note exists implicitly but is not threaded through the wp computations).

### Issue 3: D-ACT case structure has an implicit "shorter length, same origin" sub-case

**ASN-0075, D-ACT proof**: The three explicit sub-cases are "Same origin, same length," "Longer length" (deduces same origin via prefix structure), and "Different origin."

**Problem**: The case "shorter length, same origin" (`#t < L_d + 3` with `origin(t) = d`) is not explicitly listed. It is vacuous (uniform length of A_C(d) emissions forbids it), but a Dijkstra-style proof should make this exhaustion explicit. The reader has to reconstruct the partition: same-origin forces #t = L_d + 3, so "different length, same origin" is impossible in either direction; "Longer length" only nominally handles the `#t > L_d + 3` direction.

**Required**: Add one sentence acknowledging that the case `#t < L_d + 3 ∧ origin(t) = d` is vacuous by A_C(d)'s uniform emission length, parallel to the contradiction derived in the "Longer length" case. This makes the case partition manifestly exhaustive.

### Issue 4: D-IDENT's appeal to S3★ for transclusion integrity overstates the guarantee

**ASN-0075, D-IDENT consequences**: "By S2 (ArrangementFunctionality, ASN-0036) and S3★ (GeneralizedReferentialIntegrity, ASN-0047), arrangements reference I-addresses by tumbler identity: each V-position maps to a determinate `a ∈ dom(C)`."

**Problem**: S3★ permits content-subspace V-positions to map to `dom(C)` AND link-subspace V-positions to map to `dom(L)`. The blanket claim "each V-position maps to a determinate `a ∈ dom(C)`" is false for link-subspace V-positions. The intended scope is content-subspace transclusion, which the surrounding paragraph addresses, but the cited justification is imprecise.

**Required**: Restrict the citation to S3★'s content clause, or qualify the statement to "each content-subspace V-position maps to a determinate `a ∈ dom(C)`."

VERDICT: REVISE
