# Review of ASN-0102

## REVISE

### Issue 1: Source references not pinned to the content subspace

**ASN-0102, Precondition P1 / §"What is preserved"**: P1 requires only that each `rᵢ = (d_i, σ_i)` be "a well-formed content reference (ASN-0058)"; P3 then *asserts* "resolved addresses lie in `dom(Σ.C)` and so carry `subspace_I(·) = s_C`."

**Problem**: A content reference in ASN-0058 is generic over the source subspace — `σ = (u, ℓ)` with subspace identifier `u₁` (it requires `V_{u₁}(d_s) ≠ ∅`, not `u₁ = s_C`). Nothing in P1 forbids `u₁ = s_L`. If a source reference points into a source document's link subspace, `resolve_Σ(R)` yields addresses in `dom(Σ.L)`, not `dom(Σ.C)`. The discharge of `wp(COPY, S3★) ≡ (A j,i : a_j+i ∈ dom(Σ.C))` is justified "by C1 (resolution yields only existing addresses)" — but C1 (ResolutionIntegrity) concludes `dom(C)` only when the reference is into the content subspace (its proof rests on S3, the content-routing invariant). The argument is therefore circular: P3 assumes the source is content, and that assumption is exactly what must be a stated precondition. As written, COPY admits inputs that violate S3★ at the copied positions.

**Required**: Add to P1 an explicit conjunct that every source reference is into the content subspace of its source document — `subspace(u_i) = s_C` (equivalently `V_{s_C}(d_i)`-resident) for each `rᵢ` — so that C1 applies and `a_j+i ∈ dom(Σ.C)` is genuinely established rather than assumed.

### Issue 2: Dangling references to claims not present in the note

**ASN-0102, X12**: "The earlier claim that the leading boundary is the *only* absorption site is false — the trailing boundary is an equal candidate whenever `p ≤ n_S`." **ASN-0047... X14, J1'★**: "This corrects the naïve reading that *every* recorded pair reflects a fresh range extension..."

**Problem**: Both passages refute a "claim"/"reading" that appears nowhere in the note. These are residue from a prior revision. An ASN must be self-contained; a reader cannot evaluate a correction to a statement that was never made, and the rhetoric reads as if a missing earlier section is being addressed.

**Required**: State X12 and the J1'★ analysis affirmatively (both boundaries are independent candidates; recorded pairs split into `New` range-extending and `Old` already-present) without reference to a refuted prior version.

### Issue 3: Per-state invariant preservation for the new elementary transition is only partially discharged

**ASN-0102, X14 / X15 / X16**: COPY is declared a *new* elementary transition added to `𝒦`, and the note checks S2, S3★, D-SEQ/D-MIN (via X16), S8a, and the coupling invariants J0/J1★/J1'★.

**Problem**: ExtendedReachableStateInvariants (ASN-0047) is the conjunction of a large Class (a) per-state set and a Class (b) composite-boundary set. A new elementary transition must preserve all of them or argue vacuity. In particular, P7 (ProvenanceGrounding: `(a,d) ∈ R ⟹ a ∈ dom(C)`) is a non-trivial obligation incurred precisely because COPY writes new pairs into `Σ.R` — yet it is never named; it holds only because `a_j+i ∈ dom(C)` (C1/X3), which the note should state at the point it extends `R`. Likewise P4★ (`Contains_C(Σ) ⊆ R`) is *used* at the pre-state in the J1'★ argument but never shown *preserved* at the post-state (it is, because each new content-range address is recorded — but that step is implicit).

**Required**: Either enumerate the remaining Class (a)/Class (b) invariants with one-line vacuity arguments (links/entities untouched ⇒ all L-, CL-, P8-, NodeLineage-conjuncts vacuous) or, at minimum, explicitly discharge P7 at the `Σ.R` extension and P4★ at the post-state.

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content under later displacement
The first Open Question (origin/discoverability after a subsequent displacing operation) is link-projection territory (the LP-series), correctly deferred.

### Topic 2: Re-export / further-reference containment records
The second Open Question (containment when a by-reference document is itself a source) belongs to a future composition note, not this one.

VERDICT: REVISE
