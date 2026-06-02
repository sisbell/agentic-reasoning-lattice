# Review of ASN-0086

This ASN is mature and the core relational machinery (R0–R6, the three operations, both wp cases, the worked sketch) is sound — I checked the cross-home/same-home split in R0a, the cell decomposition in CoverageEqualityDecidable, the R-Scope antichain argument, the wp Case 1 self-emit branch, and the worked sketch arithmetic (`a₁=1.0.1.0.1.0.2.1`, `b₁=...2.2`, coverage half-open against `b₁`), and they hold. The ASN carries the `review-mode.anti-bloat` classifier, and the findings below are forward-reference/meta-prose accretion plus one clarity issue.

## REVISE

### Issue 1: Use-site forward pointer in R0's value-shape block
**ASN-0086, R0 "Value-shape consequence (L3-conformance check)"**: "...so the caller discharges no separate value requirement. We refer back to this check wherever an emitted triple's K.λ value-precondition must be met."

**Problem**: The first two sentences carry real content (L3-conformance is structural, value-independent). The closing sentence is a pure use-site forward pointer — it enumerates downstream consumers ("wherever ... must be met") rather than advancing the claim. This is exactly the accretion pattern the classifier names; the reader must skip it to follow R0.

**Required**: Delete the "We refer back to this check..." sentence. R5 and Nullify can cite "the L3-conformance check (R0)" without R0 advertising its own consumers.

### Issue 2: Notational-bookkeeping meta-prose in the Worked Sketch
**ASN-0086, Worked Sketch, Step 1 and Step 3**:
- "The later fresh emissions in this sketch (`a₂`, `b₂`, `a₃`) are all siblings of `b₁` ... so below we record only that varying ordinal."
- "(We use `b₂` for this retraction-of-retractor tuple — consistent with `b₁` for the original retractor — keeping `c₁`/`c₂` reserved for the Setup's content addresses.)"

**Problem**: Both are commentary about the presentation, not about the system. The second parenthetical is naming-convention bookkeeping; the first announces what abbreviation later steps will use. Neither advances the verification — they are essay content in a proof slot.

**Required**: Drop the parenthetical naming aside. The "record only that varying ordinal" sentence can be reduced to its operative content (later steps abbreviate the L-invariant discharge) or removed, since each step already says "discharge as at `b₁`".

### Issue 3: Nullify "three preconditions" overloads the term
**ASN-0086, Definition — Nullify**: "...with three preconditions: P0... P1... PC... P0 governs execution; P1 and PC condition the single-tuple-scope postcondition R-Scope."

**Problem**: Listing P1/PC as "preconditions" and then immediately stating they do not gate execution forces the reader to reconcile the contradiction inline. Worse, Step 4 of the Worked Sketch invokes `Nullify(Σ_3, d, a₃)` with **P1 false** (`a₃ ∉ dom(Σ_3.L)`) and the operation still executes and nullifies `a₃` — so "precondition" is actively misleading for P1. The Membership clause of the Definition only derives `a ∈ nullified(Σ')` on the P1 path, leaving the self-emit nullification (the case Step 4 actually exercises) unstated at the definition site even though it is the documented usage.

**Required**: Rename — call P0 the precondition (it gates execution) and P1/PC the *scope assumptions* under which R-Scope holds. Add one clause to the Membership paragraph covering the self-emit path (`a = a_emit(Σ, d_retr)`, where `a ∈ dom(Σ'.L)` directly gives `a ∈ nullified(Σ')`), so the Definition covers its own Step-4 usage.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs Observe
**Why out of scope**: The note works in ASN-0093's sequential-atomic-transition model (SequentialTransitionAxiom). The consistency model for concurrent Observe against in-flight Emit is genuinely new territory and is correctly deferred to the Open Questions, not a gap in this ASN.

### Topic 2: Multi-arity typed relations `L_K^{(n)}`
**Why out of scope**: Higher-arity links inhabit `dom(Σ.L)` but index no `L_K` tuple by design; whether they should project to binary relations or define `n`-ary relations is a future modeling choice, already logged as an Open Question.

VERDICT: REVISE
