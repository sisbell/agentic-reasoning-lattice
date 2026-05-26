# Review of ASN-0099

## REVISE

### Issue 1: F11 derivation uses single-step L12 for a multi-step claim
**ASN-0099, Persistent Discoverability**: "This follows from L12 (ASN-0093): `a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`, so the coverage of every endset of a is unchanged across the transition."
**Problem**: F11 is stated over `Σ →* Σ'` (arbitrary reachable sequences), but L12 governs only single-step transitions `Σ → Σ'`. The derivation skips the induction step that lifts L12 across chains of transitions.
**Required**: Either invoke ASN-0098's LP13 (UnconditionalLinkPersistence), which is the multi-step version, or write the explicit induction on chain length. Note that LP3★ (multi-step coverage invariance) is the cleaner load-bearing lemma for the match predicate's stability.

### Issue 2: F8 and F9 state essentially the same proposition
**ASN-0099, Determinism / Arrangement Independence**: F8 says `result(I, Σ) = result(I, Σ')` whenever `Σ.L = Σ'.L`. F9 says `findlinks(I, Σ) = findlinks(I, Σ')` for any `Σ, Σ'` with `Σ.L = Σ'.L`.
**Problem**: The formal propositions are identical (same hypothesis, same conclusion modulo `result` vs `findlinks`). The text tries to distinguish them by emphasis ("arrangement-independence"), but no claim in F9 is absent from F8. The reader cannot tell whether F8 and F9 are the same theorem labeled twice or two distinct claims.
**Required**: Either merge them (F8 already entails arrangement independence as a corollary, since `Σ.M` is unmentioned in the hypothesis) or sharpen F9 to a distinct content — for example, state F9 as the *frame condition* that the K.μ family preserves matches, parameterized over arrangement-modifying transitions specifically.

### Issue 3: `result(I, Σ)` vs `findlinks(I, Σ)` notational distinction not formal
**ASN-0099, Completeness**: "Define `result(I, Σ)` to be the output of the unfiltered FINDLINKS on query I and state Σ."
**Problem**: This casually equates `result` with the abstract `findlinks`. But F2 and F3 are stated as if `result` could differ from the abstract specification — they say "must appear" / "must be" in `result`. If `result = findlinks` by definition, F2 and F3 are tautologies (the ASN acknowledges this). If `result` is intended to denote *implementation output* and F2/F3 are conformance obligations, this distinction needs to be in the formalism, not just the prose.
**Required**: Make the abstract-spec/implementation distinction explicit. Either drop `result` and accept F2/F3 as definitional, or formalize `result` as a separate symbol denoting an implementation's actual output set and state F2/F3 as conformance requirements.

### Issue 4: Filter-to-union conversion lacks explicit slot index range
**ASN-0099, Endset Filtering**: "The unfiltered form is instead recovered as a *union* over single-slot filters: `findlinks(I, Σ) = ⋃ᵢ findlinks_filtered({(i, I)}, Σ)`, where the union ranges over the slot indices of each link."
**Problem**: "Slot indices of each link" is ill-defined for a union outside the per-link comprehension — links have different arities (L3 only requires `|L(a)| ≥ 3`). The union notation needs a fixed index range, and the treatment of constraint `(i, I)` when `i > |L(a)|` for a given link needs to be pinned down.
**Required**: Specify the range as `i ∈ ℕ⁺` (or `1 ≤ i ≤ max{|Σ.L(a)| : a ∈ dom(Σ.L)}`) and state explicitly how `findlinks_filtered({(i, I)}, Σ)` treats links where slot `i` is absent (the natural reading is that the constraint is unsatisfiable, so such links are excluded).

### Issue 5: F5 wording "are independent" is ambiguous
**ASN-0099, Identity, Not Value**: "For I-addresses α ≠ β, the result sets `findlinks({α}, Σ)` and `findlinks({β}, Σ)` are independent: a link belongs to one or the other (or both, or neither) based entirely on whether its endset coverage includes α or β..."
**Problem**: "Independent" reads as "disjoint" on first encounter. The clarifying clause ("one or the other or both or neither") contradicts this reading. The intended content — that the membership test consults coverage, not values — is a property of the predicate, not the result sets.
**Required**: Rephrase as a property of the match predicate: "The match `matches(a, {α}, Σ)` consults `Σ.L` and coverage(·), never `Σ.C(α)`, so the test at α and the test at β are computed independently." Drop the "result sets ... are independent" framing.

### Issue 6: Empty link store boundary not addressed
**ASN-0099, The Empty Query**: Only addresses `I = ∅`.
**Problem**: The boundary case `dom(Σ.L) = ∅` (no links in the store) is not discussed. The comprehension trivially yields ∅, and F2/F3/F10/F11 hold vacuously, but the ASN's standards demand boundary cases be addressed explicitly — particularly the initial state Σ₀ where `L₀ = ∅` (ASN-0047) makes this the bootstrap query semantics.
**Required**: Add one sentence noting that `dom(Σ.L) = ∅ ⟹ findlinks(I, Σ) = ∅` for every `I`, and that this is the initial-state behavior.

### Issue 7: Worked example does not exercise F11
**ASN-0099, A Worked Example**: Verifies F2, F3, F6, F13 against the instance.
**Problem**: F11 (persistent discoverability) is the central correctness claim distinguishing FINDLINKS from arrangement-derived queries — it's what makes links survivable. The example never demonstrates it. A short additional scenario ("apply K.μ⁻ removing `v_a^2`; verify ℓ still matches `{α₂}` at the post-state") would close this.
**Required**: Extend the worked example with one arrangement-modifying step showing that `ℓ` remains matchable against `{α₂}` after `α₂`'s V-position is removed from `d_a` — this exercises F11 and F9 simultaneously.

### Issue 8: Connection to ASN-0098 LP12 unstated
**ASN-0099, The Match Predicate**: Defines `matches(a, I, Σ) ≡ (E i : ... : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)`.
**Problem**: ASN-0098's LP12 (DiscoverabilityCharacterisation) states exactly this predicate restricted to `I = ran(Σ.M(d))`. The two ASNs are using the same machinery without acknowledgement, leaving the reader to discover the redundancy. The relationship `findlinks(ran(Σ.M(d)), Σ) = {a : discoverable_from(a, d, Σ)}` is load-bearing for understanding FINDLINKS as the generalization of per-document discoverability.
**Required**: One sentence after the match predicate definition: "This generalizes ASN-0098's `discoverable_from(a, d, Σ)`, which is `matches(a, ran(Σ.M(d)), Σ)`."

## OUT_OF_SCOPE

### Topic 1: Inverse direction (FOLLOWLINK / endset resolution back to V-positions)
**Why out of scope**: The ASN explicitly defers this to a future operation. Finding the links is one half; resolving their endsets back to viewable V-positions is the other half, with its own subtleties around orphaned I-addresses.

### Topic 2: Multi-instance / replicated link store semantics
**Why out of scope**: Replication is excluded by the ASN's scope statement (BEBE inter-server protocol). Partition tolerance, consistency models, and cross-instance completeness belong with the replication layer, not the abstract operation.

### Topic 3: K.λ-to-visibility timing bounds
**Why out of scope**: The sequential-transition axiom (ASN-0093) makes the next-query-after-K.λ semantics atomic; finer timing bounds belong to performance specification, not the abstract operation.

### Topic 4: Access control as a first-class scope mechanism
**Why out of scope**: F14 acknowledges access control composes orthogonally as a scope filter. Formalizing the access-control predicate (caste-based, ownership-based, capability-based) is a separate concern with its own ASN.

VERDICT: REVISE
