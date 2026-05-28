# Review of ASN-0101

## REVISE

### Issue 1: D10's J1★ vacuity argument has a missing case (S = s_L)

**ASN-0101, D10 (ValidComposite★ extension), J1★ bullet:**
"By D0's effect, every post-state content-subspace V-position `v` either lies in `Λ` (so `M'(d)(v) = M(d)(v)`, and the pre-state V-position `v` itself witnesses the same I-address) or has the form `σ_d(u)` for some `u ∈ Π` (so `M'(d)(σ_d(u)) = M(d)(u)`, and the pre-state V-position `u` witnesses the same I-address)."

**Problem:** The claim that every post-state content-subspace V-position lies in `Λ ∪ Q` is true only when `S = s_C`. When `S = s_L` (link-subspace deletion), `Λ ⊆ V_{s_L}(d)` and `Q = σ_d(Π) ⊆ V_{s_L}(M'(d))`; neither contains any content-subspace V-position. The post-state `V_{s_C}(M'(d)) = V_{s_C}(d)` (unchanged by D6), and these positions are not in `Λ ∪ Q`. The proof's case enumeration is incomplete, so a reader cannot verify that J1★'s second conjunct is always false.

**Required:** Add a third case to the case analysis: "When `S = s_L`, every post-state content-subspace V-position `v ∈ V_{s_C}(M'(d)) = V_{s_C}(d)` by D6, with `M'(d)(v) = M(d)(v)`, witnessing itself as a pre-state V-position with the same image." The conclusion is correct under this addition; only the case enumeration needs completion.

### Issue 2: D8 Group (i) discharge of S8★ asserts a length-1 decomposition but doesn't address whether `M'(d)` actually admits the canonical (maximally merged) decomposition

**ASN-0101, D8 Group (i) justification, S8★ paragraph:**
"S8★ holds at the post-state by the trivial singleton decomposition `{(v, M'(d)(v), 1) : v ∈ V_S(M'(d))}` for the affected subspace ... and by D6 (inheritance from the unchanged pre-state arrangement) for the other subspace."

**Problem:** S8★ requires the existence of *some* finite decomposition satisfying S8 (a) and (b), and the singleton decomposition discharges this requirement. But the ASN's earlier discussion observes that "two runs that were previously separated by the deleted region become V-adjacent. Whether their I-extents are now I-adjacent — and could therefore be merged into a single run under the bundle-algebra rules — is in general indeterminate." If the implementation does not reconcile, the singleton decomposition is the only canonical witness. The ASN should explicitly acknowledge that S8★ as stated is *existential* — the singleton decomposition discharges it regardless of whether a maximally merged decomposition exists or is preserved across the operation.

**Required:** Either explicitly note that S8★ is discharged at its weakest form (existence of any finite decomposition), or strengthen the discussion to relate the singleton decomposition to ASN-0058's canonical decomposition theory.

### Issue 3: D11's `wp(DEL, ¬Q_disc) ≡ ¬wp(DEL, Q_disc)` step relies on determinism

**ASN-0101, D11, between the discoverability wp and its negation form:**
"*DEL is deterministic.* Each component of `Σ'` is uniquely determined by `Σ` and the parameters `(d, σ)` ... Hence the wp transformer satisfies `wp(DEL[d, σ], ¬Q) ≡ ¬wp(DEL[d, σ], Q)` for every postcondition `Q`, licensing the negation equivalences below."

**Problem:** The determinism argument enumerates each component of `Σ'` and notes that each is uniquely determined. But the post-state component `M'(d)` is constructed pointwise via `M'(d)(v) = M(d)(σ_d^{-1}(v))` on `Q`, requiring the inverse `σ_d^{-1}` to be a function — i.e., requiring `σ_d` to be injective. Injectivity is established in D1 via TS2, but the determinism argument cites this only implicitly through the construction. A reader expecting a Dijkstra-style proof would want determinism to cite D1's injectivity result explicitly.

**Required:** Make the citation explicit: "M'(d)(v) for v ∈ Q is uniquely determined by D1's bijectivity of σ_d (TS2 applied at length m_S)."

### Issue 4: Example coverage of D9 bullet 2 is uniformly vacuous

**ASN-0101, three worked examples:**

The worked example (content subspace, depth 3), the link-subspace example (depth 2), and the cross-document example each populate only one subspace of the relevant document. Consequently, D9's bullet 2 — "If `d'' = d`, restricted to the unique subspace `S' ∈ {s_C, s_L}` with `S' ≠ S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_{S'}(d) = project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d)`" — is trivially satisfied by an empty `V_{S'}(d)` in every example. No example exercises the case where DEL in subspace S preserves a *populated* other-subspace projection bytewise.

**Required:** Either add a fourth example with both subspaces populated, or explicitly state that bullet 2 is verified in every example via the vacuous case (when `V_{S'}(d) = ∅` the equation reduces to `∅ = ∅`), with the load-bearing content of D9 bullet 2 being captured trivially by D6.

### Issue 5: Argument about why DEL ≠ K.μ⁻ + K.μ~ rests partly on external observability of `Σ_mid`

**ASN-0101, "The operation" section, on why DEL is a primitive:**
"`Σ_mid` is itself a member of the system's history — it can be queried, logged, or witnessed by any external monitor that reads the per-state history."

**Problem:** The argument leans on the existence of *external monitors* and *queries* — concepts not formally part of the foundation ASNs' state-space semantics. SequentialAtomicTransitions (ASN-0093) does establish that states form a totally ordered sequence, which gives sequence-length distinctness. But "external monitor" and "log" are operational/implementation concepts; their use blurs the architectural argument with implementation pragmatics.

**Required:** Either ground the "observability" claim in a formal observational notion derivable from the foundations (e.g., the predicate `(E i : Σ_i = Σ_mid)` over the history sequence, which differs between the one-step and two-step traces), or clearly separate the sequence-length argument (formal, load-bearing) from the observational argument (corroborative, informal). The ASN already labels the observational distinctness "corroborative, not load-bearing," but the introduction of "external monitor" still introduces an undefined concept into a formal section.

## OUT_OF_SCOPE

### Topic 1: Recoverable DELETE — operations that produce a state from which `M(d)` is recoverable from `M'(d)` alone

**Why out of scope:** The ASN explicitly defers full historical reconstruction to the versioning mechanism, and D5 + D2 supply the substrate for reconstruction without claiming that DELETE itself is the reconstruction mechanism. A future ASN on full version semantics is the appropriate locus.

### Topic 2: Orphan I-address enumeration — operations to discover content addresses absent from every arrangement

**Why out of scope:** Explicitly addressed in the "Boundaries the abstract specification does not cross" section. Enumeration support is a downstream implementation concern, not an abstract operation.

### Topic 3: Causal ordering between DELETE on transcluding documents

**Why out of scope:** Listed in Open Questions; concerns inter-operation coordination that belongs in a future ASN on multi-document protocols.

VERDICT: REVISE
