# Review of ASN-0126

## REVISE

### Issue 1: Corollary RangeSterilization is stated in general form but proven only at the worked instance
**ASN-0126, Worked illustration**: "One gate-clearing range-G retraction irreversibly sterilizes every unfilled link-chain slot its to-span covers — here the contiguous block `...2.4` through `...2.6` of its own home `d`: ... active emission homed at `d` resumes only once the block is exhausted by that many sacrificial deposits — here three..."
**Problem**: The opening clause quantifies over *any* gate-clearing range-G retraction and *every* covered unfilled slot, and both the Retraction section ("the first gap's cost extends to unfilled chain slots") and Open Question 7 cite the corollary at that generality. But the supporting paragraph ("The poisoning is a block, not a slot") derives only the three-slot instance, and only through `a_emit`'s *subsequent-emission* branch. Missing at the stated generality: (a) the first-emission boundary — a retraction whose coverage includes `d.0.s_L.1` while no link is yet homed at `d` (`J_d = -1`), i.e., the empty-chain/first-slot case the standards make mandatory; (b) the induction over the `k` covered slots that "exhausted by that many sacrificial deposits" presupposes — the proof lists three deposits, it does not induct; (c) the resumption claim — "`...2.7` the first slot past the range" lands *active* only if no *other* `L_R` tuple covers it, a proviso absent from the general statement. Showing the three-slot case works does not establish that all cases do. Separately, a normative formal artifact consumed by two other sections lives inside an illustration section — flag the placement.
**Required**: Either (1) state and prove the corollary in its own subsection at its claimed generality — arbitrary to-span `(g, ℓ)`, both EmitAddress branches, induction over the covered block of chain indices, an explicit no-other-coverage proviso on resumption — with the worked illustration reduced to an instantiation; or (2) scope the corollary explicitly to the instance and reword the Retraction-section and OQ7 citations so they no longer lean on an unproven general claim.

### Issue 2: P-tgt is established at Σ but consumed at π(Σ) without the B1 carry
**ASN-0126, Retraction as an attributed Binary**: "*Apply R-Scope within ASN-0086.* By ProjectionBridge `π(Σ)` is `→*`-reachable, so — `a` meeting P-tgt at `π(Σ)` — R-Scope applies to the empty-from `Nullify(π(Σ), d_retr, a)`..."
**Problem**: P-tgt is defined and verified at the four-component state Σ ("`a ∈ A_rel^Σ` ... or `a = a_emit(Σ, d_retr)`"); move 2 asserts it at `π(Σ)` with no justification. The equivalence is one B1 line — `A_rel^{π(Σ)} = A_rel^Σ` and `a_emit(π(Σ), d_retr) = a_emit(Σ, d_retr)` — and the note cites B1 explicitly at every comparable state crossing elsewhere ("pure L-reads, shared by B1," "carried across B1"), so its absence here is a gap by the note's own standard. The earlier leaf example has the same slippage in shorthand form ("P-tgt's first disjunct `a ∈ A_rel^Σ` holds, so R-Scope applies" — applying an ASN-0086 result directly at a four-component state).
**Required**: Insert the B1 carry: P-tgt holds at Σ iff at `π(Σ)` because both disjuncts read only the B1-shared components.

### Issue 3: Ghost-root counterexample's exclusions rest on uncited foundations
**ASN-0126, Retraction as an attributed Binary**: "for which `zeros(a) = 3` but `#E(a) = 1`, so `a ∉ dom(Σ.L)` and `a ≠ a_emit(Σ, d_retr)`: P-tgt fails on both disjuncts."
**Problem**: The "so" carries a multi-fact derivation. `a ∉ dom(Σ.L)` rests on L1b (every link address has `#E ≥ 2`, ASN-0043), which holds at this note's four-component Σ only via the bridge — L1b at the `→*`-reachable `π(Σ)`, then B1 sharing the L-component. `a ≠ a_emit(Σ, d_retr)` rests on EmitAddress's branch shapes (the first-emission branch yields `#E = 2`; the subsequent branch `inc(ℓ_prev, 0)` preserves the `#E ≥ 2` of a chain link). None of this is cited; the counterexample is load-bearing for the section's central caveat that single-tuple scope is an app obligation.
**Required**: Cite L1b (routed through the bridge/B1) for the first exclusion and EmitAddress's two branch shapes for the second.

