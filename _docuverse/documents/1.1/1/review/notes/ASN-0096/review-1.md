# Review of ASN-0096

## REVISE

### Issue 1: Claim count mismatch
**ASN-0096, organizational summary**: "Eighteen claims organized into..."
**Problem**: The five groups enumerate sixteen abbreviations — Still point (6: LP-IMM, LP-COV, LP-CON, LP-MON, LP-SLOT, LP-TYPE), Moving frame (4: LP-REARR, LP-CONTR, LP-EXT, LP-CROSS), Derived (2: LP-SURV, LP-DISC), Non-invariants (3: LP-NOV, LP-NOC, LP-NOD), Frame (1: LP-FRAME) = 16, not 18.
**Required**: Either correct the count, or surface the two missing claims with names and group placement.

### Issue 2: Moving frame may not cover all transition families
**ASN-0096, Moving frame**: "displacement modes under each K.μ family transition"
**Problem**: Only four displacement claims (REARR, CONTR, EXT, CROSS) are named. The vocabulary identifies operations including INSERT, DELETE, COPY, MAKELINK, and forking — which collapse to which displacement mode? Without an explicit mapping, the "each K.μ family" quantifier is unverified. In particular, FORK (version creation) and COPY (which produces fresh I-addresses) are not obviously any of {REARR, CONTR, EXT, CROSS}, and MAKELINK creates new links rather than displacing them — does it fall under LP-FRAME instead?
**Required**: Exhibit the surjection from K.μ family members onto the four displacement modes (or onto frame), with one sentence per family explaining why its semantics reduce to that mode.

### Issue 3: Projection signature underspecified
**ASN-0096, projection definition**: "the projection function `proj(e, d, Σ)`"
**Problem**: The argument `e` is undefined in the summary. Endset element? Span? I-address? The vocabulary distinguishes endsets, spans, and addresses — projection over each is a distinct operation with distinct cardinality and totality properties. Σ is also unstated; is it a Vstream, a (Vstream, POOM, version) tuple, the full system state?
**Required**: A definitional preamble stating the type signature, the role of each argument, and the codomain (set of V-positions? Sequence? Possibly-empty multiset under transclusion?).

### Issue 4: Derived guarantees lack visible derivation chains
**ASN-0096, LP-SURV and LP-DISC**: "Derived guarantees... the survival condition and discoverability criterion"
**Problem**: Standard #7 requires that "derived" claims show the derivation explicitly with named premises. The summary asserts derivation but does not name the premises (which still-point claims + which moving-frame claims compose into LP-SURV?). Discoverability in particular is non-trivial — it requires both forward (from source) and reverse (from target) projection well-definedness, which means it depends on at least LP-COV plus the four moving-frame claims; the dependency must be named.
**Required**: For both LP-SURV and LP-DISC, state the premise set explicitly (e.g., "LP-SURV ≡ LP-COV ∧ LP-CONTR ⇒ (proj ≠ ∅ ⟺ coverage ∩ live-vstream ≠ ∅)") and walk the inference.

### Issue 5: Boundary cases omit standard hard cases
**ASN-0096, boundary enumeration**: "empty projection, boundary insertion, cross-version, cross-owner, reverse-orphan, split coverage"
**Problem**: Several standard projection edge cases are absent:
- Zero-width span in endset (length 0 — does it project to a position or vanish?)
- Empty endset (link with no `from` spans — is projection vacuously defined, or undefined?)
- Coverage entirely contained in a single Vstream span vs. coverage straddling N>2 spans
- DELETE of the exact coverage range (does LP-CONTR distinguish exact-coverage from partial-coverage deletion?)
- INSERT inside a coverage range (does this produce two projection clusters or one?)
**Required**: Add these cases to the boundary working, or state explicitly why the existing six subsume them.

### Issue 6: No concrete example
**ASN-0096, overall structure**: claims-only presentation
**Problem**: Review standard #6 mandates a concrete example verifying key postconditions. Nothing in the summary indicates a worked scenario (e.g., "link L with coverage [3,7) in document D; apply INSERT 'XY' at V-position 5; show proj(L.from, D, Σ') yields V-positions {3,4,7,8} and LP-EXT holds").
**Required**: A single end-to-end example exercising LP-CONTR or LP-EXT against a specific Vstream/POOM state, with the projection computed before and after.

### Issue 7: Weakest precondition analysis not evident
**ASN-0096, derived guarantees**: claims of survival and discoverability
**Problem**: For LP-SURV, the non-trivial wp question is: under what conditions on the K.μ transition does the postcondition "projection non-empty after" hold? This is exactly the case Standard #7 calls out as mandatory. The summary does not indicate this analysis is present.
**Required**: A wp computation for at least LP-SURV (and ideally LP-DISC), identifying the transition predicates that strengthen or weaken the survival guarantee.

### Issue 8: Non-invariants need precise statement of *what* changes
**ASN-0096, LP-NOV, LP-NOC, LP-NOD**: "what changes"
**Problem**: Three non-invariant claims are listed without expansion. Calling something a non-invariant is only useful if the negation is sharp — "X is not preserved" must be paired with a witness transition that demonstrably violates X. Without seeing the witnesses, these are not claims; they are absences of claims.
**Required**: For each non-invariant, exhibit one K.μ transition family that violates it, so the non-invariance is constructive rather than declarative.

## OUT_OF_SCOPE

### Topic 1: Projection composition, rendering equivalence, fork correspondence, S5-sharing cardinality
**Why out of scope**: These are listed as open questions in the ASN itself, and concern interactions with versioning, rendering pipelines, and transclusion-cardinality effects that belong in dedicated ASNs once the single-document, single-version projection semantics here are stable.

### Topic 2: Link type semantics and replication protocol
**Why out of scope**: Explicitly excluded by the scope statement; if the ASN treats LP-TYPE only as preservation of the type field under transitions (not interpretation), that is consistent with scope.

VERDICT: REVISE
