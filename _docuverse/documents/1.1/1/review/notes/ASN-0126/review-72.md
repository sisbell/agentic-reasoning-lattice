# Review of ASN-0126

This is a strong note: it states its three deliverables (shape catalog, gated emit, immutable registry), proves them as named properties (P1–P6), introduces a genuine technical device (the projection bridge), extracts a non-trivial wp insight (C3 becomes live once non-unit Binary retraction is admitted), and grounds all of it in a concrete worked illustration whose arithmetic I checked and found correct. The issues below are real but fixable.

## REVISE

### Issue 1: (B2) asserts a false universal as its justification

**ASN-0126, "The projection bridge," (B2) Lemma transfer**: "Every ASN-0086 result quantified over `→*`-reachable three-component states holds at `π(Σ)` for each state Σ this note reasons about; since these results constrain only the shared C/M/L components, their conclusions transfer to Σ directly."

**Problem**: The "since" clause is presented as a fact about *every* ASN-0086 result, and it is false for ASN-0086's existence-of-successor results — R0 (TupleAddressFreshness), R5 (TupleSelfTargeting), and R6c's restoration-by-reemission. Each concludes `∃ Σ' : Σ → Σ' ∧ …`. Transferring such a conclusion via π yields a **→-successor of π(Σ)**, not a **→_sh-successor of Σ**: the witnessing `K.λ` step need not satisfy (0)/(i)/(ii), so it need not be a `K.λ_sh` step. "Their conclusions transfer to Σ directly" is therefore not true for this subclass. The note's own P5 confirms this — it does *not* invoke B2 to obtain a gated emission; it re-derives one by applying `Emit_K` at π(Σ) and then **manually lifting** the `K.λ` step to `K.λ_sh`, which would be unnecessary if B2 transferred existence claims directly. B2-as-used is sound (every actual citation — R-Scope, wp Case 2, L12, L-ContiguousPrefix — is a state/transition predicate over C/M/L), but B2-as-stated overreaches.

**Required**: Restrict B2 to ASN-0086 results whose conclusion is a predicate over the C/M/L components of a single →*-reachable state, or of a transition between states both exhibited as →_sh-reachable. State explicitly that existence-of-→-successor results are *excluded* and are handled separately by lifting (P5), since a →-successor of π(Σ) is not automatically a →_sh-successor of Σ.

### Issue 2: Shape-well-definedness is re-derived after it was already given

**ASN-0126, "The registry," paragraph after C0**: "C0's uniqueness of coverage-class keys is what lets the framework read a *shape per type*. Because lookup is by coverage class and no two entries share a `~`-equal key, `shape` respects `~` … So `shape(·)` is a well-defined function of the type-as-coverage-class `[K]` … The gate's conformance predicate, and the gate itself, read `shape(K)` through this function."

**Problem**: Two sentences earlier the same section already states "a well-formed registry *is* a partial function `T_admissible/~ ⇀ (name, shape)` from coverage classes to entries" — from which "`shape` well-defined per coverage class" is immediate. The flagged paragraph re-derives that conclusion (uniqueness ⟹ respects-~ ⟹ function-of-[K]) adding nothing, and closes by enumerating downstream consumers ("The gate's conformance predicate, and the gate itself, read `shape(K)`") — a use-site inventory rather than advancement of the definition. The same fact is then asserted a third time in "The shape-gated emit" ("(i) supplies `shape(K)` — a well-defined function of `[K]`…"). This is exactly the accretion the anti-bloat classifier targets: one fact stated three times across three sections, once via redundant re-derivation, once via consumer enumeration.

**Required**: Delete the re-derivation paragraph. If a bridge sentence is wanted, keep a single clause — "so `shape(K)` depends only on `[K]`" — and drop the downstream-consumer sentence. The lone in-text reference in "The shape-gated emit" can cite it without re-asserting well-definedness.

### Issue 3: Precondition (0) silently drops all N > 3 emissions; only the empty-from consequence is drawn

**ASN-0126, "The shape-gated emit"**: precondition "(0) *the emitted value is a standard triple* — arity 3," and the subsequent paragraph spells out only the empty-from exclusion ("`Emit_K(Σ, d, ∅, G)` … has `|F| = 0` … the emit has **no** `→_sh` image").

**Problem**: ASN-0086's `K.λ` admits arity `N ≥ 3` (L3, ASN-0043), and ASN-0043's L3 records Nelson's explicit call for "4-sets, 5-sets … n-sets." Precondition (0) restricts `→_sh` to arity *exactly* 3, so **every** `N > 3` emission — legal under ASN-0086 — also has no `→_sh` image. The note draws out this "no `→_sh` image" consequence at length for the empty-from class but leaves the arity exclusion implicit in (0). An app relying on n-set links is foreclosed by this framework and is never told so.

**Required**: State explicitly, parallel to the empty-from paragraph, that (0) excludes every `N > 3` emission from `→_sh`. Point to Open Question 6 as the deferred remedy (the remedy itself is correctly out of scope; the *acknowledgement* of the exclusion is in scope here).

## OUT_OF_SCOPE

### Topic 1: Runtime / post-`Σ_init` type registration
The registry is fixed at `Σ_init` and immutable; P1 (and hence P2/P4/P6) rests on that immutability. An app that needs to declare a new type *after* `Σ_init` has no mechanism here. That is genuine future territory — it would require a registration operation and a re-examination of P1 (the registry would no longer be invariant) — not an error in this note, whose entire contribution is the *static* registry.

### Topic 2: The C3-liveness operational consequences
The wp section establishes that non-unit Binary retraction makes C3 live, so tuples can be "born nullified." What an app *should do* about born-nullified tuples (reject at a higher layer, surface to the caller, treat as no-op) is operational semantics, correctly deferred to the successor note named in the Open Questions.

VERDICT: REVISE