### Issue 4: Abutting-spans witness — the interval-union equality is under-justified
**ASN-0126, Shape-conformance**: "T1 trichotomy at the shared endpoint and transitivity across it give `coverage(F₂) = {t : a ≤ t < a ⊕ δ(2, #a)} = coverage(F₁)`"
**Problem**: For `[a, m) ∪ [m, b) = [a, b)` with `m = a ⊕ δ(1, #a)`, `b = a ⊕ δ(2, #a)`, the ⊇ direction is trichotomy, but the ⊆ direction needs `a < m` and `m < b` before transitivity does anything — and neither ordering is supplied by the cited ingredients (trichotomy, transitivity, TS3, which only handles endpoint arithmetic). "Abut" presupposes the ordering it should derive. Both facts follow in one line from the two spans' T12 well-formedness — start < end on each span (TA-strict / T12's postcondition `s ∈ span(s, ℓ)`) — which the sentence already establishes but never invokes for ordering. Notably, RegisteredAdmissible cites exactly this T12 postcondition where it is *redundant* (see Issue 5); here, where it is needed, it is absent.
**Required**: One line: both `F₂` spans are T12-well-formed, so each has start < end, giving `a < m < b`; then trichotomy at `m` and transitivity yield the mutual inclusion.

### Issue 5: Forward-reference and justification accretion (anti-bloat)
**ASN-0126, multiple sections**: (a) two sections defer to the same downstream location — Single-source: "A multi-span source is deferred to Open Question 6."; The shape-gated emit: "The path to richer arity is left to Open Question 6." — and OQ6 then re-duplicates the Single-source motivation ("for a source spanning disjoint passages"), so the disjoint-passages rationale appears twice; (b) RegisteredAdmissible double-justifies one fact in one sentence: the TA-strict derivation establishes `s < s ⊕ ℓ`, then the em-dash clause "— span non-emptiness, recorded as T12's postcondition `s ∈ span(s, ℓ)` —" re-cites an alternative source for the same fact; (c) the supersession of `Nullify` is stated twice within the Retraction section: "This `Nullify_Binary` is the live retraction operation the framework supplies in place of the empty-from `Nullify`." and, three paragraphs later, "the empty-from `Nullify` is superseded by the attributed-Binary wrapper `Nullify_Binary` defined above."
**Problem**: Each is small, but together they match the flagged accretion patterns: multiple sections deferring to one downstream slot, duplicated motivation, double justification, and the same assertion in two paragraphs of one section.
**Required**: Keep one deferral to OQ6 (let OQ6 alone carry the motivation); drop the redundant T12 clause in RegisteredAdmissible (or move that citation to the Shape-conformance witness, where it is needed — Issue 4); state the supersession once.

## OUT_OF_SCOPE

### Topic 1: Registry read/discovery operation
Apps other than the author of `Σ_init` have no specified way to learn which coverage classes are registered or with what shapes; the operation set has no registry read.
**Why out of scope**: The gate's semantics are fully specified without one; an Observe-style registry query belongs to the successor note layering operational semantics (alongside OQ2–OQ5), not to this framework.

### Topic 2: Registry evolution beyond `Σ_init`
Amending, migrating, or widening the registry across substrate generations (e.g., relaxing a Unary registration to Multi, retiring a class).
**Why out of scope**: Immutability (P1) is this note's deliberate commitment and is proven; evolution paths are new design territory adjacent to OQ4/OQ6, not an error here.

VERDICT: REVISE
