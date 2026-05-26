# Review of ASN-0087

## REVISE

### Issue 1: Invariant table omits S2 (functionality)

**ASN-0087, "Invariant Preservation"**: The table lists L-invariants and arrangement invariants but does not explicitly verify S2 (`M(d)` is a partial function).

**Problem**: S2 is the foundational invariant that arrangements are functions. Adding `{v_ℓ ↦ ℓ}` could in principle conflict with an existing image at `v_ℓ`, breaking functionality.

**Required**: Add a one-line check: `v_ℓ ∉ dom(Σ.M(d))` by K.μ⁺_L's positioning rule combined with D-SEQ★ at `Σ` (which gives `V_{s_L}(d) = {[s_L, k] : 1 ≤ k ≤ n_L}` and `v_ℓ = [s_L, n_L + 1]` outside this set), so `Σ'.M(d)` remains a partial function.

### Issue 2: Invariant table omits trivially-preserved per-state invariants

**ASN-0087, "Invariant Preservation"**: The closing paragraph says "For state components unchanged by MAKELINK (`C`, `E`, `R`), the invariants P0, P1, P2, P4★, P6, P7, P8 are preserved trivially."

**Problem**: The ExtendedReachableStateInvariants per-state list includes S4, S7a, S7b, S7c, S7d, C-fin, NodeLineage. These are not enumerated. The closing paragraph mentions P0–P2 (which are *transition* invariants, not per-state) but skips the per-state invariants over `C` and entity structure.

**Required**: Replace the closing paragraph with an explicit enumeration: S4 (preserved by K.λ's freshness — the new allocation event for `ℓ` is distinct from all prior events); S7a, S7b, S7c, S7d (vacuous since `C` unchanged); C-fin (vacuous since `dom(C)` unchanged); P6, P7, P8 (vacuous since `E`, `R`, `C` unchanged); NodeLineage (vacuous since `E` unchanged).

### Issue 3: LP3★ citation in Reflexive Endsets is needlessly indirect

**ASN-0087, "Reflexive Endsets"**: "Σ'.M(d)(v_ℓ) = ℓ ∈ coverage(Σ'.L(ℓ).eᵢ) (using LP3★ to lift coverage to Σ')."

**Problem**: LP3★ is the multi-step transition lemma for links *already in* `dom(L)` at the starting state. Here `ℓ ∉ dom(Σ.L)`, so the natural derivation is direct: K.λ's effect gives `L_mid(ℓ) = (e₁, ..., eₙ)`, K.μ⁺_L's frame on `L` preserves this, so `L'(ℓ).eᵢ = eᵢ` and `coverage(L'(ℓ).eᵢ) = coverage(eᵢ)` by direct evaluation. The LP3★ invocation requires the reader to mentally insert `Σ_mid` as the intermediate anchor.

**Required**: Replace "(using LP3★ to lift coverage to Σ')" with "(by K.λ's effect `L_mid(ℓ).eᵢ = eᵢ` and K.μ⁺_L's frame `L'(ℓ) = L_mid(ℓ)`, so `coverage(L'(ℓ).eᵢ) = coverage(eᵢ)`)".

### Issue 4: "Reassign" terminology in Permanence is imprecise

**ASN-0087, "Permanence"**: "Subsequent operations may remove it (per the contraction operation's rules) or reassign it (per the reordering operation's rules)."

**Problem**: K.μ~ (ArrangementReordering) does not reassign `v_ℓ` itself — V-positions are tumblers, structurally fixed. K.μ~ rebinds the *image* via a bijection `π`, so after K.μ~, `M(d)(v_ℓ)` may differ from `ℓ`, and `ℓ` may appear at a different V-position. By K.μ~-FIX, `dom(M(d))` is preserved, so `v_ℓ` remains in the domain; what changes is which value it maps to.

**Required**: Replace "reassign it" with "rebind its image" or "relocate ℓ to a different V-position", and note: by K.μ~-FIX, `dom(M'(d)) = dom(M(d))`, so `v_ℓ` itself persists in the domain; what is mutable is the link's *V-position address* within `M(d)`'s graph.

### Issue 5: Intermediate state Σ_mid invariant preservation not verified

**ASN-0087, "Atomicity"**: The section characterizes discoverability at `Σ_mid` but does not verify that all per-state invariants hold at the intermediate state.

**Problem**: A reader observing `Σ_mid` needs assurance the state is internally consistent — not merely a transitional artifact. The substrate's atomicity guarantee is per-step (SequentialTransitionAxiom), so `Σ_mid` is a fully reachable state with K.λ as its predecessor transition. The ASN should briefly confirm S3★ holds at `Σ_mid`: every V-position in `dom(Σ_mid.M(d))` still images consistently because `Σ_mid.M = Σ.M` (K.λ frame) and `dom(Σ_mid.L) ⊇ dom(Σ.L)` (K.λ extension).

**Required**: Add a sentence confirming `Σ_mid` satisfies the per-state invariants (S3★ in particular — `dom(L)` only grows from `Σ` to `Σ_mid`, never breaking referential integrity).

### Issue 6: M-PriorLinkDisc scope is under-specified

**ASN-0087, "Side Effects on Prior Links' Discoverability"** and **claim M-PriorLinkDisc**: The biconditional `discoverable_from(ℓ', d, Σ') ⟺ ...` is stated only for the home document `d`.

**Problem**: The claim does not explicitly address `discoverable_from(ℓ', d_target, Σ')` for `d_target ≠ d`. While the K.μ⁺_L frame `(A d' ≠ d :: M'(d') = M(d'))` makes this case trivial (`discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)`), the claim does not state it.

**Required**: Either add a clause to M-PriorLinkDisc covering the `d_target ≠ d` case, or add a sentence in the section text noting that for documents other than the new link's home, prior-link discoverability is unchanged by K.μ⁺_L's frame.

## OUT_OF_SCOPE

### Topic 1: Well-formedness constraints for endsets referencing not-yet-allocated addresses

**Why out of scope**: This is an Open Question listed by the ASN itself. L4 (EndsetGenerality, ASN-0043) permits arbitrary tumbler addresses; the substrate does not enforce content existence at authoring time. Treatment of "future-reaching" endsets and resurrection patterns (LP18) is appropriately deferred.

### Topic 2: Protocol-layer atomicity guarantees for MAKELINK as a single client event

**Why out of scope**: The ASN correctly identifies this as an Open Question. The substrate provides per-step atomicity (SequentialTransitionAxiom); composite-level atomicity belongs to a higher protocol layer not yet specified.

### Topic 3: Discoverability under endsets referencing not-yet-allocated content

**Why out of scope**: Listed as an Open Question. This concerns the temporal interaction between link creation and subsequent content/document allocation, properly the subject of a future ASN.

### Topic 4: Empty non-type endsets (e₁ = ∅ or e₂ = ∅ with e₃ ≠ ∅)

**Why out of scope**: L3 permits any non-type slot to be empty. The framework handles this uniformly — `coverage(∅) = ∅`, so projection through that slot is empty. The MAKELINK specification need not single this out as a distinct case.

VERDICT: REVISE
