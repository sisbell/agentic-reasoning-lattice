# Review of ASN-0086

I checked the relational layer's proofs (R0–R6c, R-Scope), the two wp cases, the discipline-discharge induction, and the worked sketch against the foundation contracts. The mathematics is sound: R0a's antichain (both cross-home and same-home cases), R-Scope's single-tuple scope (including the self-emit branch via R0a at Σ'), R3/R6a/R6c monotonicity, and the wp derivations all hold, and the worked sketch is internally consistent (tumbler arithmetic, freshness, audit/active divergence all check out). The one issue is residual meta-prose that the attached anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: "Definition — relational layer" pre-states its own discharge proof's conclusion
**ASN-0086, Definition — relational layer**: "Its one *discipline commitment* is a single predicate over `→`-steps: every `→`-step `Σ → Σ'` that grows the retraction slice ... is a `Nullify`. This quantifies over *all* `→`-steps ... raw `K.λ` included; **in particular no raw arity-3 `K.λ` at a type index `K ~ R` may enlarge `L_R` outside the `Nullify` alias.**"

**Problem**: The bolded "in particular" clause is the exact conclusion the discharge paragraph derives by step-kind enumeration ("…The only remaining step kind that can grow `L_R` is a raw arity-3 `K.λ` at `K ~ R`. By the discipline commitment, the sole `L_R`-growing step kind … is … a `Nullify`"). The reader meets the same claim twice — asserted in the definition slot, then proved in the discharge. This is the "two paragraphs say the same thing in different words" / "essay content in a structural (definition) slot" pattern. The commitment itself is the single sentence "every `→`-step that grows `L_R` is a `Nullify`"; the step-kind analysis belongs only to the proof.

**Required**: Cut the "in particular no raw arity-3 `K.λ` …" clause from the definition. If disambiguation that raw `K.λ` is in scope is wanted, keep only "(this quantifies over raw `K.λ`, not just the layer aliases)"; leave the per-step-kind conclusion to the discharge induction.

### Issue 2: dangling forward pointer in AddressUniverse
**ASN-0086, Definition — AddressUniverse**: "(SD, StoreDisjointness, ASN-0093, supplies only the disjointness of the two categories, **used below**.)"

**Problem**: "used below" is a bare forward pointer that advances no reasoning at the point of use; the disjointness is invoked where it is needed (Definition — Partition, R4) with its own citation. Such pointers are the accretion the classifier targets.

**Required**: Drop the parenthetical, or replace with the substantive statement only ("SD supplies the disjointness `dom(Σ.C) ∩ dom(Σ.L) = ∅`").

## OUT_OF_SCOPE

### Topic 1: wp over the full →*-reachable (undisciplined) domain
The wp Case 2 "Domain caveat" correctly scopes the formula to layer-reachable states and notes the extra disjunct an undisciplined wide pre-existing retraction would force. Characterizing wp over the larger undisciplined domain is a separate analysis, not a defect here.

### Topic 2: higher-arity typed relations and binary projections
The Open Questions raise whether `|Σ.L(a)| > 3` links define multiple binary projections or inhabit higher-arity `L_K^{(n)}`. The current note deliberately triple-restricts every `L_K`; the higher-arity treatment is future territory.

VERDICT: REVISE
