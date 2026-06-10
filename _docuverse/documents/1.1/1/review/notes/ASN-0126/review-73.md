# Review of ASN-0126

I checked the proofs against the foundations (ASN-0043, ASN-0086) and worked the arithmetic of the worked illustration. The formal core is rigorous: P1–P6 are each derived (not asserted), the induction steps name every case, the wp factorization through `g_sh → Emit_K` is sound, the ProjectionBridge correctly excludes existence-of-successor results, the R-Scope frame argument is valid (the conclusion reads only `A_rel^{Σ'}` and the target subtree, both provably equal across Nullify and wrapper), and the born-nullified example checks out address-by-address. The boundary cases that matter here — `F = ∅`, `N > 3`, `G = ∅` (Unary), ghost targets, self-nullifying retraction, non-unit Binary retraction, first-emission `a_emit` — are all handled. The findings below are accretion, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: B2's definition is capped with a use-site inventory
**ASN-0126, "The projection bridge" (end of B2)**: "This is the subclass every B2 citation below draws on — R-Scope, wp Case 2, L12, L-ContiguousPrefix are all state- or transition-predicates over C/M/L."
**Problem**: This sentence advances no reasoning. B2's scope condition — "a predicate over the C/M/L components" — is fully stated by the sentence before it. Cataloging the four downstream results that will draw on B2 is exactly the "definition's introduction enumerates downstream consumers" pattern. (Note the contrast with the adjacent *Existence-of-successor results are excluded* paragraph, which earns its enumeration: it carries the load-bearing caveat that a `→`-successor of `π(Σ)` "is not automatically a `→_sh`-successor of Σ," preventing a real misapplication. That paragraph reasons; this sentence only lists.)
**Required**: Delete the sentence. Each of R-Scope, the wp section, and P6 already announces its own reliance on B2 at the point of use.

### Issue 2: the N>3 exclusion is wrapped in motivation, a quote, and a defense
**ASN-0126, "The shape-gated emit" (second-class paragraph)**: 'ASN-0086\'s `K.λ` admits any arity `N ≥ 3`; L3 (ASN-0043) records Nelson\'s explicit call for N-endset support beyond three, "4-sets, 5-sets ... n-sets supported in link storage and search." ... This is a deliberate narrowing of the gateable surface, not an oversight; the path to richer arity is left to Open Question 6.'
**Problem**: The substantive claim is one clause — precondition (0) restricts `K.λ_sh` to arity 3, so `N > 3` emissions have no `→_sh` image (Sh-conf reads exactly two content slots). Around it: the Nelson quote re-imports L3's color to argue N>3 is *desirable*, which the reader does not need in order to understand it is *foreclosed*, and which is already covered by the preceding "admits any arity N ≥ 3"; the restatement "an app whose links carry four or more endsets is foreclosed ... just as the empty-from emit is" repeats "no `→_sh` image"; and "not an oversight" is a defensive justification against an objection no one is making.
**Required**: Reduce to the one clause. Drop the Nelson quote, the restatement, and the "not an oversight" defense. (A single pointer to OQ6 may stay — it is not a repeated deferral.) This trims the *prose*; the foreclosure itself is a correct scope choice — see OUT_OF_SCOPE.

### Issue 3: the registry's name-uniqueness machinery feeds no claim
**ASN-0126, "The registry"**: "a **name** — an opaque string identifier"; "names are unique within the registry"; "Within one substrate, the name uniquely identifies a registry entry."
**Problem**: No result in this note reads the name. The gate reads `shape(K)`; P1–P6, CoverageEqualityDecidable, and RegisteredAdmissible read shape and the representative endset `K_j`; `a_emit`, Emit_K, and the typed-relation machinery read only C/M/L. The text itself singles out the load-bearing clause — "the condition the shape function's well-definedness actually rests on — *coverage-class keys are unique*" — which concedes that name-uniqueness is *not* what anything rests on. The derived line "the name uniquely identifies a registry entry" is then a consequence stated for no consumer.
**Required**: Drop the name-uniqueness well-formedness clause and the "uniquely identifies a registry entry" restatement, or relocate them to the successor note where app-facing lookup-by-name is specified. (The name *field* may remain as forward-looking registry content carried by P1, but the uniqueness invariant and its restatement are dead weight here.)

## OUT_OF_SCOPE

### Topic 1: arity beyond 3 and unattributed (empty-from) retraction
**Why out of scope**: The framework deliberately gates only `|F| = 1`, arity-3 links. `N > 3` support is correctly deferred to Open Question 6, and unattributed retraction (`F = ∅`) is correctly re-expressed as the attributed Binary wrapper. These foreclosures are design choices, not errors — Issue 2 targets the *prose* around the N>3 foreclosure, not the foreclosure.

### Topic 2: when and how apps register types
**Why out of scope**: The registry is fixed at `Σ_init` and never drifts (P1). Whether `Σ_init.registry` is app-declared, substrate-shipped, or dynamically grown is correctly deferred to Open Question 4. Nothing in this note requires resolving it.

VERDICT: REVISE
